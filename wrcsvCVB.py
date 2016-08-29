import sys
import operator
import csv

def pyomo_postprocess(results, n, instance):
	#se define el nombre del archivo con los resultados
	tmp_name = 'resultados/sim'+str(n)+'.csv'
	#se crea el archivo para escribir resultados
	f = csv.writer(open(tmp_name, 'wb'))
	#se escriben los encabezados del archivo
	encabezados = ['Object','Type','Property','Time','Value']
	f.writerow(encabezados)
#Generation
        for gen in instance.CENTRALES:
                for hora in instance.HORAS:
                        laux = []
                        laux.append(gen)
                        laux.append('Generator')
                        laux.append('Generation')
                        laux.append(hora)
                        laux.append(instance.g[gen,hora].value)
                        f.writerow(laux)     
