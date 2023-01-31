# NetSpeed Monitor
python based GUI that shows per second upload, download speed from the JSON endpoint provided by ns_daemon.

Since the daemon and GUI are separate apps you can close and reopen the GUI as desired. For eg when you are doing some work that requires the full screen real estate.

Upload and Download speed updates every 1s, the total is updated every 60s.

## Setup

Run the executable or the source code using your locally installed version of python using `python ns_gui.py`

### Troubleshooting

- If "calculating" is shown; Ensure that tns_daemon is installed and running on your machine.
- If the data displayed for speed is wrong ensure that you specified the desired interface name to monitor when you ran ns_daemon.
