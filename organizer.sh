#!/bin/bash

SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_FILE="grades_${TIMESTAMP}.csv"

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi

if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: $SOURCE_FILE was not found in the current directory."
    exit 1
fi

mv "$SOURCE_FILE" "$ARCHIVE_DIR/$ARCHIVED_FILE"
touch "$SOURCE_FILE"

echo "$TIMESTAMP | $SOURCE_FILE | $ARCHIVED_FILE" >> "$LOG_FILE"

echo "Archive completed successfully."
echo "Moved $SOURCE_FILE to $ARCHIVE_DIR/$ARCHIVED_FILE"
echo "Created a new empty $SOURCE_FILE"
echo "Logged action in $LOG_FILE"
