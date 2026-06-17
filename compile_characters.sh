#!/bin/bash

find stages chars -type f -name "*-sff.def" | while read -r file; do
    echo "Processing: $file"
    wine sprmake2.exe "$file"
done