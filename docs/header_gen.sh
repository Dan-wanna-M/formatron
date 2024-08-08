#!/bin/bash

# Extract tags from Git
tags=$(git tag)
echo "Tags: $tags"
# Convert tags to a space-separated string
mapfile -t tags_array <<< "$tags"

# Pass the tags to the Python script
python docs/header_gen.py --current_tag "$1" --tags "${tags_array[@]}"
