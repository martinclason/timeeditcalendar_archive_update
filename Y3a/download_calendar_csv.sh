#!/bin/bash

echo "downloading calendar csv..."

csv_url="https://cloud.timeedit.net/liu/web/schema/ri177326X50Z09Q5Z66g1Yn0yZ086Y00Q02gQY5Q5276b074QyX.csv"
file_name="Y3_18-19.csv"

usage () {
   echo 'download_calendar_csv.sh -u <url> -o <output>'
}


while [ "$1" != "" ]; do
    case $1 in
       -u | --url )             shift
                                csv_url=$1
                                ;;

       -o | --output )          shift
                                file_name=$1
                                ;;

       * )                      usage
                                exit 1
    esac
    shift
done


/usr/bin/curl $csv_url --output $file_name

exit 0
