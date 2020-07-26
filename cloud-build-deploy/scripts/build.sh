#!/bin/bash
repo=$1
filename='/workspace/diff.txt'
outputfile='/workspace/cloudbuilds.txt'
branch=$2
commit_hash=$3
touch /workspace/tmpfile.txt
status="0"
while read line; do
	IFS='/'
	read -ra ADDR <<< "$line"
    if [ ${ADDR[0]} == "pipelines" ];
    then
	    echo ${ADDR[0]}/${ADDR[1]} >> /workspace/tmpfile.txt
    else
        if [ ${ADDR[0]} == "schemas" ] || [ ${ADDR[0]} == "dlp" ];
        then
	        echo ${ADDR[0]} >> /workspace/tmpfile.txt
        fi
    fi
done < "$filename"
cat /workspace/tmpfile.txt | sort -u > "$outputfile"
while read line; do
    if [[ $line =~ "pipelines"* ]]; then
        if [[ ! -f "/workspace/datalake-repo/$line/cloudbuild.yaml" ]]; then
            cat "/workspace/datalake-repo/cloud-build-deploy/pipelines/build-assets/base.yaml" > "/workspace/datalake-repo/$line/cloudbuild.yaml"
            for dir in `find "/workspace/datalake-repo/$line/" -maxdepth 1 -mindepth 1 -type d`; do
                    directory=`echo $dir | awk -F"/" '{print $NF}'`
                    if [[ -f "/workspace/datalake-repo/cloud-build-deploy/pipelines/build-assets/$directory-step.yaml" ]]; then
                        cat "/workspace/datalake-repo/cloud-build-deploy/pipelines/build-assets/$directory-step.yaml" >> "/workspace/datalake-repo/$line/cloudbuild.yaml"
                    fi
            done
            cat "/workspace/datalake-repo/cloud-build-deploy/pipelines/build-assets/package.yaml" >> "/workspace/datalake-repo/$line/cloudbuild.yaml"
        fi
        _PIPELINE_NAME=`echo "$line" | cut -d '/' -f 2`
        status=`gcloud builds submit --config "/workspace/datalake-repo/$line/cloudbuild.yaml" --substitutions=_BRANCHNAME=$branch,_ARTIFACT_REPO=$repo,_PIPELINE_NAME=${_PIPELINE_NAME},_SHORT_SHA=$commit_hash`
    else
        status=`gcloud builds submit --config "/workspace/datalake-repo/$line/cloudbuild.yaml" --substitutions=_BRANCHNAME=$branch,_ARTIFACT_REPO=$repo,_SHORT_SHA=$commit_hash`
    fi
    if [[ $status -ne "0" ]]; then
        echo "Build failed for $line"
        status="1"
    fi
done < "$outputfile"
if [[ $status -ne "0" ]]; then
    exit 1;
fi
