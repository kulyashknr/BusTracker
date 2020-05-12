import sys
import os
import utm
import math
import json
import urllib.request
import re
from . import bus
import requests
from importlib import import_module

routes = []
dell = []
l = []
bus_info = []
route = []
# bus_lt = 0
# bus_ln = 0
# station_lt = 0
# station_ln = 0

# ...............................
def stops_quantity(route,start_st,bus_lt2,bus_ln2):
	try:
		# module = import_module('stops'+str(route))
		module = 'stops'+str(route) 
		# from .stops import module
		module = import_module('stops'+str(route))
		# from . import 'stops'+str(route)
		start_index = -1
		maxi = 10000
		index = -1
		id_i = -1
		l = module.stops
	except Exception as ex:
		print("Not found")

	#по айди нашли в лсте индекс где остановку юсера
	for x in range(0, len(l)):
		if l[x][0] == start_st:
			start_index = x

	#нашли ближайшую остановку к автобусу ее индекс и расстояние. чтобы избежать противоположных 
	# остановок проверям чтобы ее следующая остановка также была ближе к юсеру

	if str(route) == '63' or  str(route) == '63А':
		for i in range(0, len(l)):
			if get_dist(l[i][1][0], l[i][1][1], bus_lt2, bus_ln2) < maxi:
				maxi = get_dist(l[i][1][0], l[i][1][1], bus_lt2, bus_ln2)
				index = i
				id_i = l[i][0]
		# print("автобус возле этой остановки "+ str(id_i))
	else: 
		for i in range(0, len(l)):
			if get_dist(l[i][1][0], l[i][1][1], bus_lt2, bus_ln2) < maxi and math.fabs(i-start_index) <= int(len(l))/2:
				maxi = get_dist(l[i][1][0], l[i][1][1], bus_lt2, bus_ln2)
				index = i
				id_i = l[i][0]
		# print("автобус возле этой остановки "+ str(id_i))

	# print("автобус возле этой остановки "+ str(id_i), index, str(start_index)+" <-start ind")
	#надо проверить ближайшую остановку автобус проехал или проедет(нужно ли брать ближайшую остановку к количеству остановок)
	#если расстояние между ближейшей к автобусу остановкой и остановкой юсера меньше чем расстояние между автобусом и остановкой юсера 

	if get_dist(l[index][1][0], l[index][1][1], l[start_index][1][0], l[start_index][1][1]) < get_dist(bus_lt2, bus_ln2, l[start_index][1][0], l[start_index][1][1]):
		quantity = math.fabs(index - start_index) #берем к количеству
	else:
		quantity = math.fabs(index - start_index)-1 #не берем
	return quantity
	l.clear()
	

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

def route_dir(bus_lt, bus_ln, station_lt, station_ln):
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
	# print(segments)
	return segments



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

def get_buses(start_id,final_id ):
	for i in jsonData:
		if int(start_id) == i["Id"]:
			#print (i["Rn"]) #все маршруты к начальной  остановке
			if i["Rn"] is None:
				# print(i["Rn"])
				continue
			x1 = re.sub(";", "", i["Rn"])
			x2 = re.sub(", ", " ", x1)
			x = re.split("\s", x2) #регуляр что бы очистить стринг подходящих маршрутов
			φ1 = i["Pt"]["Y"]
			λ1 = i["Pt"]["X"]
			station_lt = i["Pt"]["Y"]
			station_ln = i["Pt"]["X"]
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
								if int(final_id) == res['Sc']['Crs'][0]['Ss'][u]['Id']: #проверяем если ли конечная остановка в маршруте 
									φ2 = res['Sc']['Crs'][0]['Ss'][u]['Pt']['Y']
									λ2 = res ['Sc']['Crs'][0]['Ss'][u]['Pt']['X']
									print(res['R']['N'] + " ваш номер маршрута")
									m_distance = 100000
									quantity = 10000
									bus_nb = 0
									llt = -1
									lln = -1
									speed = -1
									res = requests.get(url).json()
									for i in range(len(res['V'])):
										lt, ln = utm.to_latlon(res['St'][i]['LN'], res['St'][i]['LT'], 43, zone_letter='T', northern=None, strict=True)
										line = (res['St'][i]['Id'], res['St'][i]['AZ'], res['St'][i]['SP'])#положение всех автобусов маршрута
										
										if math.fabs(find_azimut(φ1, λ1, φ2, λ2) - res['St'][i]['AZ']) <= 60:
											# print(busnum, lt, ln, start_id)
											get_route(busnum)
											# print(get_bus_number(res['St'][i]['Id'],busnum),route_dir(lt, ln, station_lt, station_ln), stops_quantity(busnum,start_id,lt, ln))
											
								
											if float(route_dir(lt, ln, station_lt, station_ln)) < m_distance and stops_quantity(busnum,start_id,lt, ln)< quantity :
												m_distance = route_dir(lt, ln, station_lt, station_ln)
												bus_nb = get_bus_number(res['St'][i]['Id'],busnum)
												quantity = stops_quantity(busnum,start_id,lt, ln)
												llt, lln = lt, ln
											else:
												continue
									# print(bus_nb,m_distance)
									bus_info.append([busnum,bus_nb, int((m_distance/30)*60+(stops_quantity(busnum,start_id,llt,lln)*2))])
									# print(bus_nb,m_distance, llt, lln)
									# if int(stops_quantity(busnum,start_id,llt,lln)) == 0:
									# 	# print("Прибывает")
									# 	bus_info.append([busnum,bus_nb,0])
									# else:
									# 	# print((m_distance/30)*60+(stops_quantity(busnum,start_id,llt,lln)*2))
									# 	bus_info.append([busnum,bus_nb,(m_distance/30)*60+(stops_quantity(busnum,start_id,llt,lln)*2)])



						# bus_info.clear()			

											# print(lt, ln, res['St'][i]['SP'])
											# print(str(line))
											# bus_info.append([busnum, [lt, ln], res['St'][i]['Id']])

						break
			routes.clear()