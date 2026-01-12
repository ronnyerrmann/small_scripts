#!/bin/bash

# A script to perform incremental backups using rsync.
# Each time the script runs, a new folder with the current time is created.
# Any files that didn't change from the last backup will just be hardlinks to the previously backed up files
# This is for a backup of a local disk, however, it also works for remote backups.
#   Comments in the code indicate what lines to change, assuming <server> configured in .ssh/config

set -o errexit
set -o nounset
set -o pipefail

readonly SOURCE_DIR="/home/ronny/"
readonly BACKUP_DIR="/mnt/backup500/backup_increment/"
readonly DATETIME="$(date '+%Y-%m-%d_%H-%M-%S')"
readonly BACKUP_PATH="${BACKUP_DIR}/${DATETIME}"
readonly LATEST_LINK="${BACKUP_DIR}/latest"

# if backup is remote: encapsulate this into ssh server "mkdir -p ${BACKUP_DIR}"
mkdir -p ${BACKUP_DIR}

# exit if source or destination is not available
# if backup is remote: remove $BACKUP_DIR
if [[ ! -d "$SOURCE_DIR" || ! -d "$BACKUP_DIR" ]]; then
    echo "Error: $SOURCE_DIR or $BACKUP_DIR does not exist" >&2
    exit 1
fi

# if backup is remote: use server:"${BACKUP_PATH}"
rsync -a --delete \
  "${SOURCE_DIR}/" \
  --link-dest "${LATEST_LINK}" \
  --exclude "~" --exclude ".cache" --exclude "cache" --exclude ".stversions" \
  "${BACKUP_PATH}"

# if backup is remote: encapsulate this into ssh server "ln -fs ${BACKUP_PATH} ${LATEST_LINK}"
ln -fs ${BACKUP_PATH} ${LATEST_LINK}
