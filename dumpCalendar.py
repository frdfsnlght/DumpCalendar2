#!/usr/bin/python3

# Preparing python:
#
# pip3 install icalendar
# pip3 install python-dateutil

# Obtaining a calendar file:
#
# 1. Open Google Calendar
# 2. Navigate to the settings for a calendar
# 3. Click the "Export Calendar" button
# 4. Extract the ics file from the downloaded zip file
#

import sys, os.path, argparse, time, datetime
import pytz
from icalendar import Calendar, Event

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def noCommand(args):
    print('no command was given')

def getEvents(args):

    f = open(args.input, 'rb')
    cal = Calendar.from_ical(f.read())
    f.close()
    
    events = []
    for comp in cal.walk():
        if comp.name == 'VTIMEZONE':
            timeMin = datetime.datetime(args.year, 1, 1, tzinfo = comp.to_tz())
            timeMax = datetime.datetime(args.year, 12, 31, 23, 59, 59, tzinfo = comp.to_tz())
        elif comp.name == "VEVENT":
            start = comp.decoded('dtstart')
            if not isinstance(start, datetime.datetime): continue
            if start >= timeMin and start <= timeMax:
                events.append({
                    'summary': comp.get('summary'),
                    'start': start,
                    'end': comp.decoded('dtend')
                })
            
    month = 1
    print('{}\t{}\t{}\t{}'.format('Start', 'End', 'Diff', 'Summary'))
    for event in events:
        start = event['start']
        end = event['end']
        #print(json.dumps(event, indent = 4))
        #dt = datetime.strptime(event['start']['dateTime'], 'format)
        #dt = datetime.fromisoformat(event['start']['dateTime'])
        diff = end - start
        hours, seconds = divmod(diff.seconds, 3600)
        minutes = int(seconds / 60)
        if month != start.month:
            month = start.month
            print()
        print('{}\t{}\t{}:{:02d}\t{}'.format(start.strftime('%m/%d/%Y %H:%M:%S'), end.strftime('%m/%d/%Y %H:%M:%S'), hours, minutes, event['summary']))

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Convert calendar entries to TSV')
    parser.set_defaults(func = noCommand)
    
    parser.add_argument('input', type = str, help = 'the calendar input file')
    parser.add_argument('year', type = int, nargs = '?', default = datetime.date.today().year, help = 'the year to extract, or the current year if not specified')
    parser.set_defaults(func = getEvents)

    args = parser.parse_args()
    args.func(args)

