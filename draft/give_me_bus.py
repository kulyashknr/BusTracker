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

#123
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


def get_buses(start_station, start_id):
	urlData = "https://www.citybus.kz/almaty/Monitoring/GetStops/?_=1586756337290"
	jsonData = get_response(urlData)

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
											print(str(line))


						break
			routes.clear()



start_station = input()
start_id = input()
final_station = input()
final_id = input()
get_buses(start_station, start_id)
