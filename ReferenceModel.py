import sys
import os
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))
#from coopr.pyomo import *
from pyomo.core import *
from pyomo.environ import *
from math import pow

#from coopr.pyomo.base.sparse_indexed_component import *
#SparseIndexedComponent._DEFAULT_INDEX_CHECKING_ENABLED = False

model = AbstractModel()

infty = float('inf')
###########################################################################
# SETS
###########################################################################

model.BARRAS = Set(ordered=True)

def bar_rule(model):
	item = []
	for bar in model.BARRAS:
		if bar>0:
			item.append(bar)
	return item
model.BARRAS2 = Set(dimen=1, ordered=True, initialize=bar_rule)

model.LINEAS = Set(ordered=True)

model.NTram = Param(within=PositiveIntegers)
model.TRP = RangeSet(1, model.NTram)

model.StgTree = Param(within=PositiveIntegers)
model.StgSet = RangeSet(1, model.StgTree)

model.CENE = Set(ordered=True)
model.CENT = Set(ordered=True)
model.CENS = Set(ordered=True)
model.CENP = Set(ordered=True)
model.CENHS = model.CENE|model.CENS
model.CENH = model.CENHS|model.CENP
model.CENF = Set(ordered=True)
model.CENTRALES = model.CENH|model.CENT|model.CENF

model.NHoras = Param(within=Integers)
model.HORAS = RangeSet(1,model.NHoras)

model.NSim = Param()
model.NIte = Param()
model.SIM = RangeSet(1, model.NSim)
model.ITE = RangeSet(1, model.NIte)

model.NSimul = Param(initialize=53)

#def Nhoriz_rule(model):
#	item=[]
#	item.append(model.NHoras)
#	return item
model.NHORIZ = RangeSet(model.NHoras, model.NHoras)

#def demset_rule(model):
#	item = []
#	for (b,t) in model.BARRAS*model.HORAS:
#		if b>0:
#			item.append((t,b))
#	return item
#model.Demset = Set(dimen=2, initialize=demset_rule)

###########################################################################
# PARAMETERS
###########################################################################

model.GenMax  = Param(model.CENTRALES, within = NonNegativeReals)
model.GenMin  = Param(model.CENTRALES, within = NonNegativeReals)
model.VerMax  = Param(model.CENH, within = NonNegativeReals)
model.VerMin  = Param(model.CENH, within = NonNegativeReals)
model.VMax    = Param(model.CENE, within = NonNegativeReals)
model.VMin    = Param(model.CENE, within = NonNegativeReals)
model.CosGen  = Param(model.CENTRALES, within = NonNegativeReals)
model.RenCen  = Param(model.CENTRALES, within = NonNegativeReals)
model.AflCen  = Param(model.CENTRALES, model.HORAS, within = NonNegativeReals, default = 0.0)
model.c_ini   = Param(model.CENE, within = NonNegativeReals)
model.sergen  = Param(model.CENHS, model.CENHS, within = NonNegativeIntegers)
model.server  = Param(model.CENHS, model.CENHS, within = NonNegativeIntegers)

model.dureta  = Param(model.HORAS, within = NonNegativeReals)
model.DemBar  = Param(model.BARRAS2, model.HORAS)

model.x       = Param(model.LINEAS, within = NonNegativeReals)
model.R       = Param(model.LINEAS, within = NonNegativeReals)
model.V       = Param(model.LINEAS, within = NonNegativeReals)
model.IndCB   = Param(model.BARRAS, model.CENTRALES, within=NonNegativeIntegers, default = 0)
model.Ind1BL  = Param(model.BARRAS, model.LINEAS, within=NonNegativeIntegers, default = 0)
model.Ind2BL  = Param(model.BARRAS, model.LINEAS, within=NonNegativeIntegers, default = 0)
model.tram    = Param(model.LINEAS, within = NonNegativeReals)
model.FluAB   = Param(model.LINEAS, model.HORAS, within=NonNegativeReals)
model.FluBA   = Param(model.LINEAS, model.HORAS, within=NonNegativeReals)

model.LinOpe  = Param(model.LINEAS, within=NonNegativeIntegers)
model.LinFPer = Param(model.LINEAS, within=NonNegativeIntegers)


model.CoPerdAB = Param(model.LINEAS, model.TRP, within=Reals)
model.CoPerdBA = Param(model.LINEAS, model.TRP, within=Reals)

model.ManCenMax = Param(model.CENTRALES, model.HORAS, within=NonNegativeReals)
model.ManCenMin = Param(model.CENTRALES, model.HORAS, within=NonNegativeReals)
model.ManLinAB = Param(model.LINEAS, model.HORAS, within=NonNegativeReals)
model.ManLinBA = Param(model.LINEAS, model.HORAS, within=NonNegativeReals)
model.ManEmbMax = Param(model.CENE, model.HORAS, within=NonNegativeReals)
model.ManEmbMin = Param(model.CENE, model.HORAS, within=NonNegativeReals)

model.picip    = Param(model.SIM, model.ITE)
model.pipeh    = Param(model.SIM, model.ITE)
model.picolb    = Param(model.SIM, model.ITE)
model.pitoro    = Param(model.SIM, model.ITE)
model.pirapel    = Param(model.SIM, model.ITE)
model.picanut    = Param(model.SIM, model.ITE)
model.piralco    = Param(model.SIM, model.ITE)

model.phi        = Param(model.SIM, model.ITE)
model.FTIME      = Param(within = NonNegativeReals, default = 3.60)

model.IndMinTec  = Param(model.CENTRALES, within=NonNegativeIntegers, default = 0)
model.IndOnoff   = Param(model.CENTRALES, within=NonNegativeIntegers, default = 0)
model.CostArr    = Param(model.CENTRALES, within=NonNegativeReals, default = 0.0)
model.CostDet    = Param(model.CENTRALES, within=NonNegativeReals, default = 0.0)

model.netaope    = Param(model.CENTRALES, within=NonNegativeIntegers, default = 0)
model.netadet    = Param(model.CENTRALES, within=NonNegativeIntegers, default = 0)
model.netaini    = Param(model.CENTRALES, within=NonNegativeIntegers, default = 0)
model.est_ini    = Param(model.CENTRALES, within=NonNegativeIntegers, default = 0)

#def tope_rule(m,c):
#	if (model.IndMinTec[c] > 0) & (model.netaope[c]-model.netaini[c] >0):
#		return	model.netaope[c]-model.netaini[c]
#	else:
#		return 0
#model.tauope     = Param(model.CENTRALES, initialize=tope_rule) 


####SUPER SETS########################33
#to demand constraint
def v1_rule(model, bar):
	item = []
	for cen in model.CENTRALES:
		if model.IndCB[bar, cen]:
			item.append(cen)
	return item
model.V1 = Set(model.BARRAS2, dimen=1, initialize=v1_rule)

#to g bound for unserved energy
def v2_rule(model, c):
	item = []
	for (bar,cen) in model.BARRAS2*(model.CENH|model.CENT):
		if model.IndCB[bar, cen] and model.IndCB[bar,c]:
			item.append(cen)
	return item
model.V2 = Set(model.CENF, dimen=1, initialize=v2_rule)

def lin1_rule(model, bar):
	item_glo = []
	item = []
	for lin in model.LINEAS:
		if (model.Ind1BL[bar,lin] == 1 and model.LinOpe[lin]):
			for tr in model.TRP:
				item.append((lin,tr))
	return item
model.LIN1 = Set(model.BARRAS2, dimen=2, initialize=lin1_rule)

def lin2_rule(model, bar):
	item_glo = []
	item = []
	for lin in model.LINEAS:
		if (model.Ind2BL[bar,lin] == 1 and model.LinOpe[lin]):
			for tr in model.TRP:
				item.append((lin,tr))
	return item
model.LIN2 = Set(model.BARRAS2, dimen=2, initialize=lin2_rule)

def fdcr_rule(model):
	item = []
	for lin in model.LINEAS:
		if model.LinOpe[lin] == 1:
			item.append(lin)
	return item
model.LINR = Set(within=model.LINEAS, initialize=fdcr_rule)

def fdcr1_rule(model, lin):
	item = []
	for bar in model.BARRAS2:
		if model.Ind1BL[bar,lin] == 1:
			item.append(bar)
	return item
model.BARLIN1 = Set(model.LINR, dimen=1, initialize=fdcr1_rule)

def fdcr2_rule(model, lin):
	item = []
	for bar in model.BARRAS2:
		if model.Ind2BL[bar,lin] == 1:
			item.append(bar)
	return item
model.BARLIN2 = Set(model.LINR, dimen=1, initialize=fdcr2_rule)

###########################################################################
# variables
###########################################################################
def g_bnd(model,c,t):
	if(model.IndMinTec[c] == 1):
                l_bnd = 0.0
		u_bnd = model.ManCenMax[c,t]/model.RenCen[c]
        else:
		l_bnd = model.ManCenMin[c,t]/model.RenCen[c]
		u_bnd = model.ManCenMax[c,t]/model.RenCen[c]
	if(c in model.CENF):
		l_bnd = -10000.0
		#Of = sum(model.ManCenMax[cen,t]/model.RenCen[cen] for cen in model.V2[c])
		#u_bnd = max(sum(model.DemBar[bar,t] for bar in model.BARRAS2 if model.IndCB[bar,c]) - Of, 0)
		u_bnd = 10000.0;
        return(l_bnd, u_bnd)
model.g   = Var(model.CENTRALES, model.HORAS, within=NonNegativeReals, bounds=g_bnd) 

def v_bnd(model,c,t):
	return(model.VerMin[c], model.VerMax[c])
model.v   = Var(model.CENH, model.HORAS, within=NonNegativeReals, bounds=v_bnd)

model.theta  = Var(model.BARRAS, model.HORAS)

def  flAB_bnd(model,l,tr,t):
	if model.LinFPer[l] == 1:
		u_bnd = model.ManLinAB[l,t]/model.NTram
	else:
		u_bnd = model.ManLinAB[l,t]
        return(0, u_bnd)
model.flup = Var(model.LINEAS, model.TRP, model.HORAS, bounds=flAB_bnd, within=NonNegativeReals)
def  flBA_bnd(model,l,tr,t):
	if model.LinFPer[l] == 1:
		u_bnd = model.ManLinBA[l,t]/model.NTram
	else:
		u_bnd = model.ManLinBA[l,t]
        return(0, u_bnd)
model.flun = Var(model.LINEAS, model.TRP, model.HORAS, bounds=flBA_bnd, within=NonNegativeReals)

def ManEmb_bnd(model,e,t):
	return(model.ManEmbMin[e,t], model.ManEmbMax[e,t])
model.c      = Var(model.CENE, model.HORAS,bounds=ManEmb_bnd, within=NonNegativeReals)
model.afl    = Var(model.CENE, model.HORAS, within=NonNegativeReals)
model.varphi = Var(model.SIM, within=NonNegativeReals )

model.W   = Var(model.CENTRALES, model.HORAS, within=Binary)
model.Y   = Var(model.CENTRALES, model.HORAS, within=Binary)
model.Z   = Var(model.CENTRALES, model.HORAS, within=Binary)

model.StageCost = Var(model.StgSet, within= NonNegativeReals)

###########################################################################
# constrains
###########################################################################

#Demand
def dem_rule(model,t,b):
	exprG = sum(model.RenCen[cen]*model.g[cen,t] for cen in model.V1[b])
	exprF1 = sum(model.CoPerdAB[l,tr]*model.flup[l,tr,t] for (l, tr) in model.LIN1[b])+\
 		sum(model.CoPerdBA[l,tr]*model.flun[l,tr,t] for (l, tr) in model.LIN1[b])
	exprF2 = sum(model.CoPerdAB[l,tr]*model.flup[l,tr,t] for (l, tr) in model.LIN2[b])+\
		sum(model.CoPerdBA[l,tr]*model.flun[l,tr,t] for (l, tr) in model.LIN2[b])
	return exprG + exprF1 + exprF2 == model.DemBar[b,t]
model.demanda = Constraint(model.HORAS, model.BARRAS2,rule=dem_rule)

#mass balance for reservoir
def vol_rule(model,t,cen):
        if t > 1:
                return model.c[cen,t] - model.c[cen,t-1]+ model.FTIME*model.dureta[t]*(model.g[cen,t]+model.v[cen,t] -\
                        sum(model.g[cs,t] for cs in model.CENHS if (model.sergen[cs,cen] ==1 and cen != cs)) -\
                        sum(model.v[cs,t] for cs in model.CENHS if (model.server[cs,cen] ==1 and cen != cs)) -\
                        model.afl[cen,t]) == model.AflCen[cen, t]*model.dureta[t]*model.FTIME
        else:
                return model.c[cen,t] + model.FTIME*model.dureta[t]*(model.g[cen,t]+model.v[cen,t] -\
                        sum(model.g[cs,t] for cs in model.CENHS if (model.sergen[cs,cen] ==1 and cen != cs)) -\
                        sum(model.v[cs,t] for cs in model.CENHS if (model.server[cs,cen] ==1 and cen != cs)) -\
                        model.afl[cen,t]) == model.c_ini[cen] + model.AflCen[cen, t]*model.dureta[t]*model.FTIME                
model.BalVol = Constraint(model.HORAS, model.CENE, rule=vol_rule)

#flow balance for hydro gen
def ser_rule(model,t,cen):
        return model.FTIME*(model.g[cen,t]+model.v[cen,t] -\
                        sum(model.g[cs,t] for cs in model.CENHS if (model.sergen[cs,cen] ==1 and cen != cs)) -\
                        sum(model.v[cs,t] for cs in model.CENHS if (model.server[cs,cen] ==1 and cen != cs))) ==\
                        model.AflCen[cen, t]*model.FTIME
model.BalSer = Constraint(model.HORAS, model.CENS, rule=ser_rule)

#DC PF
def fdc_rule(model,t,l):
	return sum(model.flup[l,tr,t] for tr in model.TRP) -\
                       sum(model.flun[l,tr,t] for tr in model.TRP) -\
                       (-sum(model.theta[b,t] for b in model.BARLIN1[l])-\
                       sum(model.theta[b,t]  for b in model.BARLIN2[l]))*model.x[l]*100 == 0.0
model.FDC = Constraint(model.HORAS, model.LINR, rule=fdc_rule)

#Node DC
def ndc_rule(model, t, b):
        if b != 1 or b!=0:
                return Constraint.Skip
        else:
                return model.theta[b,t] == 0.0
model.NDC        = Constraint(model.HORAS, model.BARRAS, rule=ndc_rule)


#FCF
def fcf_rule(model,it,sim,t):
	exprPi = model.picip[sim,it]*model.c['CIPRESES',t]+model.pipeh[sim,it]*model.c['PEHUENCHE',t]+model.picolb[sim,it]*model.c['COLBUN',t]+\
		model.pitoro[sim,it]*model.c['ELTORO',t]+model.pirapel[sim,it]*model.c['RAPEL',t]+model.picanut[sim,it]*model.c['CANUTILLAR',t]+\
		model.piralco[sim,it]*model.c['RALCO',t]+model.varphi[sim]
	return exprPi >= model.phi[sim,it]
model.FCF   = Constraint(model.ITE, model.SIM, model.NHORIZ, rule=fcf_rule)

#MinTecL
def mintl_rule(model,t,cen):
        if model.IndMinTec[cen] == 1 and model.ManCenMin[cen,t]>0:
                return model.g[cen,t] >= model.ManCenMin[cen,t]*model.W[cen,t]
        else:
                return Constraint.Skip
model.MinTecL = Constraint(model.HORAS, model.CENTRALES, rule=mintl_rule)

#MinTecU
def mintu_rule(model,t,cen):
        if model.IndMinTec[cen] == 1 and model.ManCenMin[cen,t]>0:
                return model.g[cen,t] <= model.ManCenMax[cen,t]*model.W[cen,t]
        else:
                return Constraint.Skip
model.MinTecU = Constraint(model.HORAS, model.CENTRALES, rule=mintu_rule)

#Onoff1
def onoff1_rule(model, t, cen):
        if model.IndMinTec[cen] == 1 and model.IndOnoff[cen] == 1:
                if t == 1:
                        return model.W[cen,t] - model.Y[cen,t] + model.Z[cen,t]  == model.est_ini[cen]
                else:
                        return model.W[cen,t]-model.W[cen,t-1] - model.Y[cen,t] + model.Z[cen,t] == 0
        else:
                return Constraint.Skip
model.Onoff1  = Constraint(model.HORAS, model.CENTRALES, rule=onoff1_rule)        

#Onoff2
def onoff2_rule(model, t, cen):
        if model.IndMinTec[cen] == 1 and model.IndOnoff[cen] == 1:
                return model.Y[cen,t] + model.Z[cen,t] <= 1
        else:
                return Constraint.Skip
model.Onoff2  = Constraint(model.HORAS, model.CENTRALES, rule=onoff2_rule)        



#FOBJECTIVE#################################################################
#CFO
def stage_cost_rule(model,t):
        if t > 1:
                exprCG = sum(model.CosGen[cen]*model.dureta[taux]*model.g[cen,taux] for (cen, taux) in model.CENTRALES*model.HORAS)+\
                         sum(1/pow(1.01,taux)*model.dureta[taux]*model.FTIME*model.v[cen,taux] for (cen, taux) in model.CENH*model.HORAS)+\
			 0.036*sum(model.flup[l,tr,tuax] +model.flun[l,tr,tuax] for (l,tr,tuax) in model.LINEAS*model.TRP*model.HORAS)+\
                         sum(model.varphi[sim] for sim in model.SIM)/model.NSim+\
			 sum(7000*model.FTIME*model.afl[cen,taux] for (cen,taux) in model.CENE*model.HORAS)
                return model.StageCost[t] == exprCG 
        else:
                expr = sum(model.CostDet[cen]*model.dureta[taux]*model.Z[cen,taux] for (cen, taux) in model.CENTRALES*model.HORAS)	
                return model.StageCost[t] == expr
model.stage_cost_constraint = Constraint(model.StgSet, rule=stage_cost_rule) 

#FO
def total_cost_rule(model):
    return summation(model.StageCost)
model.Objective_rule = Objective(rule=total_cost_rule, sense=minimize)

