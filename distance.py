import sys
import os
import json
import urllib.request

def get_response(url):
    operUrl = urllib.request.urlopen(url)

    if (operUrl.getcode() == 200):
        data = operUrl.read()
        jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData


def get_buses(start_station):
    urlData = "https://www.citybus.kz/almaty/Monitoring/GetStops/?_=1586756337290"
    jsonData = get_response(urlData)

    for i in jsonData:
        if start_station in i["Nm"].lower():
            print(i["Rn"])


start_station = input()
get_buses(start_station)

# files = []
# for file in os.listdir('stops'):
# 	if '.txt' in file:
# 		#print(str(file))
# 		filepath = str('stops/'+file)
# 		with open(filepath) as fp:
# 			cnt = 0
# 			for line in fp:
# 				str_line = line
# 				if start_station in str_line.lower():
# 					print(str(file.split('.')[0]))
# 				cnt += 1
# 		fp.close()

# stations = []
# buses = [] 

# class Bus(object):
# 	id = 0
#     x = 0
#     y = 0
#     dir = ""

#     def __init__(self, id, x, y, dir):
#         self.id = id
#         self.x = x
#         self.y = y
#         self.dir = dir


# class Station(object):
# 	id = 0
# 	x = 0
# 	y = 0
# 	distance_to_bus = 0

#     def __init__(self, id, x, y, distance_to_bus):
#         self.id = id
#         self.x = x
#         self.y = y
#         seld.distance_to_bus = distance_to_bus


# def find_2nearest_stations(buses, stations):
# 	for bus in buses:
# 		for station in stations:
# 			distance = math.sqrt((bus.x - station.x)**2+(bus.y - station.y)**2)
# 			station.distance_to_bus = distance

# 		min_distance_to_bus = stations[0].distance_to_bus
# 		for station in stations:
# 			if station.distance_to_bus < min_distance_to_bus:
# 				min_distance_to_bus = station.distance_to_bus
# 				1nearest_station_index = station

# 		if 1nearest_station_index == 0:
# 			if stations[1].distance_to_bus < stations[:1].distance_to_bus:
# 				2nearest_station_index = 1
# 				bus.dir = 'A'
# 			else: 
# 				2nearest_station_index = len(stations)-1
# 				bus.dir = 'B'

# 		else:
# 			if stations[1nearest_station_index+1].distance_to_bus < stations[1nearest_station_index-1].distance_to_bus:
# 				2nearest_station_index = 1nearest_station+1
# 				bus.dir = 'A'
# 			else:
# 				2nearest_station_index = 1nearest_station-1
# 				bus.dir = 'B'
