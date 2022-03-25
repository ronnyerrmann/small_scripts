#!/bin/bash
# Author: Ronny Errmann

# If an existing valid lock file present, stop. Else clean-up and continue.
if [ -f /tmp/check_discharge.pid ]
then
  #if checkpid $(cat /tmp/check_discharge.pid)
  if ps -p $(cat /tmp/check_discharge.pid) > /dev/null
  then
    echo "Another session of check_discharge.sh is running, so terminating."
    exit 0
  else
    # The process which created the lock file no longer exists
    echo "Cleaning up after dead check_discharge.sh script."
    /bin/rm -f /tmp/check_discharge.pid
  fi
fi

# Create a lock file
echo $$ > /tmp/check_discharge.pid
# Make sure the lock file will be removed if this script is killed
trap "/bin/rm -f /tmp/check_discharge.pid; echo 'Script forcibly terminated.'; exit 1" INT TERM
trap "/bin/rm -f /tmp/check_discharge.pid; exit 0" EXIT

# Settings to check when open, and close and what to do
pathToScript=$(dirname $(readlink -f $0))
BatteryStatus() {
  upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep state | awk '{print $2}' | tr -d '\n'
}
statusBattery='discharging'
statusPluggedIn='???'
commandStart="python3 $pathToScript/status_change.py start &"
commandStop="python3 $pathToScript/status_change.py stop &"

oldStatus="$(BatteryStatus)"
#oldStatus= ${oldStatus::-1}
while true
do
  status="$(BatteryStatus)"
  if [ "$status" != "$oldStatus" ]
  then
    if [ $status == $statusPluggedIn ]
    then 
      eval $commandStop
    elif [ $status == $statusBattery ]
    then 
      eval $commandStart
    else
      echo "Unexpected battery status: $status , expected $statusPluggedIn or $statusBattery"
    fi
  fi
  #echo "$status and $oldStatus"
  oldStatus=$status
  sleep 1
done



/bin/rm -f /tmp/check_discharge.pid






