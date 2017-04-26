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
import GillespieInput_deter as Gi

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
	results = []
else:
	input = open(Gi.dataFolder+str(Gi.seed)+'_resultsUnif.dat', 'rb')
	resultsUnif = pickle.Unpickler(input).load()
	input.close()



moyenne = []
variance = []
for j in range(Gi.N):
	moyenne.append(G.giveMoments(resultsUnif, 1, j))
	variance.append(G.giveMoments(resultsUnif, 2, j))
	delta = []
	for i in range(0, len(resultsUnif[0])):
		delta.append(math.sqrt(variance[j][i] - moyenne[j][i]**2))
#On affiche les AP
if(Gi.printAllResults):
	plt.figure()
	plt.clf()
	plt.cla()
	plt.ylabel('populations')
	plt.xlabel('time t (h)')
	plt.title(str(Gi.K) + ' simulations of the populations in function of the time')
	
	x=[]
	for t in range(0,len(resultsUnif[0])):
		x.append(t*Gi.dt)
	for i in range(Gi.N):
		plt.plot(x,moyenne[i],label=Gi.popNames[i])
		#G.printResultsMeanLabel(moyenne, i, Gi.popNames[i])
	plt.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0.)
	if(Gi.saveFigs):
		plt.savefig(Gi.dataFolder+str(Gi.seed)+'_simulations.eps')
		
#plt.figure(6)
#x=[]
#y=[]
#for i in range(len(resultsUnif[0])):
#	x.append(resultsUnif[0][i][0])
#	y.append(resultsUnif[0][i][1])
#plt.plot(x,y)
#plt.show()


#plt.figure(3)
#plt.clf()
#plt.cla()

#On affiche les AP
if(Gi.printAllResultsSame):
	for i in range(Gi.N):
		plt.figure()
		plt.clf()
		plt.cla()
		plt.ylabel('population ' + Gi.popNames[i]+'(t)')
		plt.xlabel('time t (h)')
		plt.title(str(Gi.K) + ' simulations of the ' + Gi.popNames[i]+' population in function of the time')
		G.printResultsSame(resultsUnif, i, moyenne[i])
		if(Gi.saveFigs):
			plt.savefig('DATA/'+str(Gi.seed)+'_simulationsSame_' + Gi.popNames[i]+'.eps')


#if(Gi.printMoyErrorDet):
#	x = []
#	yAP = []
#	det = []
#	for t in range(0,len(resultsUnif[0])):
#		x.append(t*Gi.dt)
#		yAP.append(moyenne[t])
#		det.append(2**(t*Gi.dt/Gi.T_AP(t*Gi.dt)))
#		#det.append(1000*math.exp(-0.5*t*Gi.dt))
#	fig, ax = plt.subplots()
#	ax.errorbar(x, yAP, yerr=delta, errorevery = 10, ecolor='y', label="Gillespie mean solution")
#	#plt.plot(x,yAP)

#	plt.plot(x,det, 'r', label="deterministic solution")
#	plt.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0.)
#	plt.ylabel('population AP(t)')
#	plt.xlabel('time t (h)')
#	plt.title("Comparison between deterministic's and Gillespie's algorithm")
#	if(Gi.saveFigs):
#		plt.savefig('DATA/'+str(Gi.seed)+'_moy_error_det.eps')

#if(Gi.computeCumulatedMeanTauAP):
	#tau*AP
#	plt.figure(5)
#	taus = []
#	x = []
#	plt.clf()
#	plt.cla()

#	for k in range(0,len(results)):
#		tau = []
#		x = []
#		for t in range(0,len(results[k])):
#			x.append(t*Gi.dt)
#			if(t == 0):
#				tau.append(results[k][t][2])
#			else:
#				tau.append((tau[t-1]*(t)+ results[k][t][2])/(t+1))
		#print(tau)
#		taus.append(tau)
#		plt.plot(x,tau)
#	plt.plot(x,[Gi.T_AP(0)]*len(x),'black',linewidth=1.2, label="limit")
#	plt.legend(bbox_to_anchor=(0.8, 0.09), loc=2, borderaxespad=0.)
#	plt.ylabel('mean of Tau*AP')
#	plt.xlabel('step n')
#	plt.title("Cumulated mean of tau*AP")
#	if(Gi.saveFigs):
#		plt.savefig('DATA/'+str(Gi.seed)+'_cumulated_TauAP.eps')
	



if(Gi.printing):
	plt.show()

