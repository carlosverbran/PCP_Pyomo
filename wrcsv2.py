import sys
import operator
import numpy as np
from pyomo.core import *

def pyomo_postprocess(instance, results, i):
     name = 'sol' + str(i) + '.csv'
     name_gen = 'gen'+str(i)+'.csv'
     name_vert = 'vert'+str(i)+'.csv'
     name_vol = 'vol'+str(i)+'.csv'
     name_afl = 'afl'+str(i)+'.csv'
     name_obj = 'obj' + str(i) + '.csv'
     name_phi = 'varphi'+str(i)+'.csv'
     name_lin = 'lin'+str(i)+'.csv'
     name_w = 'w'+str(i)+'.csv'
     name_y ='y'+str(i)+'.csv'
     name_z ='z'+str(i)+'.csv'
     fo = open(name,'w')
     fgen=open(name_gen,'w')
     fvert=open(name_vert,'w')
     fvol=open(name_vol,'w')
     fafl=open(name_afl,'w')
     fw=open(name_w,'w')
     fy=open(name_y,'w')
     fz=open(name_z,'w')
     fp = open(name_obj,'w')
#     fphi = open(name_phi,'w')
#     flin = open(name_lin,'w')
     gen = []
     vert = []
     afl = []
     vol = []
     W = []
     Y = []
     Z = []
     
     fluptr = {}
     flup = {}
     fluntr = {}
     flun = {}
     fluptr_ubnd = {}
     fluntr_ubnd = {}
     flup_ubnd = {}
     flun_ubnd = {}
     lineas = []
     tramos = []
     etapas = []
     varphi = {}
     fgen.write('nom, eta, value, ub, CF\n')
     fvert.write('nom, eta, value, ub, CF\n')
     fvol.write('nom, eta, value, ub\n')
     fafl.write('nom, eta, value, ub\n')
#     flin.write('nom, eta, value, ub\n')
     fw.write('nom, eta, value\n')
     fy.write('nom, eta, value\n')
     fz.write('nom, eta, value\n')

     isim = 0
     for var in instance.components(Var):
	print var
	if var == 'g':
		objv = getattr(instance, var)
		for index in objv:
			readpar = str(objv[index])
			aux = readpar.split('[')
        	     	nomvec = list(aux[1])
			vec = aux[1].split(',')
	  	        lc = len(vec)-1
                	oldstr = vec[lc]
	                eta = oldstr.replace("]","")
        	        nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                	newnomvec = "".join(nomvec)
                	sol = float(objv[index].value)
			ub = float(objv[index].ub)
			if ub == 0:
				CF = 0
			else:
				CF = sol/ub
			item = (newnomvec, eta, sol, ub, CF)
			tmp_str = newnomvec + ',' + str(eta) + ',' + str(sol) + ',' + str(ub) + ',' + str(CF) + '\n'
			fgen.write(tmp_str)
			gen.append(item)			
        if var == 'v':	     
		objv = getattr(instance, var)
		for index in objv:
                     readpar = str(objv[index])
		     aux = readpar.split('[')
                     nomvec = list(aux[1])
                     vec = aux[1].split(',')
                     lc = len(vec) - 1
                     oldstr = vec[lc]
                     eta = oldstr.replace("]","")
                     nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                     newnomvec = "".join(nomvec)
                     sol = float(objv[index].value)
                     ub = float(objv[index].ub)
                     if ub>0:
			item = (aux[0], newnomvec, eta, sol, ub, sol/ub)
			CF = sol/ub
                     else:
			item = (aux[0], newnomvec, eta, sol, ub, 0)
			CF = 0
		     tmp_str = newnomvec + ',' + str(eta) + ',' + str(sol) + ',' + str(ub) + ',' + str(CF) + '\n'
		     fvert.write(tmp_str)
		     vert.append(item)                     
        if var == 'c':
                objv = getattr(instance, var)
		for index in objv:
 		     readpar = str(objv[index])
		     aux = readpar.split('[')
                     nomvec = list(aux[1])
                     vec = aux[1].split(',')
                     lc = len(vec) - 1
                     oldstr = vec[lc]
                     eta = oldstr.replace("]","")
                     nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                     newnomvec = "".join(nomvec)
                     sol = float(objv[index].value)
		     item = (aux[0], newnomvec, eta, sol)
    	             tmp_str = newnomvec + ',' + str(eta) + ',' + str(sol) + ',' + str(ub) + '\n'
		     fvol.write(tmp_str)
		     vol.append(item)
        if var == 'afl':
                objv = getattr(instance, var)
		for index in objv:
		     readpar = str(objv[index])
		     aux = readpar.split('[')
                     nomvec = list(aux[1])
                     vec = aux[1].split(',')
                     lc = len(vec) - 1
                     oldstr = vec[lc]
                     eta = oldstr.replace("]","")
                     nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                     newnomvec = "".join(nomvec)
                     sol = float(objv[index].value)
               	     item = (aux[0], newnomvec, eta, sol)
		     tmp_str = newnomvec + ',' + str(eta) + ',' + str(sol) + ',' + str(ub) + '\n'
		     fafl.write(tmp_str)
		     afl.append(item)
        if var == 'W':	  
                objv = getattr(instance, var)
		for index in objv:
        	     readpar = str(objv[index])
		     aux = readpar.split('[')
                     nomvec = list(aux[1])
                     vec = aux[1].split(',')
                     lc = len(vec) - 1
                     oldstr = vec[lc]
                     eta = oldstr.replace("]","")
                     nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                     newnomvec = "".join(nomvec)
                     sol = objv[index].value                     
		     item = (aux[0], newnomvec, eta, sol)
		     W.append(item)
		     if sol > 0.0:
			     tmp_str = newnomvec + ',' + str(eta) + ',' + str(sol) +'\n'
			     fw.write(tmp_str)
        if var == 'Y':
                objv = getattr(instance, var)
		for index in objv:
		     readpar = str(objv[index])
                     aux = readpar.split('[')
                     nomvec = list(aux[1])
                     vec = aux[1].split(',')
                     lc = len(vec) - 1
                     oldstr = vec[lc]
                     eta = oldstr.replace("]","")
                     nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                     newnomvec = "".join(nomvec)
                     sol = objv[index].value
		     item = (aux[0], newnomvec, eta, sol)
		     Y.append(item)
		     if sol > 0.0:
			     tmp_str = newnomvec + ',' + str(eta) + ',' + str(sol) +'\n'
			     fy.write(tmp_str)
        if var == 'Z':
                objv = getattr(instance, var)
		for index in objv:
		     readpar = str(objv[index])
		     aux = readpar.split('[')
                     nomvec = list(aux[1])
                     vec = aux[1].split(',')
                     lc = len(vec) - 1
                     oldstr = vec[lc]
                     eta = oldstr.replace("]","")
                     nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                     newnomvec = "".join(nomvec)
                     sol = objv[index].value
		     item = (aux[0], newnomvec, eta, sol)
		     Z.append(item)
		     if sol > 0.0:
			     tmp_str = newnomvec + ',' + str(eta) + ',' + str(sol) +'\n'
			     fz.write(tmp_str)
#        if var == 'flup':
#                objv = getattr(instance, var)
#		for index in objv:
#		     readpar = str(objv[index])
#		     aux = readpar.split('[')
#                     nomvec = list(aux[1])
#                     vec = aux[1].split(',')
#                     eta = int(vec[2].replace("]",""))
#                     tr  = int(vec[1])
#                     lin = int(vec[0])
#                     lineas.append(lin)
#                     if (lin == 1 and eta == 1):
#                        tramos.append(tr)
#                     if (tr == 1 and eta == 1):
#                        lineas.append(lin)
#                     if (lin == 1 and tr == 1):
#                        etapas.append(eta)
#                     sol = float(objv[index].value)
#		     ub = float(objv[index].ub)
#                     fluptr[lin, tr, eta] = str(sol)
#		     fluptr_ubnd[lin,tr,eta] = str(ub)
#	if var == 'flun':
#                objv = getattr(instance, var)
#		for index in objv:
#	             readpar = str(objv[index])
#		     aux = readpar.split('[')
#                     nomvec = list(aux[1])
#                     vec = aux[1].split(',')                     
#                     eta = int(vec[2].replace("]",""))
#                     tr  = int(vec[1])
#                     lin = int(vec[0])
#                     sol = float(objv[index].value)
#		     ub = float(objv[index].ub)
#                     fluntr[lin, tr, eta] = str(sol)		    
#		     fluntr_ubnd[lin, tr, eta] = str(ub)		    
#                if aux[0] == 'varphi':
#                     nomvec = list(aux[1])
#                     vec = aux[1].split(',')
#                     sol = float(objv[index].value)
#                     varphi[vec[0]] = sol
#                isim += 1

#	for l in lineas:
#        	 for t in etapas:
#	             flup[l,t] = sum(float(fluptr[l,tr,t]) for tr in tramos)		   
#        	     flun[l,t] = sum(float(fluntr[l,tr,t]) for tr in tramos)
#	             flup_ubnd[l,t] = sum(fluptr_ubnd[l,tr,t] for tr in tramos)
#        	     flun_ubnd[l,t] = sum(fluntr_ubnd[l,tr,t] for tr in tramos)
#	             caca = flup[l,t] - flun[l,t]
#        	     caca_bnd = flup_ubnd[l,t] - flun_ubnd[l,t]
#	             flin.write('flu' + ',' + str(l) + ',' + str(t) + ',' + str(caca) + ',' + str(caca_bnd) + '\n')	
######FIN almacenamiento soluciobnees#############
                
#     gen_test = np.array(gen)
     #gen_test1 = sorted(gen_test, key=operator.itemgetter(4), reverse=True)
     #gen_test2 = sorted(gen_test1, key=operator.itemgetter(1))

 #    vert_test = np.array(vert)
     #vert_test1 = sorted(vert_test, key=operator.itemgetter(2))
     #vert_test2 = sorted(vert_test1, key=operator.itemgetter(1), reverse=True)

 #    vol_test = np.array(vol)
     #vol_test1 = sorted(vol_test, key=operator.itemgetter(2))
     #vol_test2 = sorted(vol_test1, key=operator.itemgetter(1))

  #   afl_test = np.array(afl)
     #afl_test1 = sorted(afl_test, key=operator.itemgetter(2))
     #afl_test2 = sorted(afl_test1, key=operator.itemgetter(1))

     
######FIN ordenamiento de arreglos#############
     #print ('Longitud '+str(len(gen_test)))
#     for gen in gen_test:
#	tmp_str =  ','.join(map(str,gen))
#        fgen.write(tmp_str)
#        fgen.write("\n")

#     for vert in vert_test:
#	tmp_str =  ','.join(map(str,vert))
#	fvert.write(tmp_str)
#        fvert.write("\n")

#     for vol in vol_test:
#	tmp_str =  ','.join(map(str,vol))
#	fvol.write(tmp_str)
#        fvol.write("\n")

#     for afl in afl_test:
#	tmp_str =  ','.join(map(str,afl))
#	fafl.write(tmp_str)
#        fafl.write("\n")           
     obj_value = results.Solution.Objective.__default_objective__['value']
     fp.write(str(obj_value))

     fo.close()
     fp.close()
#     fphi.close()
#     flin.close()
     fgen.close()
     fvert.close()
     fvol.close()
     fafl.close()
     fw.close()
     fy.close()
     fz.close()
