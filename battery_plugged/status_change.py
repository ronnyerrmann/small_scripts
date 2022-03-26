# Author: Ronny Errmann
import sys
import os
import subprocess

commandList = []    # command when closed, command when opened, optional parameters to check before these commands are run:
                    #   "not"/"only" if, command to check, "contains", (part of the) output of the command 
commandList.append(["boinccmd --set_run_mode never", "boinccmd --set_run_mode auto", ["not", "boinccmd --get_cc_status", "contains", "CPU status\n    suspended: user request"] ])

fileToExcludedOpenCmds = "/tmp/suspendBattery.cmds"

"""
Test the script with the following lines to be sure that the command list works
python3 status_change.py stop
python3 status_change.py start
"""

def checkCondiditionBeforeSuspend(command, runCommand, fileToExcludedOpenCmds):
    if len(command[2]) != 4:
        raise ValueError("Wrong number of entries in the list", "Expected 4 entries, got {0}".format(len(command[2])), command[2])
    # Do the comparison
    outputCheckCmd = subprocess.check_output(command[2][1].split()).decode()
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
if sys.argv[1] == 'start':
    commandIndex = 1
    if os.path.isfile(fileToExcludedOpenCmds):
        my_file = open(fileToExcludedOpenCmds, "r")
        excludedOpenCmds = my_file.read().split("\n")
elif sys.argv[1] == 'stop':
    commandIndex = 0
else:
    raise ValueError('Unknown parameter', 'Expected open/close, but got '+sys.argv[1])

# Run the commands    
for command in commandList:
    runCommand = True
    if command[commandIndex] in excludedOpenCmds:
        runCommand = False
    if len(command) > 2 and commandIndex == 0:      # There is a condition
        runCommand = checkCondiditionBeforeSuspend(command, runCommand, fileToExcludedOpenCmds)
    if runCommand:
        os.system(command[commandIndex])

    
  
