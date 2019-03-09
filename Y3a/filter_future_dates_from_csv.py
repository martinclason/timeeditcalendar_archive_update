#!/usr/bin/env python3

import sys, getopt
from datetime import datetime, date, time, timedelta


def main(argv):

    inputfile = ''
    outputfile = ''

    options = 'i:o:' # followed with : if it has argument
    longoptions = ["input=", "output="]

    try:
        opts, trailingargs = getopt.getopt(argv, options, longoptions)
    except getopt.GetoptError:
        print("parse_csv_to_ics.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-i', '--input'):
            inputfile = arg
        elif opt in ('-o', "--output"):
            outputfile = arg

    if inputfile == '':
        print('You need to specify input and output file')
        print("filter_future_dates_from_csv.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    print("filtering csv to csv...\n")

    with open(inputfile, 'r') as textfile:

        fieldnames = [
            'startdatum', 'starttid', 'slutdatum', 'sluttid', 'kurs', 'lokal',
            'undervisningstyp', 'lärare', 'studentgrupp', 'fria grupper',
            'information till student', 'studentförening', 'url']

        lines = textfile.readlines()

        linenumber = 0

        f = open(outputfile, "w+")

        for line in lines:
            if linenumber == 0:
                f.writelines(line)
            elif linenumber == 1:
                f.writelines(line)
            elif linenumber == 2:
                f.writelines(line)
            elif linenumber == 3:
                f.writelines(line)
            else:

                dstring = line[:10]

                d = datetime.strptime(dstring,"%Y-%m-%d")
                if d < datetime.now() - timedelta(days=12):
                    f.writelines(line)

            linenumber += 1

        f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
