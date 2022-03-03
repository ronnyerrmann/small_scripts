## lid_change/
Currently it's difficult to order a Raspberry Pi, hence the webserver needs to run on a Laptop. At night I want it to be silent, hence, when I close the lid several processes need to be stopped, Volume set to mute, ...
This is solved by two scripts:

### lid_change/lid_change.py
Contains the code to run commands when the lid status changes, and to suspend or resume processes when the lid is closed or opened.

### lid_change/checkLidClosed.sh
Contains the checks if the lid is closed and calls lid_change.py

crontab get's the following entry:
