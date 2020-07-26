#!/bin/bash
cd "/workspace/${_SHORT_SHA}/"
status="0"
for dir in `find . -maxdepth 1 -mindepth 1 -type d`; do
    directory=`echo "$dir" | sed 's/\.\///g'`
    if [[ "$directory" != "cloud-build-deploy" ]]; then
        subs_var=""
        # echo "_PIPELINE_NAME=$directory" >> /workspace/build_vars
        while read line; do
            if [[ "$line" == "_PIPELINE_NAME" ]]; then
                subs_var+=`echo "_PIPELINE_NAME=$directory,"`
            else
                subs_var+=`cat /workspace/build_vars | grep $line`,
            fi
        done < "$directory/scripts/deploy_variables"
        _subs=`echo $subs_var | sed 's/,*$//'`
        echo "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        cat "$directory/cloudbuild-deploy.yaml"
        echo $_subs
        echo "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        status=`gcloud builds submit --config "$directory/cloudbuild-deploy.yaml" --substitutions=$_subs`
        if [[ $status -ne "0" ]]; then  
            echo "Build failed for $directory"
            status=1
        fi
    fi
done
if [[ $status -ne "0" ]]; then
    exit 1;
fi
