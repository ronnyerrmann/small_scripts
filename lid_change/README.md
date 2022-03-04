## lid_change/
Currently it's difficult to order a Raspberry Pi, hence the webserver needs to run on a Laptop. At night I want it to be silent, hence, when I close the lid several processes need to be stopped, Volume set to mute, ...
This is solved by two scripts:

### lid_change/lid_change.py
Contains the code to run commands when the lid status changes, and to suspend or resume processes when the lid is closed or opened. The processes can be modified in the beginning of the script. Test the script with the following lines to be sure that the command list works (nocheck will ignore the open lid during the test)
```
python3 lid_change.py close nocheck
python3 lid_change.py open
```

### lid_change/checkLidClosed.sh
Contains the checks if the lid is closed and calls lid_change.py

crontab needs the following entry to start automatically:
```
@reboot <path>/small_scripts/lid_change/checkLidClosed.sh
```
