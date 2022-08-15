## memory/
After the computer run a few days, memory starts to fill up. Without a pagefile, this can lead to unresponsiveness. Usually, it's just one application that is graping the memory.

So far both scripts are only tested for no paging at all.

### memory/check_memory.py
Checks the memory usage every few seconds, and if the same memory is over a threshold (96) for two seconds and the same process has the highest memory usage, that process will be killed.

Only works if the user has permission to kill the process.

### memory/fill_memory.py
Script to fill up the memory to test check_memory. Please note, this could make the machine unresponsive.