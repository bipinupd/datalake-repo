#!/bin/bash
mkdir -p /workspace/schemas/
cd /workspace/schemas/
xargs mkdir -p < /workspace/dir-structure.txt
cd /workspace/datalake-repo/
while read line;
do
    cp "$line" "/workspace/$line"
done < /workspace/schema-diff.txt
cp -R schemas/scripts /workspace/schemas
cp schemas/cloudbuild.yaml /workspace/schemas/cloudbuild.yaml
cp schemas/cloudbuild-deploy.yaml /workspace/schemas/cloudbuild-deploy.yaml
cd /workspace
zip -r schemas.zip schemas/