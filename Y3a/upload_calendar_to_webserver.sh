#!/bin/bash

echo "uploading ics-file to server..."

host='ftp.martinclason.se'
user='kalender@martinclason.se'
passwd=''
file='Y3_18-19.ics'

usage () {
   echo 'upload_calendar_to_webserver.sh -i <inputfile> -ho <host> -u <user> -p <passwd>'
}

while [ "$1" != "" ]; do
    case $1 in
        -i | --input )          shift
                                file=$1
                                ;;

        -ho | --host)           shift
                                host=$1
                                ;;

        -u | --user)            shift
                                user=$1
                                ;;

        -p | --password)        shift
                                passwd=$1
                                ;;

        * )                     usage
                                exit 1
    esac
    shift
done

/usr/local/bin/ftp -n $host <<END_SCRIPT
quote USER $user
quote PASS $passwd
put $file
quit
END_SCRIPT

echo ""
echo "Url to calendar subscription:"
echo "https://www.martinclason.se/Kalender/"$file

exit 0
