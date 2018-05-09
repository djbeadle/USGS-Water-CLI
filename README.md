Do you need to see plots of USGS water data in your command line? Probably not! But now you can.

[https://danielbeadle.net/blog/post/2018-04-01-usgs-water-cli/](https://danielbeadle.net/blog/post/2018-04-01-usgs-water-cli/)


Now has the ability to graph data- [in your terminal](https://github.com/imh/hipsterplot)!

Each measurement is specified by a 5 digit code. By default all measurements are displayed, but if you only want to display a specific measurement you can specify the code. You can look up the codes on the [USGS codes and parameters webpage](https://help.waterdata.usgs.gov/codes-and-parameters/parameters).

~~~bash
usage: water_info.py [-h] [-d] [-w] [-r] [-x X] [-y Y] [-s S] [-f]
                     (-C | -D D | -H H)
                     id

Retrieves current USGS water data so you don't have to leave your command line!
To find a local sensor, check https://waterdata.usgs.gov/nwis/rt

python3 water_info.py 11141280 -H 24
    Data for the past 24 hours

python3 water_info.py 01453000 -D 7
    Data for the past 7 days

python3 water_info.py 04288295 -C
    Only displays the most recent data point available

python3 water_info.py 01428750 -D 7
    This station has a temperature sensor, which is neat!

python3 water_info.py 01428750 -D 1 -s 00060,00010
    Only display the specified measurements

If -x & -y values are not specified, the default graph dimensions are 70 x 15

By default this displays all the different measurements available. To specify
which measurements to display (if available), look up the parameter codes at:
https://help.waterdata.usgs.gov/codes-and-parameters/parameters
and pass them as arguments to -s

positional arguments:
  id

optional arguments:
  -h, --help  show this help message and exit
  -d          Debug mode, prints out url being queried
  -w          Print waves
  -r          Output the raw data only
  -x X        Specify the width of the graph
  -y Y        Specify the height of the graph
  -s S        Display only certain paramater codes. Specify multiple as comma
              seperated values with no space. By default all available
              readings are displayed
  -f          Display temperature in Fahreneheit
  -C          Current data only
  -D D        Specify the number of days you want data for
  -H H        Specify the number of past hours you want data for
  ~~~

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/djbeadle/41941646642/in/dateposted/" title="temp"><img src="https://farm1.staticflickr.com/952/41941646642_d74c44fe68.jpg" width="459" height="500" alt="temp">