#!/bin/bash
# Author: Ronny Errmann

# If an existing valid lock file present, stop. Else clean-up and continue.
if [ -f /tmp/checkLidClosed.pid ]
then
  #if checkpid $(cat /tmp/checkLidClosed.pid)
  if ps -p $(cat /tmp/checkLidClosed.pid) > /dev/null
  then
    echo "Another session of checkLidClosed.sh is running, so terminating."
    exit 0
  else
    # The process which created the lock file no longer exists
    echo "Cleaning up after dead checkLidClosed.sh script."
    /bin/rm -f /tmp/checkLidClosed.pid
  fi
fi

# Create a lock file
echo $$ > /tmp/checkLidClosed.pid
# Make sure the lock file will be removed if this script is killed
trap "/bin/rm -f /tmp/checkLidClosed.pid; echo 'Script forcibly terminated.'; exit 1" INT TERM
trap "/bin/rm -f /tmp/checkLidClosed.pid; exit 0" EXIT

# Settings to check when open, and close and what to do
pathToScript=$(dirname $(readlink -f $0))
lidStatusCmd() {
  cat /proc/acpi/button/lid/LID0/state | awk '{print $2}' | tr -d '\n'
}
statusOpen='open'
statusClose='closed'
commandOpen="python3 $pathToScript/lid_change.py open &"
commandClose="python3 $pathToScript/lid_change.py close &"

oldStatus="$(lidStatusCmd)"
#oldStatus= ${oldStatus::-1}
while true
do
  status="$(lidStatusCmd)"
  if [ "$status" != "$oldStatus" ]
  then
    if [ "$status" == "$statusClose" ]
    then 
      eval $commandClose
    elif [ "$status" == "$statusOpen" ]
    then 
      eval $commandOpen
    else
      echo "Unexpected lid status: $status , expected $statusClose or $statusOpen"
    fi
  fi
  #echo "$status and $oldStatus"
  oldStatus=$status
  sleep 1
done



/bin/rm -f /tmp/checkLidClosed.pid






