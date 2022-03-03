import sys
import os
import time
import psutil
import subprocess

print(sys.argv)

commandList = []    # command when closed, command when opened
commandList.append(["boinccmd --set_run_mode never", "boinccmd --set_run_mode auto"])
# boinccmd --get_cc_status
# CPU status
#    suspended: user request
commandList.append(["killall zoom", ""])
commandList.append(["amixer -q -D pulse sset Master mute", "amixer -q -D pulse sset Master unmute"])
commandList.append(["gnome-screensaver-command -l", ""])

processList = []
processList.append("chrome")
processList.append("opera")
processList.append("thunderbird")
checkProcessesSeconds = 120     # How long after closing the lid to check and suspend the processes that have a high CPU usage and are in processList

fileToPIDs = "/tmp/suspendClosed.pid"

lidStatusCmd = ["cat","/proc/acpi/button/lid/LID0/state"]
lidStatusOpen = 'open'



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
    # Sort list of dict by key vms i.e. memory usage
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

if sys.argv[1] == 'open':
    commandIndex = 1
elif sys.argv[1] == 'close':
    commandIndex = 0
else:
    print('Do not know what to do with '+sys.argv[1])
    exit(1)

# Run the commands    
for command in commandList:
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
            if listOfProcObjects[ii]['name'] in processList and listOfProcObjects[ii]['cpu_percent']>=5:
                try:
                    listOfProcObjects[ii]['proc'].suspend()
                    suspendedPID.append(listOfProcObjects[ii]['pid'])
                    os.system("echo {0} >> {1}".format(listOfProcObjects[ii]['pid'], fileToPIDs))
                    print("suspended", listOfProcObjects[ii]['name'], listOfProcObjects[ii]['pid'], listOfProcObjects[ii]['cpu_percent'])
                except (psutil.NoSuchProcess):
                    pass
        for jj in range(1):
            time.sleep(1)
            # Check that lid wasn't opened yet
            result = subprocess.check_output(lidStatusCmd)
            result = result.decode().split()[-1]
            if result == lidStatusOpen:
                print("Lid was opened while still checking if processes need to be suspended -> resuming processes")
                commandIndex = 1
                break
        if commandIndex == 1:
            break

if commandIndex == 1:
    resumePIDs(suspendedPID)
    
  
