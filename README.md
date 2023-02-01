# NetSpeed Monitor
python based GUI that shows per second upload, download speed from the JSON endpoint provided by ns_daemon.

Since the daemon and GUI are separate apps you can close and reopen the GUI as desired. For eg when you are doing some work that requires the whole screen estate available.

Upload and Download speed updates every 1s, the total is updated every 60s.

## Setup

Once you have [ns_daemon](https://github.com/visnkmr/ns_daemon) up and running. 

Download the executable available under [releases section (for Linux, Windows)](https://github.com/visnkmr/ns_gui/releases/latest) or the source code using your locally installed version of python using 

`pip install -r requirements.txt`

`python ns_gui.py`

### Troubleshooting

- If "calculating" is shown; Ensure that tns_daemon is installed and running on your machine.
- If the data displayed for speed is wrong ensure that you specified the desired interface name to monitor when you ran ns_daemon.

## Tests (Build using Python 3.10.9)
✔️ Manjaro XFCE (Linux, based on Arch)  
Tested on Linux but uses libs that should function on Windows and Mac OS platform. Feel free to test in any other platform and tell me the results! 


## Reporting issues

Found a bug? We'd love to know about it!

Please report all issues on the GitHub [issue tracker][issues].

[issues]: https://github.com/visnkmr/ns_daemon/issues
