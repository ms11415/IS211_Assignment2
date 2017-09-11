#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 Assignment 2."""

import argparse
import csv
import logging
import urllib2
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, required=True)
args = parser.parse_args()
url = args.url

def downloadData(urlname):
    """Downloads contents at url and returns it to the caller."""
    response = urllib2.urlopen(urlname)
    data = csv.reader(response)
    # skip header row
    next(data)
    return data

def processData(contents):
    """Processes the CSV data line by line. Converts birthday to Date object
    and returns a dictionary that maps the ID to tuple of (name, birthday).
    Includes error logger when birthdays are formatted incorrectly.
    """
    # Sets up the logger.
    LOG_FILENAME = 'errors.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)
    logger = logging.getLogger('assignment2')

    # Begin processing CSV data.
    mydict = {}
    linenum = 1
    for row in contents:
        try:
            row[2] = datetime.datetime.strptime(row[2], '%d/%m/%Y')
            row[2] = row[2].date()
            mydict[row[0]] = (row[1], row[2])
        except ValueError:
            logger.error('Error processing line # %s for ID # %s',
                         linenum, row[0])
            f = open(LOG_FILENAME, 'rt')
            try:
                body = f.read()
            finally:
                f.close()
        finally:
            linenum += 1

    return mydict

def displayPerson(personID, personData):
    """Displays the person's information."""
    personID = str(personID)
    try:
        print 'Person # {} is {} with a birthday of {}'.format(
        personID, personData[personID][0], personData[personID][1])
    except:
        print 'No user found with that ID'

def main():
    csvData = downloadData(url)
    personData = processData(csvData)
    personID = 1
    while personID >= 1:
        personID = int(raw_input('Please enter an ID: '))
        if personID >= 1:
            displayPerson(personID, personData)
    else:
        print 'Goodbye!'
        exit

if __name__ == "__main__":
    main()
