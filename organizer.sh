#!/bin/bash

GRADES_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"


if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi


if [ ! -f "$GRADES_FILE" ]; then
    echo "Error: $GRADES_FILE not found. Nothing to archive."
    exit 1
fi


TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"

mv "$GRADES_FILE" "$ARCHIVED_PATH"
echo "Archived: $GRADES_FILE → $ARCHIVED_PATH"


touch "$GRADES_FILE"
echo "Created fresh $GRADES_FILE for next use."

LOG_ENTRY="[${TIMESTAMP}] Archived '${GRADES_FILE}' as '${ARCHIVED_NAME}' in '${ARCHIVE_DIR}/'"
echo "$LOG_ENTRY" >> "$LOG_FILE"
echo "Logged action to $LOG_FILE"

echo "Done."
