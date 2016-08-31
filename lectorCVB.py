import sys
import operator
import csv

def pyomo_postprocess(results, n, instance):
	#se define el nombre del archivo con los resultados
	tmp_name = 'resultados/sim'+str(n)+'.csv'
	#se crea el archivo para escribir resultados
	f = csv.writer(open(tmp_name, 'wb'))
	#se escriben los encabezados del archivo
	encabezados = ['Object','Type','Property','Period','Time','Value']
	f.writerow(encabezados)
#Generation
	dia = 1 #contador de dias de la semana
	auxDia = 0 #guarda la generacion del dia
	auxTot = 0 #guarda la generacion total de la central
        for gen in instance.CENTRALES:
                for hora in instance.HORAS:
			#generacion horaria
                        laux = []
                        laux.extend([gen,'Generator','Generation','Hour',hora])
                        laux.append(instance.g[gen,hora].value)
			auxDia += instance.g[gen,hora].value
                        f.writerow(laux)
			#generacion diaria
			if hora%24==0:
				laux = [gen,'Generator','Generation','Day',dia]
				laux.append(auxDia)
				auxTot += auxDia
				auxDia = 0
				dia += 1
				f.writerow(laux)
			#generacion semanal (total)
			if hora==168:
				laux = [gen,'Generator','Generation','Total',0]
				laux.append(auxTot)
				auxTot = 0
				f.writerow(laux)
				dia = 1
#Status - W
	dia = 1
	auxDia = 0
	auxTot = 0
	for gen in instance.CENTRALES:
		for hora in instance.HORAS:
			#status horario
			laux = []
			laux.extend([gen,'Generator','Status','Hour',hora])
            laux.append(instance.W[gen,hora].value)
			f.writerow(laux)
			#status diario
			if hora%24==0:
				laux = [gen,'Generator','Status','Day',dia]
				laux.append(auxDia)
				auxTot += auxDia
				auxDia = 0
				dia += 1
				f.writerow(laux)
			#status semanal (total)
			if hora==168:
				laux = [gen,'Generator','Generation','Total',0]
				laux.append(auxTot)
				auxTot = 0
				f.writerow(laux)
				dia = 1
