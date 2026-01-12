import sys
import os
import time
import psutil
import subprocess

commandList = []    # command when closed, command when opened, optional parameters to check before these commands are run:
                    #   "not"/"only" if, command to check, "contains", (part of the) output of the command 
commandList.append(["boinccmd --set_run_mode never", "boinccmd --set_run_mode auto", ["not", "boinccmd --get_cc_status", "contains", "CPU status\n    suspended: user request"] ])
commandList.append(["killall zoom", ""])
commandList.append(["gnome-screensaver-command -l", ""])
commandList.append(["killall -STOP Spider", "killall -CONT Spider"])
#commandList.append(["systemctl --user stop pulseaudio.socket", "systemctl --user start pulseaudio.socket"])  #Replaces the two commands below
# commandList.append(["amixer -q -D pulse sset Master mute", "amixer -q -D pulse sset Master unmute"])
# commandList.append(["killall -STOP pulseaudio", "killall -CONT pulseaudio"])    # doesn't stop tick_sched_timer to use a lot of power in powertop

commandListSudo = []
commandListSudo.append(["service bluetooth stop", "service bluetooth start"])
commandListSudo.append(["pm-powersave true", "pm-powersave false"])

processList = []                # Processes to suspend 
processList.append("chrome")
processList.append("opera")
processList.append("thunderbird")
processList.append("java")
processList.append("steamwebhelper")
tooHighCPUPercentage = 5
checkProcessesSeconds = 120     # How many seconds after closing the lid to check and suspend the processes that have a high CPU usage and are in processList

fileToPIDs = "/tmp/suspendClosed.pid"
fileToExcludedOpenCmds = "/tmp/suspendClosed.cmds"

lidStatusCmd = ["cat","/proc/acpi/button/lid/LID0/state"]
lidStatusOpen = 'open'

"""
Test the script with the following lines to be sure that the command list works
python3 lid_change.py close nocheck
python3 lid_change.py open
"""

def getListOfProcessSortedByCPU():
    '''
    Get list of running process sorted by CPU Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_times'])
            pinfo['cpu_percent'] = proc.cpu_percent(interval=0)
            #pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            #if pinfo['name'] in processList:
            # Also return the whole process object
            pinfo['proc'] = proc
            # Append dict to list
            listOfProcObjects.append(pinfo);
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    time.sleep(1)
    for ii in range(len(listOfProcObjects)):    # Now the values for cpu_percent become meaningful
        try:
            listOfProcObjects[ii]['cpu_percent'] = listOfProcObjects[ii]['proc'].cpu_percent(interval=0)
        except (psutil.NoSuchProcess):
            pass
    # Sort list of dict by key 
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['cpu_percent'], reverse=True)

    return listOfProcObjects

def resumePIDs(suspendedPID):
    # Load the PID file and add PIDs to suspendedPID
    if os.path.isfile(fileToPIDs):
        my_file = open(fileToPIDs, "r")
        data = my_file.read()
        dataList = data.split("\n")
        for entry in dataList:
            if len(entry) < 2:
                continue
            entryInt = int(entry)
            if entryInt not in suspendedPID:
                suspendedPID.append(entryInt)
    # resume processes
    for pid in suspendedPID:
        try:
            proc = psutil.Process(pid)
            proc.resume()
            print("resumed", proc.as_dict(attrs=['pid', 'name']))
        except (psutil.NoSuchProcess):
            print("not resumed as not existend PID: ", pid)
            pass
    if os.path.isfile(fileToPIDs):
        os.remove(fileToPIDs)
    if os.path.isfile(fileToExcludedOpenCmds):
        os.remove(fileToExcludedOpenCmds)

def checkCondiditionBeforeSuspend(command, runCommand, fileToExcludedOpenCmds):
    if len(command[2]) != 4:
        raise ValueError("Wrong number of entries in the list", "Expected 4 entries, got {0}".format(len(command[2])), command[2])
    # Do the comparison
    try:
        outputCheckCmd = subprocess.check_output(command[2][1].split()).decode()
    except:
        outputCheckCmd = ''
    result = -1
    if command[2][2] == "contains":
        result = outputCheckCmd.find(command[2][3])
        print("Running command {0} led to the following results: Expected text:\n{1}\nwas found at position {2} in the result from the command:\n{3}".format(command[2][1], command[2][3], result, outputCheckCmd))
    else:
        print("Do not know what to do with entry index 2: "+command[2][2])
    # Check the comparison
    if command[2][0] == "not":
        if result != -1:
           runCommand = False
    elif command[2][0] == "only":
        if result == -1:
            runCommand = False
    else:
        print("Do not know what to do with entry index 0: "+command[2][0])
    if not runCommand:
        os.system("echo {0} >> {1}".format(command[1], fileToExcludedOpenCmds))
    return runCommand

# Handle the args
excludedOpenCmds = []
if len(sys.argv) < 2:
    raise ValueError('Parameter missing', 'Expected at least open or close')
if sys.argv[1] == 'open':
    commandIndex = 1
    if os.path.isfile(fileToExcludedOpenCmds):
        my_file = open(fileToExcludedOpenCmds, "r")
        excludedOpenCmds = my_file.read().split("\n")
elif sys.argv[1] == 'close':
    commandIndex = 0
else:
    raise ValueError('Unknown parameter', 'Expected open/close, but got '+sys.argv[1])
checkOpen = True
if len(sys.argv) > 2:
    if sys.argv[2] == 'nocheck':
        checkOpen = False

# Run the commands    
for command in commandList:
    runCommand = True
    if command[commandIndex] in excludedOpenCmds:
        runCommand = False
    if len(command) > 2 and commandIndex == 0:      # There is a condition
        runCommand = checkCondiditionBeforeSuspend(command, runCommand, fileToExcludedOpenCmds)
    if runCommand:
        os.system(command[commandIndex])

# Stop processes
suspendedPID = []
if commandIndex == 0:
    if os.path.isfile(fileToPIDs):
        startPIDs(suspendedPID)
    endTime = time.time() + checkProcessesSeconds
    while time.time() < endTime:
        listOfProcObjects = getListOfProcessSortedByCPU()
        for ii in range(20):
            #print(listOfProcObjects[ii])
            if listOfProcObjects[ii]['name'] in processList and listOfProcObjects[ii]['cpu_percent'] >= tooHighCPUPercentage:
                try:
                    listOfProcObjects[ii]['proc'].suspend()
                    suspendedPID.append(listOfProcObjects[ii]['pid'])
                    os.system("echo {0} >> {1}".format(listOfProcObjects[ii]['pid'], fileToPIDs))
                    print("suspended", listOfProcObjects[ii]['name'], listOfProcObjects[ii]['pid'], listOfProcObjects[ii]['cpu_percent'])
                except (psutil.NoSuchProcess):
                    pass
        if checkOpen:
            for jj in range(1):
                time.sleep(1)
                # Check that lid wasn't opened yet
                result = subprocess.check_output(lidStatusCmd)
                result = result.decode().split()[-1]
                if result == lidStatusOpen:
                    print("Lid was opened while still checking if processes need to be suspended -> resuming processes")
                    commandIndex = 1
                    break
        else:
            time.sleep(1)   # Don't check for processes all the time
        if commandIndex == 1:
            break

# Resume processes
if commandIndex == 1:
    resumePIDs(suspendedPID)
    
  
