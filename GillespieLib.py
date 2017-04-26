import random as rd
import math
import numpy as np
import matplotlib.pyplot as plt

#import GillespieInput_loktaVolterra as Gi
import GillespieInput_deter as Gi


def a(N, M, population, R, vc):
    va = [0]*M
    vh = Gi.h(population)
    for i in range(0,M):
        #for j in range(0,N):
            #if(R[i][j] != 0):
	va[i] = vc[i]*vh[i]
    return va

def aCumule(va):
    M = len(va)
    ac= [0]*M
    ac[0] = va[0]
    for i in range(1,M):
        ac[i] = ac[i-1] + va[i]
    return ac

def tau(a0, r1):
    return -math.log(r1)/a0

#attention, renvoie mu-1 (pratique car directement en phase avec les tableaux python)
def mu(ac, r2):
    vmu = 0
    M = len(ac)
    while(ac[vmu] < r2*ac[M-1]):
        vmu += 1
    return vmu

def applyReaction(vmu, population, R):
    M = len(R)
    N = len(population)
    newPop = []
    newPop += population
    for j in range(0,N):
        if(R[vmu][j] != 0):
            newPop[j] -= R[vmu][j]
    
    for j in range(N,N+N):
        if(R[vmu][j] != 0):
            newPop[j-N] += R[vmu][j]
            
    return newPop




def printInfo():
	#Affichage de la population initiale.
	strInfoPopInit = "Initialement, il y a : \n"
	for i in range(0,Gi.N):
	    strInfoPopInit += str(Gi.populationInit[i]) + " " + Gi.popNames[i] + (".\n\n" if (i == Gi.N-1) else ", \n")

	#Affichage des reactions possibles : 
	strInfoReac = "Les reactions possibles sont : \n"
	for i in range(0,Gi.M):
	    first = True
	    for j in range(0,Gi.N):
		if(Gi.R[i][j] != 0):
		    if(first):
			strInfoReac += str(Gi.R[i][j]) + str(Gi.popNames[j])
			first = False
		    else: strInfoReac += " + " + str(Gi.R[i][j]) + str(Gi.popNames[j])
	    strInfoReac += " --> "
	    first = True
	    for j in range(Gi.N,Gi.N+Gi.N):
		if(Gi.R[i][j] != 0):
		    if(first): 
			strInfoReac += str(Gi.R[i][j]) + str(Gi.popNames[j-Gi.N])
			first = False
		    else: strInfoReac += " + " + str(Gi.R[i][j]) + str(Gi.popNames[j-Gi.N])
	    strInfoReac += "\n"
	    
	print(strInfoPopInit)
	print(strInfoReac)

def experience(seedUnique):
    rd.seed(seedUnique)
    t = 0
    step = 0
    a0 = 1
    populations = []
    populations.append([t,Gi.populationInit, 0])
    while(t < Gi.Tmax and  step <= Gi.Nmax and a0 != 0):
        vc  = Gi.c(t)
        va  = a(Gi.N, Gi.M, populations[step][1], Gi.R, vc)
        vac = aCumule(va)
        r1 = rd.random()
        r2 = rd.random()
        a0 = vac[Gi.M-1]
	if(a0 != 0):
		vtau = tau(a0, r1)
		vmu = mu(vac, r2)
		t = t + vtau
		populations.append([t,applyReaction(vmu, populations[step][1], Gi.R), vtau*populations[step][1][0]])
		step += 1
    return populations
    
    
def translateResults(results):
	K = len(results)
	res = []
	for k in range(0,K):
		resk = []
		n = 0
		n_stoch = 0
		t = n*Gi.dt
		while(t < Gi.Tmax):
			etat, n_stoch = findStateAtT(t, results[k], n_stoch)
			n += 1
			t = n*Gi.dt
			resk.append(etat)
		etat, n_stoch = findStateAtT(t, results[k], n_stoch)
		n += 1
		t = n*Gi.dt
		resk.append(etat)
		res.append(resk)
	return res
	
def findStateAtT(t, simulation, n_stoch):
	N = len(simulation)
	n = n_stoch
	while((n < N) and (simulation[n][0] < t)):
		n += 1
	n -= 1
	if(n < 0):
		n = 0
	return [simulation[n][1], min(n,0)]


def printResults(results, i):
	for k in range(0,Gi.K):
	    x = []
	    yAP = []
	    for t in range(0,len(results[k])):
		x.append(t*Gi.dt)
		yAP.append(results[k][t][i])
	    plt.plot(x,yAP)
	    
def printResultsLabel(results, i, label):
	for k in range(0,Gi.K):
	    x = []
	    yAP = []
	    for t in range(0,len(results[k])):
		x.append(t*Gi.dt)
		yAP.append(results[k][t][i])
	    plt.plot(x,yAP, label = label)

def printResultsSame(results, i, moyenne):
	for k in range(0,Gi.K):
	    x = []
	    yAP = []
	    for t in range(0,len(results[k])):
		x.append(t*Gi.dt)
		yAP.append(results[k][t][i])
	    plt.plot(x,yAP, 'b')
	plt.plot(x, moyenne, 'r')
	
def giveMoments(results, ordre, index):
	K = len(results)
	N = len(results[0])
	moments = []
	for i in range(0,N):
		moment = 0
		for k in range(0,K):
			moment += (results[k][i][index])**ordre
		moment = moment/float(K)
		moments.append(moment)
	return moments
	
	
def compareInterpol(results,resultsUnif):
	N = len(results[0])
	x = []
	y = []
	for i in range(0,N):
		x.append(results[0][i][0])
		y.append(results[0][i][1][0])
	plt.plot(x,y)
	N = len(resultsUnif[0])
	x = []
	y = []
	for i in range(0,N):
		x.append(i*Gi.dt)
		y.append(resultsUnif[0][i][0])
	plt.plot(x,y)