#!/bin/bash
cd $(dirname "${BASH_SOURCE[0]}")
. setenv


OUT=$(mktemp /tmp/curl_output.XXXXXXXXXX) || { echo "-E- Failed to create temp file"; exit 1; }


HTTP_CODE=$(curl -o $OUT -sw '%{http_code}' --show-error -H 'Content-Type: application/json' ${URL_PYTHON_SERVER}/list_events)
RETOUR=$?

echo "--------------------------------------------------"
cat $OUT
echo "--------------------------------------------------"
echo "HTTP_CODE="$HTTP_CODE
if [ $RETOUR -ne 0 ];then
    echo "-E- list events failed."
else
    echo "-I- list events display done."
fi

rm -f  $OUT
exit $RETOUR
