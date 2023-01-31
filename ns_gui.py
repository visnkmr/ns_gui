# ns_gui.py
# Written by: https://visnkmr.github.io

import tkinter as tk
import requests
import json

# Variables for use in the size() function.
KB = float(1024)
MB = float(KB ** 2)  # 1,048,576
GB = float(KB ** 3)  # 1,073,741,824
TB = float(KB ** 4)  # 1,099,511,627,776


def closewin(event):
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
    try:
        response_API = requests.get('http://localhost:6798/')
        data = response_API.text
        parse_json = json.loads(data)
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
    except requests.exceptions.RequestException as e:
        label_total_usage["text"] = f'Ensure tnsoverlaydaemon is working.'
        label_total_usage.grid(row=0, column=2)
        # raise SystemExit(e)
    window.after(REFRESH_DELAY, update)  # reschedule event in refresh delay.


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
