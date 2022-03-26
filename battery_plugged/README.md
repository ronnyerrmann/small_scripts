## battery_plugged/
Running Scripts when power is disconnected to the laptop or reconnected again.
This is solved by two scripts:

### battery_plugged/status_change.py
Contains the code to run commands when the status of the power supply changes. The processes can be modified in the beginning of the script. Test the script with the following lines to be sure that the command list works:
```
python3 status_change.py stop
python3 status_change.py start
```

### battery_plugged/check_discharge.sh
Contains the checks if the if the batter is discharging or not and calls status_change.py. Please check that the command given in `BatteryStatus` will run on the system, acpi might need to be installed.

Make the script executable:
```
chmod u+x <path>/small_scripts/battery_plugged/check_discharge.sh
```

crontab needs the following entry to start automatically:
```
@reboot <path>/small_scripts/battery_plugged/check_discharge.sh
```
