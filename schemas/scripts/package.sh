#!/bin/bash
mkdir -p /workspace/schemas/
cd /workspace/schemas/
xargs mkdir -p < /workspace/dir-structure.txt
while read line;
do
    cp "/workspace/datalake-repo/$line" "/workspace/$line"
done < /workspace/schema-diff.txt
cp -R /workspace/datalake-repo/schemas/scripts/ /workspace/schemas/scripts/
cp /workspace/datalake-repo/schemas/cloudbuild.yaml /workspace/schemas/cloudbuild.yaml
cp /workspace/datalake-repo/schemas/cloudbuild-deploy.yaml /workspace/schemas/cloudbuild-deploy.yaml
ls -la /workspace/schemas/*
cd /workspace
zip -r schemas.zip schemas/