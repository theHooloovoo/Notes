#!/usr/bin/env python3

import sys
import lxml.html, requests
import datetime

def convert_date(d):
    """ Takes in a string formatted as 'Mon DD' and converts it
        to 'YYYY/MM/DD'. The year is inferred such that a date
        that occures in the past is 'pushed' up by one year.
    """
    cur_date = datetime.datetime.now()
    year = cur_date.year
    new_date = datetime.datetime.strptime(' '.join([str(year),d]), '%Y %b %d')
    # Increment the date if the timedelta is negative
    delta = cur_date - new_date
    if delta.days > 0:
        year += 1
    # convert to "YY/MM/DD"
    return str(year) + new_date.strftime("/%m/%d")

def open_band_file(f_in):
    """ Takes in a file handle, and returns a list.
        Each element of the list is in the form: [band URL, bandname].
    """
    band_list = []
    # Function Body
    for line in f_in.readlines():
        if len(line.split()) != 2:
            print("Couldn't parse:\n")
            print(line)
            sys.exit()
        else:
            band_list.append(line.split())
    return band_list

def get_tour_dates(url, bandname, tour_list):
    """ Takes in a bandcamp url, and returns a list of tour dates
        Each tour date is in the form: [date, bandname, location]
        date is in the form 'Mon DD'.
    """
    # Open the url, then extract & parse the html into a tree
    webpage = requests.get(url)
    tree = lxml.html.fromstring(webpage.content)
    # Find the 'showography' id, for that contains the list of 
    # the band's tour dates. Then step down two layers and 
    # get the complete set of tour dates, as a list.
    tours = tree.xpath('//*[@id="showography"]/ul/li')
    for n in tours:
        # Get the text, and format the list into something suitable
        t = n.xpath('./*/text()')
        text_list = [convert_date(t[0]), bandname, t[1]]
        # print(text_list)
        tour_list.append(text_list)

# =============================================================================
# === Start the Script ========================================================

band_file = open("resources/bands", 'r')
band_urls = open_band_file(band_file)

tour_list = []
for band in band_urls:
    print("  =", band, "===================================")
    get_tour_dates(band[0], band[1], tour_list)

tour_list = sorted(tour_list)

for tour in tour_list:
    print(tour[0],
          '{:<12}'.format(tour[1]),
          '{:<25}'.format(tour[2]),
         )

