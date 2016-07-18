"""
   This program is designed to create an optimal flight paths between two
   potential origin and destination cities. The focus of this methodology was
   to look at optimal flight paths for routes between Atlanta and Seattle,
   using existing waypoints (described in the paper and powerpoint.)

   Creator: Karthik Kalagnanam Rao, Summer 2015, Briarcliff High School, NY
"""

import xlrd 
import networkx as nx  
from haversine import haversine 
import math

def getFlightData(flightnum, day, path):
    """
        Function: getFlightData
        -------------------
        converts the csv data created by the HTML Scrapper Tool to readable excel files:
            first sheet contains acutal flight path data
            second sheet contains waypoint data

        flightnum: name of the flight number and airlines (DAL1929)
        day: date of flight - 8 characters(yyyymmdd)
        path: location of the stored csv files and place where xlsx will be saved

        returns: name of the created xlsx 
    """
    
    from pyexcel.cookbook import merge_all_to_a_book
    import pyexcel.ext.xlsx     

    fileID = path  #path name of data

    merge_all_to_a_book([fileID+ flightnum+day+".csv",
                         fileID+flightnum+day+"waypoints"+".csv"], flightnum+day+".xlsx") # Creates excel file
    #Sheet 1: tracker points, Sheet 2: Waypoints

    return str(flightnum+day+'.xlsx')

def getWeatherData(day, month, year, path):
        """
        Function: getWeatherData
        --------------------------
        converts the 6 csv data files created by the HTML Scrapper Tool to readable excel files:
            each sheet contains wind data for respective zones
            (boston, miami, ftworth, chicago, saltlakecity, sanfrancisco)

        day: date data was collected - 2 characters (dd)
        month: month data was collected - 2 characters (mm)
        year: year data was colelcted - 4 character (yyyy)
        path: location of the stored csv files and place where xlsx will be saved

        returns: name of the created xlsx 
    """
    
    from pyexcel.cookbook import merge_all_to_a_book
    import pyexcel.ext.xlsx     #needed to support xlsx format

    zones = ['boston', 'miami', 'ftworth', 'chicago', 'saltlakecity', 'sanfrancisco'] #names for zones
    fileID = path #path for weather
    csvHeaders = [] #Lists to store files names

    for i in range(6):
        csvHeaders.append(fileID+zones[i]+str(day)+str(month)+str(now.year)+'.csv')#paths of csv files of data for each zone

    merge_all_to_a_book([csvHeaders[0], csvHeaders[1], csvHeaders[2], csvHeaders[3],
                         csvHeaders[4], csvHeaders[5]], 'weather'+ str(day) + str(month)+'.xlsx')

    return 'weather'+str(day) + str(month)+'.xlsx'


def weatherMap(day, month,year):
    """
    Function: weatherMap
    ------------------------
    creates a networkx graph of all weather points given from the AWS data files and
    makes them into nodes on the graph, parsed for alitude, speed, direction and temperature

    day: day the data was collected
    month: month the data was collected
    year: year the data was collected

    returns: networkx graph object with wind information at all stations given by the AWS in form (dir,speed,temp)
    """

    workbook = xlrd.open_workbook('weather'+str(day) + str(month)+'.xlsx')  #Opens up workbook with weather data
    airports = getAirportCodes()                            #Creates dictionary of all aiport codes
    weatherMap = nx.Graph()                                #Creates network for weather map
    helper = [26,19,41,42,32,22]                    #List with helper values to read weather.xlsx
    altitudes = ['3000', '6000', '9000', '12000', '18000', '24000', '30000', '34000', '39000']

    for i in range(6):      #Goes through each zone
        sheet = workbook.sheet_by_index(i)  
        for j in range(1, helper[i]):       #Adds each airport as a node
            weatherMap.add_node(sheet.cell_value(j,0))
            try:    #Adding latitude and longitude for airports that have it available
                weatherMap.node[sheet.cell_value(j,0)]['lat'] = airports['K'+sheet.cell_value(j,0)][0]
                weatherMap.node[sheet.cell_value(j,0)]['lon'] = airports['K'+sheet.cell_value(j,0)][1]
            except KeyError:    #Raises KeyError for points that do not exist
                weatherMap.node[sheet.cell_value(j,0)]['lat'] = 0
                weatherMap.node[sheet.cell_value(j,0)]['lon'] = 0
            for k in range(1,10):
                if k == 1 and (sheet.cell_value(j,k) != ''):
                    if(int(sheet.cell_value(j,k)[:2]) < 51):    #Adding wind speed and orientation at 3000
                        weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = (int(sheet.cell_value(j,1)[:2])*10,
                                                                  int(sheet.cell_value(j,k)[2:4]), 0)
                    elif(int(sheet.cell_value(j,k)[:2]) > 51 and int(sheet.cell_value(j,k)[:2]) < 86):
                        weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = ((int(sheet.cell_value(j,k)[:2])-50)*10,
                                                                  int(sheet.cell_value(j,k)[2:4])+100, 0)
                    elif(int(sheet.cell_value(j,k)[:2]) > 86):
                        weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = (0,0,0)
                if (k == 2 or k==3 or k==4 or k==5 or k==6) and (
                                    sheet.cell_value(j,k) != '') and len(sheet.cell_value(j,k))>4:  #Adding wind speed and orientation at 6000-24000
                    if(int(sheet.cell_value(j,k)[:2]) < 51):    #Checks to see if wind speed is below 100
                        #print i, j, k
                        if(sheet.cell_value(j,k)[4] == '-'):    #Checks to see if temp if postive/negative
                            weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = (int(sheet.cell_value(j,k)[:2])*10,
                                                                  int(sheet.cell_value(j,k)[2:4]), -1*int(sheet.cell_value(j,k)[5:7]))
                        elif(sheet.cell_value(j,k)[4] == '+'):
                             weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = (int(sheet.cell_value(j,k)[:2])*10,
                                                                  int(sheet.cell_value(j,k)[2:4]), int(sheet.cell_value(j,k)[5:7]))
                    elif(int(sheet.cell_value(j,k)[:2]) > 51 and int(sheet.cell_value(j,k)[:2]) < 86):  #Checks to see if wind speed is above 100
                        if(sheet.cell_value(j,k)[4] == '-'):
                            weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = ((int(sheet.cell_value(j,k)[:2])-50)*10,
                                                                  int(sheet.cell_value(j,k)[2:4])+100, -1*int(sheet.cell_value(j,k)[5:7]))
                        elif(sheet.cell_value(j,k)[4] == '+'):
                            weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = ((int(sheet.cell_value(j,k)[:2])-50)*10,
                                                                  int(sheet.cell_value(j,k)[2:4])+100, int(sheet.cell_value(j,k)[5:7]))
                    elif(int(sheet.cell_value(j,k)[:2]) > 86):
                        weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = (0,0,0)
                if k == 7 or k== 8 or k == 9:       #Adding wind speed and orientation at 30000-39000
                    if(int(sheet.cell_value(j,k)[:2]) < 51):
                        weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = (int(sheet.cell_value(j,k)[:2])*10,
                                                                  int(sheet.cell_value(j,k)[2:4])*1.15078, -1*int(sheet.cell_value(j,k)[5:7]))
                    elif(int(sheet.cell_value(j,k)[:2]) > 51 and int(sheet.cell_value(j,k)[:2]) < 86):
                        weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = ((int(sheet.cell_value(j,k)[:2])-50)*10,
                                                                  (int(sheet.cell_value(j,k)[2:4])+100)*1.15078, int(sheet.cell_value(j,k)[5:7]))
                    elif(int(sheet.cell_value(j,k)[:2]) > 86):
                        weatherMap.node[sheet.cell_value(j,0)][altitudes[k-1]] = (0,0,0)

    return weatherMap


def getAirportCodes(path):
    """
    Function: getAirportCodes
    ----------------------------
    reads excel file with all airport codes and creates a dictionary that include airport code and geographic coordinates

    path: location of the global_airports.xlsx document

    returns: dictionary with all airport codes and geopgraphic coordinates
    """
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    airports = {}       #Dictionary of all the airports

    for i in range(1,6977):     #Goes through all airports
        if sheet.cell_value(i,5) != '':
            airports[sheet.cell_value(i,5)] =  float(sheet.cell_value(i,6)), float(sheet.cell_value(i,7)) #Adds lat and long

    return airports

def waypointDict(files):
    """
    Function waypointDict
    ---------------------------
    creates a file that has waypoint data for a list of all entered flights
    
    files: list with tags for paths of xlsx files formatted in the way shown getFlightData

    returns: a dictionary with all waypoints with name of waypoint as key and lat and lon tuple as data
    """
    import xlrd

    waypoints = {}      #Dictionary for all waypoints

    for i in range(len(files)): #Appends each waypoint to the dictionary
        workbook = xlrd.open_workbook(files[i])
        sheet = workbook.sheet_by_index(1)
        for i in range(2, int(sheet.cell_value(0,0))):  
            waypoints[sheet.cell_value(i,0)] = (float(sheet.cell_value(i,1))
                                                , float(sheet.cell_value(i,2)))

    return waypoints

def zones(files):
    """
    Function: zones
    --------------------
    creates geographic zones for the ATL-SEA flight using geographical considerations

    files: list with tags for paths of xlsx files formatted in the way shown getFlightData (used for waypointDict function)

    returns: a list with all the waypoints within each geographic zone for the ATL-SEA flight
    """
    waypoints = waypointDict(files)      #Dictionary of waypoints
    zone = [[], [], [], [], [], []]     #Lists for each zone

    for i in range(len(waypoints)):     #Iterate through all the zones and put them into each zone
        if waypoints[waypoints.keys()[i]][1] > -87.5 and waypoints.keys()[i] != 'source':       #adding for zone 1
            zone[0].append(waypoints.keys()[i])
        if waypoints[waypoints.keys()[i]][1] > -97.6 and waypoints[waypoints.keys()[i]][1] <= -93.3341667 and waypoints[
                        waypoints.keys()[i]][0]<40 and waypoints.keys()[i] != 'source':   #adding for zone 2
            zone[1].append(waypoints.keys()[i])
        if waypoints[waypoints.keys()[i]][1] > -93.3341667 and waypoints[waypoints.keys()[i]][1] <= -87.7625: #adding for zone 2
            zone[1].append(waypoints.keys()[i])
        if waypoints[waypoints.keys()[i]][1] > -101.7 and waypoints[waypoints.keys()[i]][1] <= -98.2356: #adding for zone 3
            zone[2].append(waypoints.keys()[i])
        if waypoints.keys()[i]=='LNK' or waypoints.keys()[i]=='PWE' or waypoints.keys()[i]=='OVR' or waypoints.keys(
                                    )[i]=='DSM' or waypoints.keys()[i]=='FOD': #adding for zone 3
            zone[2].append(waypoints.keys()[i])
        if waypoints[waypoints.keys()[i]][1] >= -110.1091667 and waypoints[waypoints.keys()[i]][1
                                ] <= -101.7150714 and waypoints[waypoints.keys()[i]][0] < 45.1: #adding for zone 4
            zone[3].append(waypoints.keys()[i])
        if waypoints[waypoints.keys()[i]][1] >= -114.0841667 and waypoints[waypoints.keys()[i]][1] <= -110.3355556: #adding for zone 5
            zone[4].append(waypoints.keys()[i])
        if waypoints.keys()[i] == 'BIL' or waypoints.keys()[i] == 'MLS' or waypoints.keys()[i] == 'LWT': #adding for zone 5
            zone[4].append(waypoints.keys()[i])
        if waypoints[waypoints.keys()[i]][1] <= -115.6460556 and waypoints.keys()[i] != 'sink':
            zone[5].append(waypoints.keys()[i])     #adding for zone 6

    return zone

def predictionPoints(day, month,year,files):
    """
    Function predictionPoints
    ------------------------------
    creates a list with all points along all edges that need interpolated wind data through the Gaussian Process Regression

    day: day the data was collected
    month: month the data was collected
    year: year the data was collected
    files: list with tags for paths of xlsx files formatted in the way shown getFlightData

    returns: list of all prediction points y*
    """
    import geopy
    from geopy.distance import VincentyDistance

    zone = zones()  #create zones
    waypoint = waypointDict(files) #get the waypoint dict of all waypoints
    weather = weatherMap(day,month,year)
    y* = [] #points along paths where wind speed is needed
    network = nx.DiGraph()

    for i in range(len(zone) - 1):  #Creates the edges from layer to layer in bipartite graph
        for j in range(len(zone[i])):
            for k in range(len(zone[i+1])):
                network.add_edge(zone[i][j], zone[i+1][k],  #Adds edges from one zone to another with distance as attribute
                                 distance = haversine((waypoint[zone[i][j]]), (waypoint[zone[i+1][k]]))/1.60934)
    for i in range(len(zone[0])):
        network.add_edge('source', zone[0][i], distance = haversine(waypoint['source'], waypoint[zone[0][i]])/1.60934)
    for i in range(len(zone[5])):
        network.add_edge(zone[5][i], 'sink', distance = haversine(waypoint[zone[5][i]], waypoint['sink'])/1.60934)


    for i in range(network.number_of_edges()):#Goes through each edge to find intervals to calculate weather data
        b = bearing((waypoint[network.edges()[i][0]]), (waypoint[network.edges()[i][1]]))   #bearing of the edge
        origin = geopy.Point(waypoint[network.edges()[i][0]][0], waypoint[network.edges()[i][0]][1])#lat,lon of point 1
        network[network.edges()[i][0]][network.edges()[i][1]]['speed'] = 0
        for j in range(0, int(round_down(network[network.edges()[i][0]][network.edges()[i][1]]['distance'],20)),20):
            destination = VincentyDistance(kilometers=j).destination(origin, b) #geopy to calculate lat lon after 20miles
            b_final = (bearing((destination.latitude, destination.longitude), (waypoint[network.edges()[i][0]][0], waypoint[network.edges()[i][0]][1]))+180)%360
            y*.append[(desintination.latitude, destination.longitude)]

     

    return y*

def GP(day,month,year,files):
    """
    Function GP
    -----------------
    takes the known weather points and prediction points and calculates the direction and speed using a Gaussian Process Regression

    day: day the data was collected
    month: month the data was collected
    year: year the data was collected
    files: list with tags for paths of xlsx files formatted in the way shown getFlightData

    returns: list of predicted direction and wind
    """
    import numpy
    import GPy

    y* = predictionPoints(day,month,year,files)
    weather = weatherMap(day,month,year)
    
    X = numpy.zeros((weather.number_of_nodes(),2))
    y = numpy.zeros((weather.number_of_nodes(),1))
    z = numpy.zeros((len(y*),2))
    zdir = numpy.zeros((len(y*),1))
    zspeed = numpy.zeros((len(y*),1))

    #Regression for Wind Direction
    for i in range(28283):
        z[i][0] = y*[i][0]
        z[i][1] = y*[i][0]
    
    for i in range(176):
        X[i][0] = weather.node[weather.nodes()[i]]['lat']   #lat of known weather points
        X[i][1] = weather.node[weather.nodes()[i]]['lon']   #lon of known weather points
        y[i][0] = weahter.node[weather.nodes()[i]]['30000'][0] #direction at known weather points
        
    ker = GPy.kern.Matern52(2,ARD=True) + GPy.kern.White(2) #kernel for GP Regression
    m = GPy.models.GPRegression(X,y,ker)
    
    m.optimize(messages = False, max_f_eval = 100000)
    zdir = m.predict(z)
    
    #Regression for Wind Speed 
    for i in range(176):
        y[i][0] = weather.node[weather.nodes()[i]]['30000'][1]
     
    m = GPy.models.GPRegression(X,y,ker)
     
    m.optimize(messages = False, max_f_eval = 50000)
    zspeed = m.predict(z)
    
    return [zdir,zspeed]


def bearing(pointA, pointB):
    """
    Function bearing
    -------------------
    Calculates the bearing between two points.The formulae used is the following:
    θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

      pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

   returns: the degree in bearings (float)
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def bipartite(day, month,year,files):
    """
    Function bipartite
    ---------------------
    Creates a bipartite graph with edges across all possible combinations of waypoints through the zones.
    Each edge has an attribute of speed(average speed across the edge based on wind) and time (speed/distance)

    day: day the data was collected
    month: month the data was collected
    year: year the data was collected
    files: list with tags for paths of xlsx files formatted in the way shown getFlightData

    returns: a bipartite graph with edges between zones that have the attributes of speed and time (networkx graph)
    """
    
    import geopy
    from geopy.distance import VincentyDistance


    zone = zones()  #create zones
    waypoint = waypointDict(files) #get the waypoint dict of all waypoints
    zdir = GP(day,month,year)[0] #predicted wind directions across all prediction points
    zspeed = GP(day,month,year)[0]#predicted wind speed across all prediction points
    network = nx.DiGraph()

    for i in range(len(zone) - 1):  #Creates the edges from layer to layer in bipartite graph
        for j in range(len(zone[i])):
            for k in range(len(zone[i+1])):
                network.add_edge(zone[i][j], zone[i+1][k],  #Adds edges from one zone to another with distance as attribute
                                 distance = haversine((waypoint[zone[i][j]]), (waypoint[zone[i+1][k]]))/1.60934)
    for i in range(len(zone[0])):
        network.add_edge('source', zone[0][i], distance = haversine(waypoint['source'], waypoint[zone[0][i]])/1.60934)
    for i in range(len(zone[5])):
        network.add_edge(zone[5][i], 'sink', distance = haversine(waypoint[zone[5][i]], waypoint['sink'])/1.60934)

    p = 0 #placeholder for iterating through zdir and zspeed lists
    for i in range(network.number_of_edges()):#Goes through each edge to find intervals to calculate weather data
        b = bearing((waypoint[network.edges()[i][0]]), (waypoint[network.edges()[i][1]]))   #bearing of the edge
        origin = geopy.Point(waypoint[network.edges()[i][0]][0], waypoint[network.edges()[i][0]][1])#lat,lon of point 1
        network[network.edges()[i][0]][network.edges()[i][1]]['speed'] = 0
        k = 0 #placeholder to find total number of iteration points along each edge
        for j in range(0, int(roundDown(network[network.edges()[i][0]][network.edges()[i][1]]['distance'],20)),20):
            destination = VincentyDistance(kilometers=j).destination(origin, b) #geopy to calculate lat lon after 20miles
            b_final = (bearing((destination.latitude, destination.longitude), (waypoint[network.edges()[i][0]][0], waypoint[network.edges()[i][0]][1]))+180)%360
            network[network.edges()[i][0]][network.edges()[i][1]]['speed'] += speed_calc(destination.latitude, destination.longitude, b_final, zdir[p],zpeed[p])
            k+=1
            p+=1
        network[network.edges()[i][0]][network.edges()[i][1]]['speed'] /= k #average speed across each edge
        network[network.edges()[i][0]][network.edges()[i][1]]['time'] = network[network.edges()[i][0]][network.edges()[i][1]]['distance']/
                                                                                        network[network.edges()[i][0]][network.edges()[i][1]]['speed'] #time across each edge
                                                                                        
    return network

def roundDown(num, divisor):
    """
    Function roundDown
    ----------------------
    finds the nearest multiple lower than the given number

    num: number you are looking to round
    divisor: factor you arre looking to round with

    returns: nearest number lower than the given num and is divisible by divisor
    """
    return num - (num%divisor)

def speed_calc(lat, lon, brng, zdir,zspeed):
    """
    Function speed_calc
    ------------------------
    calculates mock speed based on wind velocity at any given point using vector arithmetic

    lat: latitude of airplane
    lon: longitutde of airplane
    brng: bearing of airplane at that point
    zdir: wind direction at that point
    zspeed: wind speed at that point

    returns: recalculated speed based on the effects of wind
    """
    airplane_speed = 597.547534896 #optimal speed in knots for airplane
    wind_speed = zspeed
    wind_direction = zdir

    x_comp = ((airplane_speed*math.sin(brng)+wind_speed*math.sin(wind_direction)))
    y_comp = ((airplane_speed*math.cos(brng)+wind_speed*math.cos(wind_direction)))

    speed = (x_comp**2 + y_comp**2)**.5

    return speed

def shortest_path(day, month,year,files):
    """
    Function shortest_path
    -------------------------
    Finds shortest path through the network on any given day based on time

    day: day the data was collected
    month: month the data was collected
    year: year the data was collected
    files: list with tags for paths of xlsx files formatted in the way shown getFlightData

    returns: network of nodes with the shortest time between orgin and destination (attributes = waypoints and time)
    """
    network = bipartite(day,month,year,files)
    zone = zones(files)
    linear_path = nx.DiGraph()
    time_placeholder = 1000

    for i in range(len(zone)):
        linear_path.add_node(i)

    for i in range(len(zone)-1):
        for j in range(len(zone[i])):
            for k in range(len(zone[i+1])):
                if network[zone[i][j]][zone[i+1][k]]['fuel'] < time_placeholder:
                    linear_path.add_edge(zone[i][j], zone[i+1][k], fuel  = network[zone[i][j]][zone[i+1][k]]['fuel'], o = zone[i][j], zone[i+1][k])

    return linear_path
                    
                   

    
