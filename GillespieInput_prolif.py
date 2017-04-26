#Variables de l'algorithme.
K 	 = 100	#nombre d'experiences e lancer
Tmax = 10 	#Duree de l'experience (en heures ?)
Nmax = 100000 #Nombre maximal d'etapes
seed = 1201	#Graine aleatoire
# M reactions
# N especes

popNames = ["AP", "IP_1", "IP_2", "N"] #nom de chaque population
N = len(popNames)
popIndex = dict(zip(popNames, range(N)))
populationInit = [1.,0,1.,0] 			#populations initiales


#Reactions : les N premieres cases sont les reactants, les N autres dernieres cases sont les produits.
R=[]
reactions = []
#R.append([1,0,0,0,0,0,0,1])#
#R.append([1,0,0,0,2,0,0,0])
#R.append([1,0,0,0,1,0,0,1])
#R.append([1,0,0,0,1,1,0,0])
#R.append([1,0,0,0,1,0,1,0])
#R.append([0,1,0,0,0,2,0,0])
#R.append([0,1,0,0,0,0,2,0])
#R.append([0,0,1,0,0,0,0,2])
reactions.append("1AP = 2AP")
reactions.append("1AP = 1AP + 1N")
reactions.append("1AP = 1AP + 1IP_1")
reactions.append("1AP = 1AP + 1IP_2")
reactions.append("1IP_1 = 2IP_1")
reactions.append("1IP_1 = 2IP_2")
reactions.append("1IP_2 = 2N")


def translateReactions(reactions):
	for reaction in reactions:
		reac = [0]*(2*N)
		reactants,produits = reaction.rstrip().replace(" ","").split("=")
		reactants = reactants.split("+")
		produits = produits.split("+")
		for r in reactants:
			for s in popNames:
				if(len(r.split(s)) != 1):
					reac[popIndex[s]] = float(r.split(s)[0])
		
		for p in produits:
			for s in popNames:
				if(len(p.split(s)) != 1):
					reac[popIndex[s]+N] = float(p.split(s)[0])
		
		R.append(reac)
	return R


R = translateReactions(reactions)
M = len(R)


#pas de temps dans la representation "deterministe"
dt = 0.01

#booleens d'affichage/enregistrement
printing = True
printInterpol = False
printAllResults = True
printAllResultsSame = False
printMoyErrorDet = True
saveFigs = True
saveData = True
verbose = True
createDatas = True
computeCumulatedMeanTauAP = True


def alpha(t):
    alpha = 0.693147181
    return alpha

def beta(t):
    beta = 0
    return beta

def gamma(t):
    gamma = 0
    return gamma

def epsilon(t):
    epsilon = 0
    return epsilon

def T_AP(t):
    T_AP = 1
    return T_AP

def T_IP_1(t):
    T_IP_1 = 12
    return T_IP_1

def T_IP_2(t):
    T_IP_2 = 12
    return T_IP_2

def c(t):
    valpha = alpha(t)
    vbeta = beta(t)
    vgamma = gamma(t)
    vepsilon = epsilon(t)
    vT_AP = T_AP(t)
    vT_IP_1 = T_IP_1(t)
    vT_IP_2 = T_IP_2(t)
    cRes = []
    cRes.append(valpha/vT_AP)
    cRes.append(0)#(1-valpha)*(1-vbeta)/vT_AP)
    cRes.append(0)#(1-valpha)*vbeta*vgamma/vT_AP)
    cRes.append(0)#(1-valpha)*vbeta*(1-vgamma)/vT_AP)
    cRes.append(valpha/vT_AP)#vepsilon/vT_IP_1)
    cRes.append(0)#(1-vepsilon)/vT_IP_1)
    cRes.append(0)#1./vT_IP_2)
    return cRes
    
def h(population):
	return [population[0],0,0,0,population[1],0,0]