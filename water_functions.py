# For getting the data
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

# For graphing in the command line!
# Honestly this is pretty ridiclious
import hipsterplot

# Printout a single data point
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

# Print out a graph of time series data
def print_series_data(time_series, time_string, width=70, height=15):
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
        print('\033[94m')
        hipsterplot.plot(data, timestamp, num_x_chars=width, num_y_chars=height)
        print('\033[0m')

# No graphing, prints out time series data in raw form. 
def print_series_data_raw(time_series):
    # Each sensor records data points in different time series
    for series in time_series:
        # Iterate through the time stamped data points we have
        print(series["variable"]["variableDescription"])
        for point in series["values"][0]["value"]:
            print(point["dateTime"] + ", " + point["value"])

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