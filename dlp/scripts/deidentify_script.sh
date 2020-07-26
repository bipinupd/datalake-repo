#!/bin/bash
PROJECT_ID=$1
API_ROOT_URL="https://dlp.googleapis.com"
ALL_API_CALL_SUCCESS=0;

for template in /workspace/dlp/deIdentify-templates/*.json; do
  cat "$template" | jq '.deidentifyTemplate.deidentifyConfig.recordTransformations.fieldTransformations | . [].primitiveTransformation | . [].cryptoKey.kmsWrapped.wrappedKey' |  sed 's/\"//g' | cut -d '_' -f 1 > /workspace/keys_in_template
  input="/workspace/keys_in_template"
  declare -A dlp_keys
  while IFS= read -r line
  do
    x=${line}_DLP_SECRET
    secret=`gcloud secrets versions access latest --secret="${x}"`
    dlp_keys[${line}_CRYPTO_NAME]=`echo $secret | jq -r .name`
    dlp_keys[${line}_WRAPPED_KEY]=`echo $secret | jq -r .ciphertext`
  done < "$input"

  for key in "${!dlp_keys[@]}"; do
    sed -i.bak "s|$key|${dlp_keys[$key]}|g" "$template"
  done
  
  templateId=$(cat "$template" | jq '.templateId' | sed 's/"//g')
  API_KEY=`gcloud auth print-access-token`
  TEMPLATE_API="${API_ROOT_URL}/v2/projects/${PROJECT_ID}/deidentifyTemplates"
  
  template_exists=$(curl -H "Content-Type: application/json" -H "Authorization: Bearer ${API_KEY}"  "${TEMPLATE_API}/$templateId" --write-out '%{http_code}' --silent --output /dev/null)
  method="POST"

  if [[ $template_exists == "200" ]]; then
    method="PATCH"
    TEMPLATE_API="${API_ROOT_URL}/v2/projects/${PROJECT_ID}/deidentifyTemplates/$templateId"
    jq 'del(.templateId)' "$template" > "$template".tmp && mv "$template".tmp "$template"
  fi

  DEID_CONFIG_PAYLOAD="@${template}"

  api_status=$(curl -X $method -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}"  "${TEMPLATE_API}" \
  -d "${DEID_CONFIG_PAYLOAD}" --write-out '%{http_code}' --silent --output /dev/null)
  
  if [[ ${api_status} -gt 299 ]]; then
    echo "failed registering $template" 
    ALL_API_CALL_SUCCESS=-1
  fi
done

echo $ALL_API_CALL_SUCCESS