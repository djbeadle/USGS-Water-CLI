#!/usr/bin/env python3

# For parsing the command line arguments 
import argparse
from argparse import RawDescriptionHelpFormatter

# For formatting the command line arguments
import textwrap

# For getting the data
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

# For converting string to JSON
import json

# Get the url (specified as a command line argument)
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
    Retrieves current USGS water data so you don't have to leave your command line.
    To find a local sensor, check https://waterdata.usgs.gov/nwis/rt
    
    example: python water_info.py 11141280
    
    Depends on the wonderful python Requests library which is easily installable via pip'''
    )
)
parser.add_argument("id")
parser.add_argument("-d", help="Debug mode", required=False, action='store_true')
args = parser.parse_args()

# Build the URL we're going to get the data from
api_url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites="
api_url += args.id
api_url += "&siteStatus=all"

if args.d == True:
    print("Scraping the following URL:")
    print(api_url)
    print("")

# Functions supporting the scraping, stolen from RealPython.com!
# https://realpython.com/python-web-scraping-practical-introduction/

# Get the JSON response
def scrape_url(url):
    response = simple_get(url)

    # If we got a successful response....
    if response is not None:
        return response

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url)) as resp:
            return resp

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

# Intro text
print("Retreiving current water data from USGS...")
print("")

# Grab the data
station_info = scrape_url(api_url)
station_json = station_info.json()
time_series = station_json["value"]["timeSeries"]

# Available measurements:
i = 1
print("#  Value\t Variable")
print("-  -----\t --------")
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

    print(i, " ", current_value, "\t", variable_name+ ",", variable_type+",", site_name)
    
    i = i + 1

if i == 1:
    print("No data available for this site, perhaps you entered a bad id?")
    exit