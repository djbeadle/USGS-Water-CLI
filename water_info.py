#!/usr/bin/env python3

# For parsing the command line arguments 
import argparse
from argparse import RawDescriptionHelpFormatter

# For graphing in the command line!
# Honestly this is pretty ridiclious
import hipsterplot

# For formatting the command line arguments
import textwrap

# For getting the data
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

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
        python water_info.py 11141280 -H 24
        python water_info.py 11141280 -D 7
        python water_info.py 11141280 -C
    
    Depends on the wonderful python Requests library which is easily installable via pip'''
    )
)
parser.add_argument("id")
parser.add_argument("-d", help="Debug mode, prints out url being queried", required=False, action='store_true')
parser.add_argument("-n", help="No waves", required=False, action='store_true')
parser.add_argument("-r", help="Output the raw data only", required=False, action='store_true')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-C", help="Current data only", required=False, action='store_true')
group.add_argument("-D", help="Specify the number of days you want data for", required=False)
group.add_argument("-H", help="Specify the number of past hours you want data for", required=False)

args = parser.parse_args()

if args.r == True:
    args.n = True

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

# Get the JSON
def scrape_url(url):
    response = simple_get(url)

    # If we got a successful response....
    if response is not None:
        return response

def simple_get(url):
    try:
        with closing(get(url)) as resp:
            return resp

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def log_error(e):
    print(e)

# Intro text
print("Retreiving current water data from USGS...")
print("")

# Grab the data
station_info = scrape_url(api_url)
station_json = station_info.json()
time_series = station_json["value"]["timeSeries"]

# Print some waves!
if args.n == False:
    print(bcolors.OKBLUE + '''\
  ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   
-'  `-'  `-'  `-'  `-'  `-'  `-'  `-'  ``-'  `-'  `-'  `-'  `-'  `-''' + bcolors.ENDC)

# Printout the data!
def print_current_data(time_series):
    i = 0
    for item in time_series:
        no_data_value = item["variable"]["noDataValue"]
        variable_type = item["variable"]["valueType"]
        site_name = item["sourceInfo"]["siteName"]
        lat = item["sourceInfo"]["geoLocation"]["geogLocation"]["latitude"]
        long = item["sourceInfo"]["geoLocation"]["geogLocation"]["longitude"]
        network = item["sourceInfo"]["siteCode"][0]["network"]
        agency_code = item["sourceInfo"]["siteCode"][0]["agencyCode"]
        current_value = item["values"][0]["value"][0]["value"]
        variable_name = item["variable"]["variableName"].replace("&#179;", " cubed")
        print(current_value, "\t", variable_name+ ",", variable_type+",", site_name)
        
        i = i + 1

    if i == 0:
        print("No data available for this site, perhaps you entered a bad id?")
        exit

# Print out a graph a time series of data
def print_series_data(time_series, time_string):
    # Each sensor records data points in different time series
    i = 0
    for series in time_series:
        # Iterate through the time stamped data points we have
        data = []
        timestamp = []

        print(series["sourceInfo"]["siteName"])
        print(series["variable"]["variableDescription"])
        print("Displaying", time_string)
        
        for point in series["values"][0]["value"]:
            data.append(float(point["value"]))
            timestamp.append(i)
            i = i+1
        
        hipsterplot.plot(data, timestamp)
        print("")

# No graphing, prints out the data in raw form. 
def print_series_data_raw(time_series):
    # Each sensor records data points in different time series
    for series in time_series:
        # Iterate through the time stamped data points we have
        print(series["variable"]["variableDescription"])
        for point in series["values"][0]["value"]:
            print(point["dateTime"] + ", " + point["value"])

print("Displaying charts for the past", args.C is not None )
if args.C == True:
    print_current_data(time_series)
elif args.r == True:
    print_series_data_raw(time_series)
else:
    print_series_data(time_series, time_string)