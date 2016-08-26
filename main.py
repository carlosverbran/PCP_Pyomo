__author__ = 'MPro'

import os
import sys
import string
import time
import numpy
import scipy
from multiprocessing import Process
import multiprocessing as mp
from pyomo.core import *
from pyomo.opt import SolverFactory
from ReferenceModel import model
from wrcsv import pyomo_postprocess

options_in = {}

str_nscen = sys.argv[1]
nscen = int(str_nscen)
ncpu = mp.cpu_count()
threads = ncpu/nscen

#options_in['threads'] = threads
options_in['logfile'] = 'solver.log'
options_in['optimalitytol']  = 1e-9
options_in['FeasibilityTol']  = 1e-9

#optVal=numpy.array([0 for i in range(nscen)])
def algorit(n, m):
    nameins = 'Scen_base' + str(n) + '.dat'
    namelp = 'prob' + str(n) + '.lp'
    print nameins
    start_time = time.time()
    instance = m.create(nameins)
    opt = pyomo.opt.base.solvers.SolverFactory('gurobi', options = options_in)
    opt.symbolic_solver_labels=True        
    #instance.write(namelp,  io_options={'symbolic_solver_labels':True})
    elapsed_time =  '%2.2f' % float(time.time()-start_time)
    print 'time to instance', str(elapsed_time),  's'
    start_time = time.time()
    results = opt.solve(instance)
    instance.load(results)
    print 'tiempo de resolucion', time.time() - start_time, 's'
#    optVal[n-1] = results.solution.objective.__default_objective__.value
    start_time = time.time()
    pyomo_postprocess(results, n)
    print 'tiempo de escritura', time.time() - start_time, 's'
   
#Secuencial
#algorit(int(sys.argv[1]), model)

#Paralelo        
if __name__ == '__main__':
    for sim in range(1, nscen + 1):
        p = Process(target=algorit, args=(sim, model))
        p.start()
    p.join()


