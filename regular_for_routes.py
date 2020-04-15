import re
import bus
import requests
string1 = "Автобусы: 37, 65, 113; "
string2 = "Автобус: 60; " #есть 3 случая несколько автобусов и 1 только автобус. Также когда их вообще нет(null)
routes = []
dell = []
x1 = re.sub(";", "", string2)
x2 = re.sub(", ", " ", x1)
x = re.split("\s", x2)
for i in range(1,len(x)-1):
	routes.append(int(x[i]))
for route in routes:
	for busnum in bus.buses:
		if busnum == route:
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
