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
		jsonData = json.loads(data)
	else:
		print("Error receiving data", operUrl.getcode())
	return jsonData


def get_buses(start_station):
	urlData = "https://www.citybus.kz/almaty/Monitoring/GetStops/?_=1586756337290"
	jsonData = get_response(urlData)

	for i in jsonData:
		if start_station in i["Nm"].lower():
			# print(i["Rn"])
			x1 = re.sub(";", "", i["Rn"])
			x2 = re.sub(", ", " ", x1)
			x = re.split("\s", x2)
			for i in range(1,len(x)-1):
				routes.append(x[i])
			for route in routes:
				for busnum in bus.buses:
					if str(busnum) == route:
						url = bus.buses[busnum]
						try:
							res = requests.get(url).json()
						except Exception as ex:
							print('URL ',busnum, ex)
							dell.append(busnum)
							continue
						else:
							print(res['R']['N'])
							res = requests.get(url).json()
							for i in range(len(res['V'])):
								line = (res['St'][i]['Id'],res['St'][i]['ST'], res['St'][i]['AZ'], res['St'][i]['LT'], res['St'][i]['LN'],res['St'][i]['SP'])#buses
								print(str(line)[1:-1]+'\n')
						break



start_station = input()
get_buses(start_station)
