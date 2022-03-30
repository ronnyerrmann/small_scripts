#!/bin/bash
# Author: Ronny Errmann
# Adapted from https://askubuntu.com/questions/1075050/how-to-remove-uninstalled-snaps-from-cache
# Removes old revisions of snaps
# $((100*1024**2)) is 100MB
delete_larger_than=$((200*1024**2))

set -eu
LANG=en_US.UTF-8 snap list --all | awk '/disabled/{print $1, $3}' |
    while read snapname revision; do
        cmdsize() {
            ls -l /var/lib/snapd/snaps/"$snapname"_"$revision".snap | awk '{print $5}'
        }
        size="$(cmdsize)"
        if (( "$size" >= "$delete_larger_than" ))
        then 
            snap remove "$snapname" --revision="$revision"
        fi
    done
