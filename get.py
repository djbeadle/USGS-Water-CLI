# For parsing the command line arguments 
import argparse

# For parsing the HTML
from bs4 import BeautifulSoup

# For getting the HTML
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

# For converting string to JSON
import json

# Get the url (specified as a command line argument)
parser = argparse.ArgumentParser()
parser.add_argument("id")
args = parser.parse_args()

# Build the URL we're going to get the data from
api_url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites="
api_url += args.id
api_url += "&parameterCd=00060,00065,00010&siteStatus=all"

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

# The actual code that runs:
station_info = scrape_url(api_url)
station_json = station_info.json()
time_series = station_json["value"]["timeSeries"]

print(station_info)
print("")
print(time_series[0])

for i in time_series:
    print(time_series.gets(i))
    print("")