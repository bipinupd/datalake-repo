#!/bin/bash
mkdir -p /workspace/dlp/{deIdentify-templates,inspect-templates,scripts}
mkdir -p /workspace/dlp/tests/utils
mkdir -p /workspace/dlp/tests/it-test
cd /workspace/dlp
find . -type f -name '*.ddl' -delete
cd /workspace/datalake-repo/
cp -R dlp/scripts/* /workspace/dlp/scripts/
cp -R dlp/tests/utils/*.py /workspace/dlp/tests/utils/
cp dlp/tests/conftest.py /workspace/dlp/tests/conftest.py
cp dlp/tests/pytest.ini /workspace/dlp/tests/pytest.ini

input="/workspace/dlp-diff.txt"
while IFS= read -r line
do
  subfolder=$(echo "$line" | cut -d '/' -f 2)
  if [[ $subfolder == "deIdentify-templates" ]]; then
    cp "$line" "/workspace/dlp/deIdentify-templates/"
    template_file=`echo "${line}" | awk -F/ '{print $NF}'`
    it_test_file="${template_file%.*}"_test.py
    cp "dlp/tests/it-test/$it_test_file" "/workspace/dlp/tests/it-test/"
  fi
  if [[ $subfolder == "inspect-templates" ]]; then
    cp "$line" "/workspace/dlp/inspect-templates/"
    template_file=`echo "${line}" | awk -F/ '{print $NF}'`
    it_test_file="${template_file%.*}"_test.py
    cp dlp/tests/it-test/$it_test_file /workspace/dlp/tests/it-test/
  fi
done < "$input"
cd /workspace
zip -r dlp.zip dlp/
