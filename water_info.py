#!/opt/local/bin/python3

# Various function definitions
from water_functions import *

# For parsing the command line arguments 
import argparse
from argparse import RawDescriptionHelpFormatter

# For formatting the command line arguments
import textwrap

# For converting string to JSON
import json

# For pretty colors!
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Parse command line arguments:
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
    Retrieves current USGS water data so you don't have to leave your command line.
    To find a local sensor, check https://waterdata.usgs.gov/nwis/rt
    
    examples:
        python3 water_info.py 11141280 -H 24
            Data for the past 24 hours

        python3 water_info.py 01453000 -D 7
            Data for the past 7 days

        python3 water_info.py 04288295 -C
            Only displays the most recent data point available

        python3 water_info.py 01428750 -D 7
            This station has a temperature sensor, which is neat!
    
    If x & y values are not specified, the default graph width and height is 70 and 15'''
    )
)
parser.add_argument("id")
parser.add_argument("-d", help="Debug mode, prints out url being queried", required=False, action='store_true')
parser.add_argument("-w", help="Print waves", required=False, action='store_true')
parser.add_argument("-r", help="Output the raw data only", required=False, action='store_true')
parser.add_argument("-x", help="Specify the width of the graph", required=False)
parser.add_argument("-y", help="Specify the height of the graph", required=False)
parser.add_argument("-f", help="Display temperature in Fahreneheit", required=False, action='store_true')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-C", help="Current data only", required=False, action='store_true')
group.add_argument("-D", help="Specify the number of days you want data for", required=False)
group.add_argument("-H", help="Specify the number of past hours you want data for", required=False)

args = parser.parse_args()

# Validate our inputs
if args.x is None:
    plot_width = 70
else:
    plot_width = int(args.x)

if args.y is None:
    plot_height = 15
else:
    plot_height = int(args.y)

# A string with the timeframe ex: "past 12 hours", "past 3 days"
time_string = ""

# Build the URL we're going to query the data from
# Current data:
if args.C == True:
    api_url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites="
    api_url += args.id
    api_url += "&siteStatus=all"
    time_string = "the most recent data available"

# Multiple days in the past:
elif args.D is not None:
    api_url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites="
    api_url += args.id
    api_url += "&period=P"
    api_url += args.D
    api_url += "D&siteStatus=all"
    time_string = "data from the past " + args.D + " days"

# Multiple hours in the past:
elif args.H is not None:
    api_url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites="
    api_url += args.id
    api_url += "&period=PT"
    api_url += args.H
    api_url += "H&siteStatus=all"
    time_string = "data from the past " + args.H + " hours"

# Debug mode
if args.d == True:
    print("Scraping the following URL:")
    print(api_url)
    print("")

# Intro text
print("Retreiving current water data from USGS...")
print("")

# Grab the data
station_info = scrape_url(api_url)
station_json = station_info.json()
time_series = station_json["value"]["timeSeries"]

# Print some waves!
if args.w == True:
    print(bcolors.OKBLUE + '''\
  ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   
-'  `-'  `-'  `-'  `-'  `-'  `-'  `-'  ``-'  `-'  `-'  `-'  `-'  `-''' + bcolors.ENDC)

# Print some graphs
if args.C == True:
    print_current_data(time_series, use_fahrenheit=args.f)
elif args.r == True:
    print_series_data_raw(time_series, use_fahrenheit=args.f)
else:
    print_series_data(time_series, time_string, width=plot_width, height=plot_height, use_fahrenheit=args.f)