import bus127
import requests
import math
import utm

route = []

def get_dist(lt1, ln1, lt2,ln2):
	R = 6373.0
	lat1 = math.radians(lt1)
	lon1 = math.radians(ln1)
	lat2 = math.radians(lt2)
	lon2 = math.radians(ln2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	distance = R * c

	return distance

def get_route():
	for busurl in bus127.buses:
		url = bus127.buses[busurl]
		res = requests.get(url).json()
		points = res['Sc']['Crs'][0]['Ps']
		for point in points:
			route.append([point['Y'], point['X']])
		# print(route)
# 	stations = res['Sc']['Crs'][0]['Ss']
# 	for station in stations:
# 		# print(station['Pt']['Y'])
# 		station_point.append([station['Pt']['X'], station['Pt']['Y']])

bus_lt, bus_ln = utm.to_latlon(658048, 4790628, 43, zone_letter='T', northern=None, strict=True)
station_lt, station_ln = 43.26525, 76.948869
print(bus_lt, bus_ln)

get_route()

def route_dir():
	dist_list = [] 
	clockwise = True
	segments = 0
	# расстояние до автобуса всех точек
	for i in range(0,len(route)):
		dist_list.append(get_dist(route[i][0], route[i][1], bus_lt, bus_ln))
		# print(get_dist(route[i][0], route[i][1], bus_lt, bus_ln))
	
	# print(bus_lt, bus_ln, route[150][0], route[150][1], get_dist(route[150][0], route[150][1], bus_lt, bus_ln))

	min_value = dist_list[0]
	min_index = 0

	# из всех расстояний найти ближаюшую точку к автобусу
	for i in range(0, len(dist_list)):
		if dist_list[i] < min_value:
			min_value = dist_list[i]
			min_index = i
	# print(min_index)
	# определить направление (от ближайшей точки)
	# try:
	# 	if get_dist(route[min_index - 1][0], route[min_index - 1][1], station_lt, station_ln) > get_dist(route[min_index + 1][0], route[min_index + 1][1], station_lt, station_ln):
	# 		clockwise = True
	# except IndexError as e:
	# 	raise
	# print(get_dist(route[min_index - 1][0], route[min_index - 1][1], station_lt, station_ln),get_dist(route[min_index + 1][0], route[min_index + 1][1], station_lt, station_ln))

	# расстояние от остановки до точек (все точки до ближайшей к автобусу)
	station_closepoint_index = 0
	station_dist = []

	# if clockwise is True:
	for i in range(0, len(route)):
		station_dist.append(get_dist(route[i][0], route[i][1], station_lt, station_ln))
		# print(get_dist(route[i][0], route[i][1], station_lt, station_ln))

	min_value_st = station_dist[0]
	min_index_st = 0

	# из расстояний от ближайшей точки к автобусу найти ближаюшую точку до остановки (последняя точка до прибытия к остановке)
	for i in range(min_index, len(station_dist)):
		if station_dist[i] < min_value_st:
			min_value_st = station_dist[i]
			min_index_st = i
	# print(min_index_st, min_value_st)

	# сумма расстояний отрезков от ближайшей точки
	for i in range(min_index, min_index_st - 1):
		segments += get_dist(route[i][0], route[i][1], route[i + 1][0], route[i + 1][1])
		# print(segments)

	# к сумме расстояний добавить расстояние от автобуса до ближ точки и от остановки до ее ближ точки
	segments += min_value + min_value_st
	print(segments)
route_dir()



