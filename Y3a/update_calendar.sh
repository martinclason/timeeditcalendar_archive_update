#!/bin/bash

echo | date
echo "updating archive calendar..."

FTP_PASSWD=$(cat /Users/martinclason/.secrets/kalender@martinclason.se)

echo $FILE_PATH

FILE_PATH="/Users/martinclason/.timeeditcalendar_archive_update/Y3a"

cd $FILE_PATH

./download_calendar_csv.sh -u "https://cloud.timeedit.net/liu/web/schema/ri177326X50Z09Q5Z66g1Yn0yZ086Y00Q02gQY5Q5276b074QyX.csv" -o Y3_18-19.csv
./filter_future_dates_from_csv.py -i Y3_18-19.csv -o Y3_18-19_filtrerat.csv
./parse_csv_to_ics.py -i Y3_18-19_filtrerat.csv -o Y3_18_19_filtrerat.ics -calname "TimeEdit-Y3.a\, ARKIV"
./upload_calendar_to_webserver.sh -i Y3_18_19_filtrerat.ics --password $FTP_PASSWD

exit 0
