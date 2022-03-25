## battery_plugged/
Running Scripts when power is disconnected to the laptop or reconnected again.
This is solved by two scripts:

### lid_change/lid_change.py
Contains the code to run commands when the lid status changes, and to suspend or resume processes when the lid is closed or opened. The processes can be modified in the beginning of the script. Test the script with the following lines to be sure that the command list works (nocheck will ignore the open lid during the test)
```
python3 lid_change.py close nocheck
python3 lid_change.py open
```

### battery_plugged/check_discharge.sh
Contains the checks if the if the batter is discharging or not and calls script_change.py

Make the script executable:
```
chmod u+x <path>/small_scripts/battery_plugged/check_discharge.sh
```

crontab needs the following entry to start automatically:
```
@reboot <path>/small_scripts/battery_plugged/check_discharge.sh
```
