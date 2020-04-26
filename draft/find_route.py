import sys
import os
import json
import urllib.request
import re
import bus
import requests

routes = []
dell = []

def get_response(url):
	operUrl = urllib.request.urlopen(url)

	if (operUrl.getcode() == 200):
		data = operUrl.read()
		jsonData = json.loads(data.decode('utf-8'))
	else:
		print("Error receiving data", operUrl.getcode())
	return jsonData


def get_buses(start_station):
	urlData = "https://www.citybus.kz/almaty/Monitoring/GetStops/?_=1586756337290"
	jsonData = get_response(urlData)

	for i in jsonData:
		if start_station.lower() in i["Nm"].lower():
			print (i["Rn"])
			if i["Rn"] is None:
				# print(i["Rn"])
				continue
			x1 = re.sub(";", "", i["Rn"])
			x2 = re.sub(", ", " ", x1)
			x = re.split("\s", x2) #регуляр что бы очистить стринг подходящих маршрутов
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
								if final_station.lower() in res['Sc']['Crs'][0]['Ss'][u]['Nm'].lower(): #проверяем если ли конечная остановка в маршруте 
									print(res['R']['N'])
									print('aaaa')
									res = requests.get(url).json()
									for i in range(len(res['V'])):
										line = (res['St'][i]['Id'],res['St'][i]['ST'], res['St'][i]['AZ'], res['St'][i]['LT'], res['St'][i]['LN'],res['St'][i]['SP'])#положение всех автобусов маршрута
										print(str(line)[1:-1]+'\n')
						break
			routes.clear()



start_station = input()
final_station = input()
get_buses(start_station)
