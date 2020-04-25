import sys
import os
import utm
import math
import json
import urllib.request
import re
import bus
import requests

routes = []
dell = []

bus_info = []
route = []
bus_lt = 0
bus_ln = 0
station_lt = 0
station_ln = 0

# ..................................
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

def get_route(route_num):
	route.clear()
	for busurl in bus.buses:
		if str(busurl) == str(route_num):
			url = bus.buses[busurl]
			res = requests.get(url).json()
			points = res['Sc']['Crs'][0]['Ps']
			for point in points:
				route.append([point['Y'], point['X']])

def route_dir():
	dist_list = [] 
	segments = 0
	# расстояние до автобуса всех точек
	for i in range(0, len(route)):
		dist_list.append(get_dist(route[i][0], route[i][1], bus_lt, bus_ln))
		# print(get_dist(route[i][0], route[i][1], bus_lt, bus_ln))
	
	min_value = dist_list[0]
	min_index = 0

	# из всех расстояний найти ближаюшую точку к автобусу
	# print(get_dist(route[4][0], route[4][1], bus_lt, bus_ln))

	# print(route[4],bus_lt, bus_ln)
	for i in range(0, len(dist_list)):
		if dist_list[i] < min_value:
			min_value = dist_list[i]
			min_index = i
			
	# print('end ///////////////////////////////////////')
	
	# определить направление (от ближайшей точки)
	# от ближайшей точки к автобусу проверить соседнии точки к остановке и ее саму. Для определения направления. i-1, i, i+1
	try:
		i1 = get_dist(route[min_index - 1][0], route[min_index - 1][1], station_lt, station_ln)
		i2 = get_dist(route[min_index][0], route[min_index][1], station_lt, station_ln)
		i3 = get_dist(route[min_index + 1][0], route[min_index + 1][1], station_lt, station_ln)
	except IndexError as e:
		raise

	if (i1 < i2) and (i1 < i3):
		min_index -= 1
	elif (i3 < i1) and (i3 < i2):
		min_index += 1
	min_value = get_dist(route[min_index][0], route[min_index][1], bus_lt, bus_ln)




	# расстояние от остановки до точек (все точки до ближайшей к автобусу)
	station_dist = []

	for i in range(0, len(route)):
		station_dist.append(get_dist(route[i][0], route[i][1], station_lt, station_ln))
		# print(get_dist(route[i][0], route[i][1], station_lt, station_ln))

	min_value_st = station_dist[0]
	min_index_st = 0
	# print('start ///////////////////////////////////////')

	# из всех расстояний от ближайшей точки к автобусу найти ближаюшую точку до остановки (последняя точка до прибытия к остановке)
	for i in range(0, len(station_dist)):
		# print(station_dist[i], min_value_st, min_index_st)
		if station_dist[i] < min_value_st:
			min_value_st = station_dist[i]
			min_index_st = i
	# print(min_index_st, min_value_st)

	# определить направление (от ближайшей точки)
	# от ближайшей точки к остановке проверить соседние точки к остановке. Для определения направления. i-1, i, i+1
	try:
		j1 = get_dist(route[min_index_st - 1][0], route[min_index_st - 1][1], bus_lt, bus_ln)
		j2 = get_dist(route[min_index_st][0], route[min_index_st][1], bus_lt, bus_ln)
		j3 = get_dist(route[min_index_st + 1][0], route[min_index_st + 1][1], bus_lt, bus_ln)
	except IndexError as e:
		raise

	if (j1 < j2) and (j1 < j3):
		min_index_st -= 1
	elif (j3 < j1) and (j3 < j2):
		min_index_st += 1
	min_value_st = get_dist(route[min_index_st][0], route[min_index_st][1], station_lt, station_ln)
	# print(min_index_st, min_value_st)



	# сумма расстояний отрезков от ближайшей точки к автобусу
	# ифы для по часовой и против
	if min_index < min_index_st:
		for i in range(min_index, min_index_st - 1):
			segments += get_dist(route[i][0], route[i][1], route[i + 1][0], route[i + 1][1])
	else:
		for i in range(min_index_st, min_index - 1):
			segments += get_dist(route[i][0], route[i][1], route[i + 1][0], route[i + 1][1])
			 # print(segments)

	# к сумме расстояний добавить расстояние от автобуса до ближ точки и от остановки до ее ближ точки
	segments += min_value + min_value_st
	# print(segments, bus_lt, bus_ln, min_value, min_value_st, min_index, min_index_st, j1,j2,j3)
	print(segments)



# ...............................


def find_azimut(φ1, λ1, φ2, λ2):
    #λ1 = 76.949642
    #φ1 = 43.232319
    # φ2 = 43.232319
    # λ2 = 76.949642
    y = math.sin(λ2-λ1) * math.cos(φ2);
    x = math.cos(φ1)*math.sin(φ2) -math.sin(φ1)*math.cos(φ2)*math.cos(λ2-λ1);
    brng = math.atan2(y, x)
    return ((180/math.pi)*brng+360)%360

def get_bus_number(busId, bnumber):
	for busnum in bus.buses:
		if bnumber == busnum:
			url = bus.buses[busnum]
			try:
				res = requests.get(url).json()
			except Exception as ex:
				print('URL ' + "27",busnum, ex)
				dell.append(busnum)
				continue
			else:
				res = requests.get(url).json()
				for i in range(len(res['V'])):
					if res['V'][i]['Id'] == busId:
						return res['V'][i]['Nm']

def get_response(url):
	operUrl = urllib.request.urlopen(url)

	if (operUrl.getcode() == 200):
		data = operUrl.read()
		jsonData = json.loads(data)
	else:
		print("Error receiving data", operUrl.getcode())
	return jsonData

urlData = "https://www.citybus.kz/almaty/Monitoring/GetStops/?_=1586756337290"
jsonData = get_response(urlData)

def get_buses(start_station, start_id):
	for i in jsonData:
		if (start_station.lower() in i["Nm"].lower()) and (int(start_id) == i["Id"]):
			#print (i["Rn"]) #все маршруты к начальной  остановке
			if i["Rn"] is None:
				# print(i["Rn"])
				continue
			x1 = re.sub(";", "", i["Rn"])
			x2 = re.sub(", ", " ", x1)
			x = re.split("\s", x2) #регуляр что бы очистить стринг подходящих маршрутов
			φ1 = i["Pt"]["Y"]
			λ1 = i["Pt"]["X"]
			for i in range(1,len(x)-1):
				routes.append(x[i])
			for route in routes:
				for busnum in bus.buses:
					if str(busnum) == route: 
						url = bus.buses[busnum] #в файле bus.py берем нужную ссылку на маршрут 
						try:
							res = requests.get(url).json()
						except Exception as ex:
							print('URL ',busnum, ex)
							dell.append(busnum)
							continue
						else:
							res = requests.get(url).json()
							for u in range(len(res['Sc']['Crs'][0]['Ss'])):
								if (final_station.lower() in res['Sc']['Crs'][0]['Ss'][u]['Nm'].lower()) and (int(final_id) == res['Sc']['Crs'][0]['Ss'][u]['Id']): #проверяем если ли конечная остановка в маршруте 
									φ2 = res['Sc']['Crs'][0]['Ss'][u]['Pt']['Y']
									λ2 = res ['Sc']['Crs'][0]['Ss'][u]['Pt']['X']
									print(res['R']['N'] + " ваш номер маршрута")
									res = requests.get(url).json()
									for i in range(len(res['V'])):
										lt, ln = utm.to_latlon(res['St'][i]['LN'], res['St'][i]['LT'], 43, zone_letter='T', northern=None, strict=True)
										line = (res['St'][i]['Id'], res['St'][i]['AZ'], res['St'][i]['SP'])#положение всех автобусов маршрута
										# print(str(line))
										# print(str(lt) +" " +str(ln) + '\n')
										#print(str(find_azimut(lt, ln)) + " Azimut" +'\n')
										#find_azimut(φ1, λ1, φ2, λ2)
										if math.fabs(find_azimut(φ1, λ1, φ2, λ2) - res['St'][i]['AZ']) <= 60:
											print(get_bus_number(res['St'][i]['Id'],busnum))
											print(lt, ln, res['St'][i]['SP'])
											print(str(line))
											bus_info.append([busnum, [lt, ln], res['St'][i]['Id']])
						break
			routes.clear()



start_station = 'esentai'
start_id = 367
final_station = 'карасай батыра'
final_id = 122
get_buses(start_station, start_id)
# print(bus_info)
for station in jsonData:
		if (start_station.lower() in station["Nm"].lower()) and (int(start_id) == station["Id"]):
			station_lt = station["Pt"]["Y"]
			station_ln = station["Pt"]["X"]
for i in range(0, len(bus_info)):
	get_route(bus_info[i][0])
	bus_lt, bus_ln = bus_info[i][1]
	route_dir()









