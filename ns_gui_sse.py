# ns_gui.py
# Written by: https://visnkmr.github.io

import time
import tkinter as tk
# import requests
import json
import sseclient
import threading
import queue
url = "http://localhost:6798/stream"
# from sseclient import SSEClient

# Create a global queue to store messages from SSEClient
message_queue = queue.Queue()
# Create a global event to signal the thread to stop or continue
stop_event = threading.Event()


def sse_loop(url):
    # This function runs on a separate thread and handles SSE
    # Initialize a variable to store the last event id
    last_event_id = None
    # Use a while loop to recheck for SSE connections until the window is closed
    while True:
        # Check if the stop event is set
        if stop_event.is_set():
            # Break out of the loop and stop the thread
            break
        try:
            # Create the SSEClient object with the URL, the last event id and the retry value
            messages = sseclient.SSEClient(url, retry=5000)
            # Iterate over the messages
            for msg in messages:
                print(json.loads(msg.data))
                # Put the message data into the queue
                message_queue.put(msg.data)
                # Check if the stop event is set
                if stop_event.is_set():
                    # Break out of the loop and stop the thread
                    break
                # Update the last event id with the current message id
                last_event_id = msg.id
        except Exception as e:
            # Print the exception and retry after a delay
            print(e)
            print("Retrying connection in 5 seconds...")
            time.sleep(5)

# Variables for use in the size() function.
KB = float(1024)
MB = float(KB ** 2)  # 1,048,576
GB = float(KB ** 3)  # 1,073,741,824
TB = float(KB ** 4)  # 1,099,511,627,776


def closewin(event):
    print("attempting to end thread")
    # Set the stop event to True
    stop_event.set()
    # Wait for the thread to join
    sse_thread.join()
    # Destroy the window
    window.destroy()


def size(B,isbytes):

    B = float(B if isbytes else B*8)
    u = "B" if isbytes else "b"
    if B < KB:
        return f"{B}{u}"
    elif KB <= B < MB:
        return f"{B / KB:.2f} K{u}"
    elif MB <= B < GB:
        return f"{B / MB:.2f} M{u}"
    elif GB <= B < TB:
        return f"{B / GB:.2f} G{u}"
    elif TB <= B:
        return f"{B / TB:.2f} T{u}"


## Constants
REFRESH_DELAY = 1000  # Window update delay in ms.

## Variables to calculcate speed
last_upload, last_download, upload_speed, down_speed = 0, 0, 0, 0

## the overlay window
window = tk.Tk()
window.minsize(320, 40)
window.configure(background='black')

window.title("Network Bandwidth Monitor")  # Setting the window title.

close_label = tk.Label(
            window,
            text=' x |',
            fg='white',
            bg='black'
        )
close_label.bind("<Button-1>", closewin)
close_label.grid(row=0, column=1, padx=5, pady=10)

label_total_usage = tk.Label(text="Calculating...\n", font="12", background='black', foreground='white')
label_total_usage.grid(row=0, column=2)


# Updating Labels
def update():
    global last_upload, last_download, upload_speed, down_speed
    if not message_queue.empty():
        # Get the message data from the queue
        msg_data = message_queue.get()
        print(json.loads(msg_data))
        parse_json = json.loads(msg_data)
        upload = parse_json[0]
        download = parse_json[1]
        todaytotal = parse_json[2]

        if last_upload > 0:
            if upload < last_upload:
                upload_speed = 0
            else:
                upload_speed = upload - last_upload

        if last_download > 0:
            if download < last_download:
                down_speed = 0
            else:
                down_speed = download - last_download

        last_upload = upload
        last_download = download

        # {} {}↑ {}
        label_total_usage["text"] = f'{size(down_speed,False)}ps↓ {size(upload_speed,False)}ps↑ {size(todaytotal,True)}'
        label_total_usage.grid(row=0, column=2)
       
    else:
        # print(e)
        label_total_usage["text"] = f'Pls ensure that ns_daemon is running on your machine by browsing http://localhost:6798/ from your browser.'
        label_total_usage.grid(row=0, column=2)
        # raise SystemExit(e)
        # window.update()
        #print("test")
    window.after(REFRESH_DELAY, update)  # reschedule event in refresh delay.
# Create a new thread to run the sse_loop function with the url argument
sse_thread = threading.Thread(target=sse_loop, args=(url,))
# Start the thread
sse_thread.start()
#print("test")
window.after(REFRESH_DELAY, update)

window.overrideredirect(True)
# window.geometry("+205+205")
window.lift()
window.wm_attributes("-topmost", True)

lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def move_window(event):
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x, y))


window.bind('<Button-1>', SaveLastClickPos)
window.bind("<B1-Motion>", move_window)
window.mainloop()
