#!/bin/bash
# Based on https://www.wikitechy.com/tutorials/linux/best-way-to-kill-all-child-processes-in-linux

killtree() {
    local _pid=$1
    # echo "this PID $_pid"
    local _sig=${2:--TERM}
    local _proc_details=$(ps hlf $_pid)
    kill -STOP ${_pid} # needed to stop quickly forking parent from producing children between child killing and parent killing
    for _child in $(ps -o pid --no-headers --ppid ${_pid}); do
        #echo "new tree on child ${_child}"
        killtree ${_child} ${_sig}
    done
    kill ${_sig} ${_pid}
    kill -CONT ${_pid} # revert the stop
    echo "killed ${_proc_details}"
}

if [ $# -eq 0 -o $# -gt 2 ]; then
    echo "Usage: $(basename $0) <pid> [signal]"
    exit 1
fi

killtree $@