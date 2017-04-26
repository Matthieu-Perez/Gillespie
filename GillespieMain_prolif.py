import random as rd
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['errorbar.capsize'] = 3

import pickle
#print(mpl.rcParams.keys())

import GillespieLib as G
#import GillespieInput_loktaVolterra as Gi
import GillespieInput_prolif as Gi

#Resultats : (k)x[(t)x(AP IP1 IP2 N)x(tau*AP)]
results = []

if(Gi.verbose):
	G.printInfo()

if(Gi.createDatas):
	rd.seed(Gi.seed)
	for k in range(0,Gi.K):
	    seedUnique = rd.randint(1,max(100000,Gi.K))
	    results.append(G.experience(seedUnique)) #On lance toutes les experiences
 
	#On se remet sur une grille de pas dt    
	resultsUnif = G.translateResults(results)

	if(Gi.printInterpol):
		plt.figure(1)
		plt.clf()
		plt.cla()
		G.compareInterpol(results,resultsUnif)
	if(Gi.saveData):
		output = open('DATA/'+str(Gi.seed)+'_resultsUnif.dat', 'wb')
		pickle.Pickler(output).dump(resultsUnif)
		output.close()
else:
	input = open('DATA/'+str(Gi.seed)+'_resultsUnif.dat', 'rb')
	resultsUnif = pickle.Unpickler(input).load()
	input.close()




#On affiche les AP
if(Gi.printAllResults):
	plt.figure(2)
	plt.clf()
	plt.cla()
	plt.ylabel('population AP(t)')
	plt.xlabel('time t (h)')
	plt.title(str(Gi.K) + ' simulations of the AP population in function of the time')
	G.printResults(resultsUnif, 0)
	G.printResults(resultsUnif, 1)
	if(Gi.saveFigs):
		plt.savefig('DATA/'+str(Gi.seed)+'_simulations.eps')
		
#plt.figure(6)
#x=[]
#y=[]
#for i in range(len(resultsUnif[0])):
#	x.append(resultsUnif[0][i][0])
#	y.append(resultsUnif[0][i][1])
#plt.plot(x,y)
#plt.show()

moyenne = G.giveMoments(resultsUnif, 1, 0)
variance = G.giveMoments(resultsUnif, 2, 0)
delta = []
for i in range(0, len(resultsUnif[0])):
	delta.append(math.sqrt(variance[i] - moyenne[i]**2))

#plt.figure(3)
#plt.clf()
#plt.cla()

#On affiche les AP
if(Gi.printAllResultsSame):
	plt.figure(3)
	plt.clf()
	plt.cla()
	plt.ylabel('population AP(t)')
	plt.xlabel('time t (h)')
	plt.title(str(Gi.K) + ' simulations of the AP population in function of the time')
	G.printResultsSame(resultsUnif, 0, moyenne)
	if(Gi.saveFigs):
		plt.savefig('DATA/'+str(Gi.seed)+'_simulationsSame.eps')


if(Gi.printMoyErrorDet):
	
	x = []
	yAP = []
	det = []
	for t in range(0,len(resultsUnif[0])):
		x.append(t*Gi.dt)
		yAP.append(moyenne[t])
		det.append(2**(t*Gi.dt/Gi.T_AP(t*Gi.dt)))
		#det.append(1000*math.exp(-0.5*t*Gi.dt))
	fig, ax = plt.subplots()
	ax.errorbar(x, yAP, yerr=delta, errorevery = 10, ecolor='y', label="Gillespie mean solution")
	#plt.plot(x,yAP)

	plt.plot(x,det, 'r', label="deterministic solution")
	plt.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0.)
	plt.ylabel('population AP(t)')
	plt.xlabel('time t (h)')
	plt.title("Comparison between deterministic's and Gillespie's algorithm")
	if(Gi.saveFigs):
		plt.savefig('DATA/'+str(Gi.seed)+'_moy_error_det.eps')

if(Gi.computeCumulatedMeanTauAP):
	#tau*AP
	plt.figure(5)
	taus = []
	x = []
	plt.clf()
	plt.cla()

	for k in range(0,len(results)):
		tau = []
		x = []
		for t in range(0,len(results[k])):
			x.append(t*Gi.dt)
			if(t == 0):
				tau.append(results[k][t][2])
			else:
				tau.append((tau[t-1]*(t)+ results[k][t][2])/(t+1))
		#print(tau)
		taus.append(tau)
		plt.plot(x,tau)
	plt.plot(x,[Gi.T_AP(0)]*len(x),'black',linewidth=1.2, label="limit")
	plt.legend(bbox_to_anchor=(0.8, 0.09), loc=2, borderaxespad=0.)
	plt.ylabel('mean of Tau*AP')
	plt.xlabel('step n')
	plt.title("Cumulated mean of tau*AP")
	if(Gi.saveFigs):
		plt.savefig('DATA/'+str(Gi.seed)+'_cumulated_TauAP.eps')
	



if(Gi.printing):
	plt.show()

