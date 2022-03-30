## clear_space/
When the linux system creates too much information to be stored, some automatic tasks are necessary to keep things running.

### clear the journal
Create a new crontab entry as root:
```
sudo crontab -e
```
and add the following line at the end:
```
59 6,18 * * * journalctl --vacuum-size=1000M
```
The times and size of the remaining journal entries can be changed, at the moment the command will run at 6:59 and 18:59 (if the computer is on) and will only keep the newest 1000MB of journal.

### Remove old snaps
Snap automatically installs new versions and keeps the old ones (two old versions is the standard). However some snap packages can be quite large (e.g. pycharm used over 500MB per version), so several gigabyte of storage might become occupied by old versions. To free up some space the following options are possible.

Only keep one old snap version:
```
sudo snap set system refresh.retain=2
```

However, that might not be enough and one wants to get rid of old versions that use up a lot of space. For this the script `remove_large_old_snaps.sh` can be used.
Make the script executable:
```
chmod u+x <path>/small_scripts/clear_space/remove_large_old_snaps.sh
```
One might want to change the size when old snaps should be deleted. At the moment it is set to 200MB and can be change in variable **delete\_larger\_than** in check_discharge.sh (around line 6).

Finally a new crontab entry as root can be added:
```
sudo crontab -e
```
and add the following line at the end:
```
55 6,18 * * * <path>/small_scripts/clear_space/remove_large_old_snaps.sh
```
