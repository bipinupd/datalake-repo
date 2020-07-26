#!/bin/bash
mkdir -p /workspace/schemas/
cd /workspace/schemas/
xargs mkdir -p < /workspace/dir-structure.txt
cd /workspace/datalake-repo/
input="/workspace/schema-diff.txt"
cat "$linput"
while read line
do
    cp "$line" "/workspace/schemas/$line"
done < "$input"
cd /workspace
zip -r schemas.zip schemas/