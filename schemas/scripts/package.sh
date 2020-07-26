#!/bin/bash
mkdir -p /workspace/schemas/
cd /workspace/schemas/
xargs mkdir -p < /workspace/dir-structure.txt
echo "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
cat /workspace/schema-diff.txt
echo "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
while read line;
do
    echo "/workspace/datalake-repo/$line ------------/workspace/$line"
    cp "/workspace/datalake-repo/$line" "/workspace/$line"
done < /workspace/schema-diff.txt
cp /workspace/datalake-repo/schemas/scripts/* /workspace/schemas/scripts/
cp /workspace/datalake-repo/schemas/cloudbuild.yaml /workspace/schemas/cloudbuild.yaml
cp /workspace/datalake-repo/schemas/cloudbuild-deploy.yaml /workspace/schemas/cloudbuild-deploy.yaml
ls -la /workspace/schemas/*
cd /workspace
zip -r schemas.zip schemas/