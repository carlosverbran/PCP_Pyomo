import sys
import operator

def pyomo_postprocess(results, n):
     tmp_name_g='g'+str(n)+'.csv'
     tmp_name_v='v'+str(n)+'.csv'
     tmp_name_theta='theta'+str(n)+'.csv'
     tmp_name_c='vol'+str(n)+'.csv'
     tmp_name_afl='afl'+str(n)+'.csv'
     tmp_name_w='w'+str(n)+'.csv'
     tmp_name_y='y'+str(n)+'.csv'
     tmp_name_z='z'+str(n)+'.csv'


     fg = open(tmp_name_g,'w')
     fv = open(tmp_name_v,'w')
     ft = open(tmp_name_theta,'w')
     fc = open(tmp_name_c,'w')
     fa = open(tmp_name_afl,'w')
     fw = open(tmp_name_w,'w')
     fy = open(tmp_name_y,'w')
     fz = open(tmp_name_z,'w')

     fluptr = {}
     flup = {}
     fluntr = {}
     flun = {}
     lineas = []
     tramos = []
     etapas = []
     varphi = {}

     item = []
     g = []	
     v = []	
     theta = []	
     c = []	
     afl = []	
     w = []	
     y = []	
     z = []

     fg.write('clave, nom, eta, value\n')
     fv.write('clave, nom, eta, value\n')
     ft.write('clave, nom, eta, value\n')
     fc.write('clave, nom, eta, value\n')
     fa.write('clave, nom, eta, value\n')
     fw.write('clave, nom, eta, value\n')
     fy.write('clave, nom, eta, value\n')
     fz.write('clave, nom, eta, value\n')

     for i in range(len(results.solution)):
         for var in results.solution[i].variable:
             aux = var.split('(')
             if aux[0] == 'g':
                nomvec = list(aux[1])
	        vec = aux[1].split('_')
                lc = len(vec) - 1
                oldstr = vec[lc]
                eta = oldstr.replace(")","")
		nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
		if len(eta) == 1:
			eta = '00'+eta
		elif len(eta) == 2:
			eta='0'+eta
                newnomvec = "".join(nomvec)
	        sol = results.solution[i].variable[var]['Value']
		item = (aux[0], newnomvec, eta, sol)	
		g.append(item)
	#	fo.write(aux[0] + ',' + newnomvec + ',' + eta + ',' + str(sol))
        #       fo.write("\n")
             if aux[0] == 'v':
                nomvec = list(aux[1])
	        vec = aux[1].split('_')
                lc = len(vec) - 1
                oldstr = vec[lc]
                eta = oldstr.replace(")","")

		if len(eta) == 1:
			eta = '00'+eta
		elif len(eta) == 2:
			eta='0'+eta
                nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                newnomvec = "".join(nomvec)
	        sol = results.solution[i].variable[var]['Value']
		item = (aux[0], newnomvec, eta, sol)	
		v.append(item)
	#	fo.write(aux[0] + ',' + newnomvec + ',' + eta + ',' + str(sol))
        #       fo.write("\n")
             if aux[0] == 'theta':
                nomvec = list(aux[1])
	        vec = aux[1].split('_')
                lc = len(vec) - 1
                oldstr = vec[lc]
                eta = oldstr.replace(")","")

		if len(eta) == 1:
			eta = '00'+eta
		elif len(eta) == 2:
			eta='0'+eta
                nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []
                newnomvec = "".join(nomvec)
	        sol = results.solution[i].variable[var]['Value']
		item = (aux[0], newnomvec, eta, sol)	
		theta.append(item)
	#	fo.write(aux[0] + ',' + newnomvec + ',' + eta + ',' + str(sol))
        #       fo.write("\n")
             if aux[0] == 'c':
                nomvec = list(aux[1])
	        vec = aux[1].split('_')
                lc = len(vec) - 1
                oldstr = vec[lc]
                eta = oldstr.replace(")","")
                nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []

		if len(eta) == 1:
			eta = '00'+eta
		elif len(eta) == 2:
			eta='0'+eta
                newnomvec = "".join(nomvec)
	        sol = results.solution[i].variable[var]['Value']
		item = (aux[0], newnomvec, eta, sol)	
		c.append(item)
	#	fo.write(aux[0] + ',' + newnomvec + ',' + eta + ',' + str(sol))
        #       fo.write("\n")
             if aux[0] == 'afl':
                nomvec = list(aux[1])
	        vec = aux[1].split('_')
                lc = len(vec) - 1
                oldstr = vec[lc]
                eta = oldstr.replace(")","")
                nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []

		if len(eta) == 1:
			eta = '00'+eta
		elif len(eta) == 2:
			eta='0'+eta
                newnomvec = "".join(nomvec)
	        sol = results.solution[i].variable[var]['Value']
		item = (aux[0], newnomvec, eta, sol)	
		afl.append(item)
	#	fo.write(aux[0] + ',' + newnomvec + ',' + eta + ',' + str(sol))
        #       fo.write("\n")
             if aux[0] == 'W':
                nomvec = list(aux[1])
	        vec = aux[1].split('_')
                lc = len(vec) - 1
                oldstr = vec[lc]
                eta = oldstr.replace(")","")
                nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []

		if len(eta) == 1:
			eta = '00'+eta
		elif len(eta) == 2:
			eta='0'+eta
                newnomvec = "".join(nomvec)
	        sol = results.solution[i].variable[var]['Value']
		item = (aux[0], newnomvec, eta, sol)	
		w.append(item)
	#	fo.write(aux[0] + ',' + newnomvec + ',' + eta + ',' + str(sol))
        #       fo.write("\n")
             if aux[0] == 'Y':
                nomvec = list(aux[1])
	        vec = aux[1].split('_')
                lc = len(vec) - 1
                oldstr = vec[lc]
                eta = oldstr.replace(")","")
                nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []

		if len(eta) == 1:
			eta = '00'+eta
		elif len(eta) == 2:
			eta='0'+eta
                newnomvec = "".join(nomvec)
	        sol = results.solution[i].variable[var]['Value']
		item = (aux[0], newnomvec, eta, sol)	
		y.append(item)
	#	fo.write(aux[0] + ',' + newnomvec + ',' + eta + ',' + str(sol))
        #       fo.write("\n")
             if aux[0] == 'Z':
                nomvec = list(aux[1])
	        vec = aux[1].split('_')
                lc = len(vec) - 1
                oldstr = vec[lc]
                eta = oldstr.replace(")","")
                nomvec[len(nomvec)-len(eta)-2:len(nomvec)] = []

		if len(eta) == 1:
			eta = '00'+eta
		elif len(eta) == 2:
			eta='0'+eta
                newnomvec = "".join(nomvec)
	        sol = results.solution[i].variable[var]['Value']
		item = (aux[0], newnomvec, eta, sol)	
		z.append(item)
	#	fo.write(aux[0] + ',' + newnomvec + ',' + eta + ',' + str(sol))
        #       fo.write("\n")

	     if aux[0] == 'flup':
	        nomvec = list(aux[1])
	        vec = aux[1].split('_')
                eta = int(vec[2].replace(")",""))
                tr  = int(vec[1])
                lin = int(vec[0])
                if (lin == 1 and eta == 1):
                   tramos.append(tr)
                if (tr == 1 and eta == 1):
                   lineas.append(lin)
                if (lin == 1 and tr == 1):
                   etapas.append(eta)
                fluptr[lin, tr, eta] = str(results.solution[i].variable[var]['Value'])
	     if aux[0] == 'flun':
	        nomvec = list(aux[1])
	        vec = aux[1].split('_')
                eta = int(vec[2].replace(")",""))
                tr  = int(vec[1])
                lin = int(vec[0])
                fluntr[lin, tr, eta] = str(results.solution[i].variable[var]['Value'])
             if aux[0] == 'varphi':
	        nomvec = list(aux[1])
	        vec = aux[1].split('_')
                varphi[vec[0]] = str(results.solution[i].variable[var]['Value'])
     for l in lineas:
         for t in etapas:
             flup[l,t] = sum(float(fluptr[l,tr,t]) for tr in tramos)
             flun[l,t] = sum(float(fluntr[l,tr,t]) for tr in tramos)
             caca = flup[l,t] - flun[l,t]
             #fo.write('flu' + ',' + str(l) + ',' + str(t) + ',' + str(caca))
             #fo.write('\n')

     gen_test = list(g)
     gen_test1 = sorted(gen_test, key=operator.itemgetter(2))
     gen_test2 = sorted(gen_test1, key=operator.itemgetter(1))
     for gen in gen_test2:
        tmp_str =  ','.join(map(str,gen))
        fg.write(tmp_str)
        fg.write("\n")

     v_test = list(v)
     v_test1 = sorted(v_test, key=operator.itemgetter(2))
     v_test2 = sorted(v_test1, key=operator.itemgetter(1))
     for ver in v_test2:
        tmp_str =  ','.join(map(str,ver))
        fv.write(tmp_str)
        fv.write("\n")

     t_test = list(theta)
     t_test1 = sorted(t_test, key=operator.itemgetter(2))
     t_test2 = sorted(t_test1, key=operator.itemgetter(1))
     for t in t_test2:
        tmp_str =  ','.join(map(str,t))
        ft.write(tmp_str)
        ft.write("\n")

     c_test = list(c)
     c_test1 = sorted(c_test, key=operator.itemgetter(2))
     c_test2 = sorted(c_test1, key=operator.itemgetter(1))
     for vol in c_test2:
        tmp_str =  ','.join(map(str,vol))
        fc.write(tmp_str)
        fc.write("\n")

     a_test = list(afl)
     a_test1 = sorted(a_test, key=operator.itemgetter(2))
     a_test2 = sorted(a_test1, key=operator.itemgetter(1))
     for af in a_test2:
        tmp_str =  ','.join(map(str,af))
        fa.write(tmp_str)
        fa.write("\n")

     w_test = list(w)
     w_test1 = sorted(w_test, key=operator.itemgetter(2))
     w_test2 = sorted(w_test1, key=operator.itemgetter(1))
     for wr in w_test2:
	if wr[3] == 1.0:
	        tmp_str =  ','.join(map(str,wr))
        	fw.write(tmp_str)
	        fw.write("\n")


     y_test = list(y)
     y_test1 = sorted(y_test, key=operator.itemgetter(2))
     y_test2 = sorted(y_test1, key=operator.itemgetter(1))
     for yi in y_test2:
	if yi[3] == 1.0:
	        tmp_str =  ','.join(map(str,yi))
        	fy.write(tmp_str)
	        fy.write("\n")

     z_test = list(z)
     z_test1 = sorted(z_test, key=operator.itemgetter(2))
     z_test2 = sorted(z_test1, key=operator.itemgetter(1))
     for zr in z_test2:
	if zr[3] == 1.0:
	        tmp_str =  ','.join(map(str,zr))
	        fz.write(tmp_str)
	        fz.write("\n")


     fg.close()
     fv.close()
     ft.close()
     fc.close()
     fa.close()
     fw.close()
     fy.close()
     fz.close()

