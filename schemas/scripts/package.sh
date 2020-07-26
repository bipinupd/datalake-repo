#!/bin/bash
mkdir -p /workspace/schemas
cd /workspace/schemas
xargs mkdir -p < /workspace/dir-structure.txt
echo "****************************************************"
ls -la /workspace/schemas/enterprise/example_dataset/*
while IFS= read line
do
    echo "********************/workspace/$line&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    cp "/workspace/datalake-repo/$line" "/workspace/$line"
done < "/workspace/schema-diff.txt"
cp  /workspace/datalake-repo/schemas/scripts/* /workspace/schemas/scripts/
cp /workspace/datalake-repo/schemas/cloudbuild.yaml /workspace/schemas/cloudbuild.yaml
cp /workspace/datalake-repo/schemas/cloudbuild-deploy.yaml /workspace/schemas/cloudbuild-deploy.yaml
ls -la /workspace/schemas/*
echo "****************************************************"
ls -la /workspace/schemas/enterprise/example_dataset/*
cd /workspace
zip -r schemas.zip schemas/