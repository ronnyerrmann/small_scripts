import os
import time
import psutil
from datetime import datetime


def check_prepare_lockfile():
    scriptname = os.path.basename(__file__)
    pidfile = f"/tmp/{scriptname}.pid"
    # If an existing valid lock file present, stop. Else clean-up and continue.
    if os.path.isfile(pidfile):
        try:
            oldpid = int(open(pidfile, "r").readlines()[0])
        except:
            print(f"Can't read old pidfile: {pidfile}")
        else:
            if oldpid in psutil.pids():
                print("Another session of $scriptname is running, so terminating.")
                exit(0)
            else:
                # The process which created the lock file no longer exists
                # print(f"Cleaning up after dead {scriptname} script.")
                os.remove(pidfile)

    # Create a lock file
    os.system(f"echo {os.getpid()} > {pidfile}")

    return pidfile


def get_ram_usage_percent():
    return psutil.virtual_memory().percent


def get_process(ignore_proc: set = {}):
    highest_ram = {"memory_percent": 0}
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "memory_percent", "cpu_percent", "cpu_times",
                                        "memory_full_info", "ppid", "username"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        else:
            if pinfo["memory_percent"] > highest_ram["memory_percent"] and pinfo["name"] not in ignore_proc:
                highest_ram = pinfo
    return highest_ram


if __name__ == '__main__':
    check_prepare_lockfile()
    while True:
        mem_percent = get_ram_usage_percent()
        if mem_percent > 96:
            probproc_pre = get_process()
            time.sleep(2)   # give it a second
            mem_percent = get_ram_usage_percent()
            if mem_percent > 96:
                probproc = get_process()
                if probproc_pre["pid"] == probproc["pid"]:
                    os.system(f"kill {probproc['pid']}")
                    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')} - "
                          f"Warning: using {mem_percent} percent of memory, "
                          f"therefore process {probproc} has been killed")

        time.sleep(5)
