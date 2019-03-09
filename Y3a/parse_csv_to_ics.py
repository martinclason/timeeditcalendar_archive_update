#!/usr/bin/env python3

import csv, sys, getopt, hashlib
from datetime import datetime, date, time, timedelta

# Link to validator for ics-format:
# https://icalendar.org/validator.html

def main(argv):

    inputfile = ''
    outputfile = ''
    calname = ''

    options = 'i:o:n' # followed with : if it has argument
    longoptions = ["input=", "output=", "calname="]

    try:
        opts, trailingargs = getopt.getopt(argv, options, longoptions)
    except getopt.GetoptError:
        print("parse_csv_to_ics.py -i <inputfile> -o <outputfile> -n <calname>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-i', '--input'):
            inputfile = arg
        elif opt in ('-o', "--output"):
            outputfile = arg
        elif opt in ('-n', "--calname"):
            calname = arg

    if inputfile == '':
        print('You need to specify input and output file')
        print("parse_csv_to_ics.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    print("parsing csv to ics...\n")

    def get_ics_dt(datecompstring, timecompstring):
        """
        Takes date and time on format: 2018-09-03 & 08:15
        Returns string in ics format, ex: 20190313T080000Z
        """

        d = datetime.strptime(datecompstring + " " + timecompstring, "%Y-%m-%d %H:%M")
        d = d - timedelta(hours=1) # adjusting for timezone

        return d.strftime("%Y%m%dT%H%M%SZ")


    DTSTART = lambda row : "DTSTART:" + get_ics_dt(row['startdatum'], row['starttid'])

    DTEND = lambda row : "DTEND:" + get_ics_dt(row['slutdatum'], row['sluttid'])

    def UID(row):
        s = "".join(row.values())

        d = str.encode(s)

        h = hashlib.md5(d)

        return str(h.hexdigest())

    LOCATION = lambda row : "LOCATION:" + "Lokal : " + row['lokal']

    def DESCRIPTION(row):
        s = "DESCRIPTION:"
        if row['lärare'] != '':
            s += "Lärare: " + row['lärare'] + "\\n"
        if row['information till student'] != '':
            s += row['information till student'] + "\\n"
        s += row['undervisningstyp'] + "\\n"
        return s

    LASTMODIFIED = lambda row : "LAST-MODIFIED:" + "20190307T024657Z"

    def SUMMARY(row):
        s = "SUMMARY:"

        if row['kurs'] != '':
            s += row['kurs']

        utyp = row['undervisningstyp'].lower()

        kortnamn = [
            ("föreläsning", "FÖ"),
            ("information", "INFO"),
            ("lektion", "LE"),
            ("handledning", "HA"),
            ("seminarium", "SE"),
            ("laboration", "LA"),
            ("redovisning", "RE"),
            ("studentförening", "STUDFÖR")]

        for (desc, kort) in kortnamn:
            if desc in utyp:
                s += ", " + kort

        if row['studentgrupp'] != '':
            s += ", " + row['studentgrupp']

        if row['fria grupper'] != '':
            s += ", " + row['fria grupper']

        s = s.replace(",", "\,")

        return s


    with open(inputfile, 'r') as csvfile:

        fieldnames = [
            'startdatum', 'starttid', 'slutdatum', 'sluttid', 'kurs', 'lokal',
            'undervisningstyp', 'lärare', 'studentgrupp', 'fria grupper',
            'information till student', 'studentförening', 'url']

        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        linenumber = 0

        f = open(outputfile, "w+")

        f.write(f"""BEGIN:VCALENDAR\r
VERSION:2.0\r
METHOD:PUBLISH\r
X-WR-CALNAME:{calname}\r
X-WR-CALDESC:Date limit 2018-07-30 - 2019-07-01\r
X-PUBLISHED-TTL:PT20M\r
CALSCALE:GREGORIAN\r
PRODID:MARTINCLASON\r
""")

        for row in reader:
            if linenumber == 0:
                pass
            elif linenumber == 1:
                pass
            elif linenumber == 2:
                pass
            else:
                f.write("BEGIN:VEVENT" + "\r\n")
                f.write(DTSTART(row) + "\r\n")
                f.write(DTEND(row) + "\r\n")
                f.write("UID:" + UID(row) + "\r\n") #str(uid) + "\r\n")
                f.write("DTSTAMP:20190307T024657Z" + "\r\n")
                f.write(LASTMODIFIED(row) + "\r\n")
                f.write(SUMMARY(row) + "\r\n")
                f.write(LOCATION(row) + "\r\n")
                f.write(DESCRIPTION(row) + "\r\n")
                f.write("END:VEVENT" + "\r\n")

                # print(str(row['startdatum']), end=" ")
                # print(str(row['starttid']), end=" ")

                # print(DTSTART(row), end=" ")
                # print(DTEND(row))

            linenumber += 1

        f.write("END:VCALENDAR")
        f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
