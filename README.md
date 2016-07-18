# FlightPathOptimization

This program is designed to create an optimal flight paths between two potential origin and destination cities. The focus of this methodology was to look at optimal flight paths for routes between Atlanta and Seattle, using existing waypoints. More details can be found by reading my paper FlightPathOptimization.pdf.
_____________________________________________________________________________________________________________________________

##Metholodgy Overview

In this project we seek to examine flight paths between two airports and to create an effective and optimal route between the two cities. We examine paths between the cities of Atlanta and Seattle because of their geographic locations; the route is an east-west and north- south flight. In this project, we implement a shortest path algorithm to model fuel consumption along the different possible routes available between the two cities. The solution approach is modeled as follows:


1) For a given O-D pair, we first identify the feasible waypoints using historical data. (FlightData.m contains the necessary functions used to collect such data from FlightAware using an HTML Web Scraper Tool)

2) We introduce arcs between the waypoints to get a network that represents all possible routes between the O-D pair. (Using the bipartite function in FlightPathMain.py)

3) We need to associate the travel time for each arc (weather.m collects the data, getWeatherData function will process the weather data, and weatherMap function will design a graph that contains weather info at specificed weather centers across the US). 

4) In order to do this we (a) first calculate the wind velocity at each point along the arc using interpolation techniques for wind data (GP function) and (b) calculate the travel time given the wind velocity, assuming a constant optimal cruising speed for the plane (speed_calc function in FlightPathMain.py).

5) We solve the network for shortest travel time to identify the optimal flight path. This flight path minimizes fuel usage since ground speed is assumed constant (hence fuel consumption rate is held constant.) Therefore, shortest travel time yields a fuel-optimal route (shortest_path function in FlightPathMain.py).


The methodology can be broken down into three sections: Data Collection; Model for Wind Interpolation and Application of a Shortest Path Algorithm. The methods proposed in this project were coded in python for the analysis and matlab for data collection.

_____________________________________________________________________________________________________________________________

##Packages/Files Needed 

* Python 2.7
* Matlab 13a
* xlrd (excel reader) 
* networkx (graph theory operations)
* haversine (lat and lon operations)
* pyexcel.cookbook (converts csv file to excel file)
* global_airports.xlsx (global airports lat and lon)
* getTableFromWeb_mod (Matlab HTML Table Reader)
* getHTMLTableData (Matlab HTML Table Reader)

_____________________________________________________________________________________________________________________________

## Getting Started

1. Install the programs and packages listed above (I personally use IDLE for all python implmentations)
2. Use the FlightData.m file to enter the FlightAware web address of tracker for the flight. A sample link is shown below. *
3. Use the weather.m file to scrape data from the US Aviation Weather Center website. **
4. FlightPathMain.py provides a variety of functions used to help create and design a shortest path for fuel between origin and destination 

- *http://flightaware.com/live/flight/DAL2815/history/20160718/0629Z/KSEA/KATL/tracklog 
- **Sample Data is provided (both already converted to excel files) for weather data on August 3rd, 2015 and flight data on July 31st, 2015
- For both weather.m and FlightData.m, the file paths have been hard-coded because I used this code 1000's of time over the course of the project. A comment has been included to indicate where you must change the path ID. 
