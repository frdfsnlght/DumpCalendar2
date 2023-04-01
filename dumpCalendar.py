#!/usr/bin/python3

# Requires python version >=3.7

# Preparing python:
#
# pip3 install icalendar
# pip3 install recurring-ical-events
# pip3 install python-dateutil

# Obtaining a calendar file:
#
# 1. Open Google Calendar
# 2. Navigate to the settings for a calendar
# 3. Click the "Export Calendar" button
# 4. Extract the ics file from the downloaded zip file
#

import sys, os.path, argparse, time, datetime
from icalendar import Calendar, Event
import recurring_ical_events

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def noCommand(args):
    print('no command was given')

def getEvents(args):

    f = open(args.input, 'rb')
    cal = Calendar.from_ical(f.read())
    f.close()
    to_tz = None
    
    print('Dumping year {}'.format(args.year))
    
    myTZ = datetime.datetime.now().astimezone().tzinfo
    print('My timezone is {}'.format(myTZ))
    
    timeMin = datetime.datetime(args.year, 1, 1, tzinfo = myTZ)
    timeMax = datetime.datetime(args.year, 12, 31, 23, 59, 59, tzinfo = myTZ)
    allEvents = recurring_ical_events.of(cal).between(timeMin, timeMax)

    # filter events
    events = []
    for event in allEvents:
        if not isinstance(event['DTSTART'].dt, datetime.datetime):
            continue
        events.append({
            'summary': event['SUMMARY'],
            'start': event['DTSTART'].dt.astimezone(myTZ),
            'end': event['DTEND'].dt.astimezone(myTZ)
        })
        
    events.sort(key = lambda e: e['start'])
    
    month = 1
    print('{}\t{}\t{}\t{}'.format('Start', 'End', 'Diff', 'Summary'))
    for event in events:
        if month != event['start'].month:
            month = event['start'].month
            print()
        print('{}\t{}\t{}\t{}'.format(event['start'].strftime('%m/%d/%Y %H:%M:%S'), event['end'].strftime('%m/%d/%Y %H:%M:%S'), event['end'] - event['start'], event['summary']))

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Convert calendar entries to TSV')
    parser.set_defaults(func = noCommand)
    
    parser.add_argument('input', type = str, help = 'the calendar input file')
    parser.add_argument('year', type = int, nargs = '?', default = datetime.date.today().year, help = 'the year to extract, or the current year if not specified')
    parser.set_defaults(func = getEvents)

    args = parser.parse_args()
    args.func(args)

