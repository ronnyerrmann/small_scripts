# small_scripts
A list of (Linux) tools to make life easier.

## battery_plugged/
Running Scripts when power is disconnected to the laptop or reconnected again.
This is solved by two scripts described in [battery_plugged/README.md](battery_plugged/). It is a small version of the scripts in [lid_change/](lid_change/).

## lid_change/
Currently it's difficult to order a Raspberry Pi, hence the webserver needs to run on a Laptop. At night I want it to be silent, hence, when I close the lid several processes need to be stopped, Volume set to mute, ...
This is solved by two scripts, described in [lid_change/README.md](lid_change/).

## clear_space/
When the linux system creates too much information to be stored, some automatic tasks are necessary to keep things running. They scripts are described in [clear_space](clear_space/README.md).

## memory/
Check the memory usage and kill programs if necessary [memory](memory/README.md)

## killtree.sh
Kill all (child) processes in the process tree. Call with PID and optional the SIGTERM