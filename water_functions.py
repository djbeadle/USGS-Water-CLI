# For getting the data
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

# For graphing in the command line!
# Honestly this is pretty ridiclious
import hipsterplot

# Replace:
#   superscript "3" with "cubed"
#   degree symbol with "degrees"
def clean_variable_name(text):
    text_temp = text.replace("&#179;", " cubed")
    text_temp = text_temp.replace("&#176;", "degrees ")
    return text_temp

def celsius_to_fahrenheit(value):
    return round(float(value) * (9/5) + 32, 3)

# Printout a single data point
def print_current_data(time_series, use_fahrenheit=None):
    i = 0
    for item in time_series:
        no_data_value = item["variable"]["noDataValue"]
        variable_type = item["variable"]["valueType"]
        site_name = item["sourceInfo"]["siteName"]
        lat = item["sourceInfo"]["geoLocation"]["geogLocation"]["latitude"]
        long = item["sourceInfo"]["geoLocation"]["geogLocation"]["longitude"]
        network = item["sourceInfo"]["siteCode"][0]["network"]
        agency_code = item["sourceInfo"]["siteCode"][0]["agencyCode"]
        variable_name = clean_variable_name(item["variable"]["variableName"])
        current_value = item["values"][0]["value"][0]["value"]

        if use_fahrenheit == True:
            if "degrees C" in variable_name:
                current_value = celsius_to_fahrenheit(item["values"][0]["value"][0]["value"])
                variable_name = clean_variable_name(item["variable"]["variableName"]).replace("degrees C", "degrees F")

        print(current_value, "\t", variable_name+ ",", variable_type+",", site_name)
        
        i = i + 1

    if i == 0:
        print("No data available for this site, perhaps you entered a bad id?")
        exit

# Print out a graph of time series data
def print_series_data(time_series, time_string, width=70, height=15, use_fahrenheit=None):
    # Each sensor records data points in different time series
    i = 0
    for series in time_series:
        # Iterate through the time stamped data points we have
        data = []
        timestamp = []
        
        site_name = series["sourceInfo"]["siteName"]
        variable_description = series["variable"]["variableDescription"]

        convert_to_fahr = False
        if use_fahrenheit == True:
            if "degrees Celsius" in variable_description:
              convert_to_fahr = True
              variable_description = variable_description.replace("degrees Celsius", "degrees Fahrenheit")

        print(site_name)
        print(variable_description)
        print("Displaying", time_string)

        for point in series["values"][0]["value"]:
            if convert_to_fahr == True:
                data.append(celsius_to_fahrenheit(float(point["value"])))
            else:
                data.append(float(point["value"]))
            timestamp.append(i)
            i = i + 1
            
        print('\033[94m')
        hipsterplot.plot(data, timestamp, num_x_chars=width, num_y_chars=height)
        print('\033[0m')
    
    if i == 0:
        print("No data available for this site, perhaps you entered a bad id?")
        exit

# No graphing, prints out time series data in raw form. 
def print_series_data_raw(time_series, use_fahrenheit=None):
    i = 0
    # Each sensor records data points in different time series
    for series in time_series:
        site_name = series["sourceInfo"]["siteName"]
        variable_description = series["variable"]["variableDescription"]
        
        convert_to_fahr = False
        if use_fahrenheit == True:
            if "degrees Celsius" in variable_description:
              convert_to_fahr = True
              variable_description.replace("degrees Celsius", "degrees Fahrenheit")

        # Iterate through the time stamped data points we have
        print(variable_description)
        for point in series["values"][0]["value"]:
            if convert_to_fahr == True:
                print(point["dateTime"] + ", " + str(celsius_to_fahrenheit(float(point["value"]))))
            else:
                print(point["dateTime"] + ", " + point["value"])
        i = i + 1
    
    if i == 0:
        print("No data available for this site, perhaps you entered a bad id?")
        exit

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