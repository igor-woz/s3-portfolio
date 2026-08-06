#!/bin/bash

# Check if the user provided any files
if [ $# -eq 0 ]; then
    echo "Usage: $0 file1.txt file2.txt ..."
    exit 1
fi

# Loop through each file safely
for file in "$@"; do
    if [ -f "$file" ]; then
        echo "Processing file: $file"
        aws s3 cp "$file" s3://your-bucket-name/
    else
        echo "Warning: $file is not a valid file."
    fi
done
