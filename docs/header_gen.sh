#!/bin/bash

# Extract tags from Git
tags=$(git tag)

# Convert tags to a space-separated string
mapfile -t tags_array <<< "$tags"

# Pass the tags to the Python script
python docs/header_gen.py --tags "${tags_array[@]}"
