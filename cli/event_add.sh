#!/bin/bash
cd $(dirname "${BASH_SOURCE[0]}")
. setenv


OUT=$(mktemp /tmp/curl_output.XXXXXXXXXX) || { echo "-E- Failed to create temp file"; exit 1; }

if [[ $1 != "" ]]; then 
    HTTP_CODE=$(curl -o $OUT -sw '%{http_code}' --show-error -d "$1" -H 'Content-Type: application/json' ${URL_PYTHON_SERVER}/add_event)
else
    HTTP_CODE=$(curl -o $OUT -sw '%{http_code}' --show-error -d '{"tags": ["CLI"]}' -H 'Content-Type: application/json' ${URL_PYTHON_SERVER}/add_event)
fi
RETOUR=$?

echo "--------------------------------------------------"
cat $OUT
echo "--------------------------------------------------"
echo "HTTP_CODE="$HTTP_CODE
if [ $RETOUR -ne 0 ];then
    echo "-E- add event failed."
else
    echo "-I- add event done."
fi

rm -f  $OUT
exit $RETOUR
