#!/bin/bash
cd $(dirname "${BASH_SOURCE[0]}")
. setenv

#Usage:
#'{"purge": true}'
#'{"start_epoch_array": ["1650059272.843029", "1650101244.100029"]}'
#'{"purge": true, "start_epoch_array": ["1650059272.843029", "1650101244.100029"]}'



OUT=$(mktemp /tmp/curl_output.XXXXXXXXXX) || { echo "-E- Failed to create temp file"; exit 1; }

if [[ $1 != "" ]]; then 
    HTTP_CODE=$(curl -o $OUT -sw '%{http_code}' --show-error -d "$1" -H 'Content-Type: application/json' ${URL_PYTHON_SERVER}/remove_events)
    RETOUR=$?
else
    HTTP_CODE=$(curl -o $OUT -sw '%{http_code}' --show-error -d "{}" -H 'Content-Type: application/json' ${URL_PYTHON_SERVER}/remove_events)
    echo "-E- arg1 is mandatory".
    RETOUR=8
fi

echo "--------------------------------------------------"
cat $OUT
echo "--------------------------------------------------"
echo "HTTP_CODE="$HTTP_CODE
if [ $RETOUR -ne 0 ] ;then
    echo "-E- remove events failed."
else
    echo "-I- remove events done."
fi

rm -f  $OUT
exit $RETOUR
