# Jason notes:
# forked from: https://github.com/NUKnightLab/TimelineJS3/blob/master/contrib/iamamoose/timeline.py.txt
# Use with timelinejs3 google doc template
# BUT -- this will output data in a timelinejs 2 or older JSON format that will work on older versions


# ORIG comments:
# Convert google doc spreadsheet format for timelinejs to json file
# useful if you want to experiment using google doc but eventually
# host everything yourself privately.

# Example: go to google docs spreadsheet and do File -> Download As -> CSV (Comma Separated Values)
# save as timeline.csv, run this, you get a timeline.json out
#
# Or look at your google doc ID long string like for example 1xTn9OSdmnxbBtQcKxZYV-xXkKoOpPSu6AUT0LXXszHo
# wget -qO timeline.csv 'https://docs.google.com/spreadsheets/d/1xTn9OSdmnxbBtQcKxZYV-xXkKoOpPSu6AUT0LXXszHo/pub?output=csv'

import csv
import json

import time

now = time.strftime("%Y%m%d")
csvfile = open('timeline.csv','rb')
outfilestr = 'timeline-' + now + '.json'
outfile = open(outfilestr, 'w')
print "Writing output to " + outfilestr + "..."

reader = csv.DictReader(csvfile)

data = {}
events = []
data['timeline'] = {}
data['timeline']['headline'] = "Milestones in WaterSense History"
data['timeline']['type'] = "default"
data['timeline']['text'] = "<p><img class='embedded' alt='EPA Seal' src='/sites/production/files/2013-06/seal.gif'><br>A U.S. Environmental Protection Agency Timeline</p>"
data['timeline']['startDate'] = "2004"
data['timeline']['asset'] = {}
data['timeline']['asset']['media'] = ""
data['timeline']['asset']['credit'] = ""
data['timeline']['asset']['caption'] = ""

data['timeline']['date']=events


# Didn't support 'End Time': '', 'Time': ''

keymap = {'Media': 'asset|media', 'Media Caption': 'asset|caption', 'Media Thumbnail': 'asset|thumbnail',
#          'Month': 'startDate+month', 'Day': 'startDate+day', 'Year': 'startDate+year',
          'End Month': 'end_date|month', 'End Day': 'end_date|day', 'End Year': 'end_date|year',
          'Text': 'text', 'Headline': 'headline', 
          'Group': 'group' }          

for row in reader:
    event = {}
    for a in keymap:
        if row[a]:
            if '|' in keymap[a]:
                (x,y)=keymap[a].split("|")
                if not x in event: event[x]={}
                event[x][y] = row[a]
            elif '+' in keymap[a]:
                #print keymap[a]
                # concat object... since sets are not in order I scrapped this idea in favor of just
                # setting the startDate value manually
                (x,y)=keymap[a].split("+")
                if not x in event: 
                    event[x]=""
                else: event[x] += ","
                event[x] += a + "^" + row[a]
            else:
                event[keymap[a]] = row[a]                

    # manually define the startdate value
    event['startDate'] = row['Year'] + "," + row['Month']  + "," + row['Day']

    if (row['Type'] == 'title'):
        data['title']=event
    else:
        events.append(event)

json.dump(data,outfile, sort_keys=True,indent=4)

# open file
import subprocess
subprocess.call(['open', outfilestr])