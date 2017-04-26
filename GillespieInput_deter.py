import math
#Variables de l'algorithme.
K 	 = 100	#nombre d'experiences e lancer
Tmax = 480	#Duree de l'experience (en heures ?)
Nmax = 100000 #Nombre maximal d'etapes
seed = 1223	#Graine aleatoire
dataFolder = "DATA/deter/" #la ou on enregistre les donnees et figures
# M reactions
# N especes

popNames = ["AP", "IP_1", "IP_2", "N", "Glia"] #nom de chaque population
N = len(popNames)
popIndex = dict(zip(popNames, range(N)))
populationInit = [100.,0.,0.,0.,0.] 			#populations initiales


#Reactions : les N premieres cases sont les reactants, les N autres dernieres cases sont les produits.
R=[]
reactions = []
reactions.append("1AP = 2AP")
reactions.append("1AP = 1Glia")
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
dt = 1

#booleens d'affichage/enregistrement
printing = True
printInterpol = False
printAllResults = True
printAllResultsSame = True
printMoyErrorDet = True
saveFigs = False
saveData = False
verbose = True
createDatas = True
computeCumulatedMeanTauAP = True


def alpha(t):
    alpha = 0.2
    return alpha

def beta(t):
    beta = 0.1
    return beta

def gamma(t):
    gamma = 0.1
    return gamma

def delta(t):
	delta = 0.01
	return delta

def epsilon(t):
    epsilon = 0.01
    return epsilon

def T_AP(t):
    T_AP = 29.4
    return T_AP

def T_IP_1(t):
    T_IP_1 = 29.4
    return T_IP_1

def T_IP_2(t):
    T_IP_2 = 26.2
    return T_IP_2

def c(t):
    valpha = alpha(t)
    vdelta = delta(t)
    vbeta = beta(t)
    vgamma = gamma(t)
    vepsilon = epsilon(t)
    vT_AP = T_AP(t)
    vT_IP_1 = T_IP_1(t)
    vT_IP_2 = T_IP_2(t)
    cRes = []
    cRes.append(math.log(2)*(1-vdelta)*valpha/vT_AP)
    cRes.append(math.log(2)*vdelta/vT_AP)
    cRes.append(math.log(2)*(1-vdelta)*(1-valpha)*(1-vbeta)/vT_AP)
    cRes.append(math.log(2)*(1-vdelta)*(1-valpha)*vbeta*vgamma/vT_AP)
    cRes.append(math.log(2)*(1-vdelta)*(1-valpha)*vbeta*(1-vgamma)/vT_AP)
    cRes.append(math.log(2)*vepsilon/vT_IP_1)
    cRes.append(math.log(2)*(1-vepsilon)/vT_IP_1)
    cRes.append(math.log(2)*1./vT_IP_2)
    return cRes
    
def h(population):
	return [population[popIndex["AP"]],population[popIndex["AP"]],population[popIndex["AP"]],population[popIndex["AP"]],population[popIndex["AP"]],population[popIndex["IP_1"]],population[popIndex["IP_1"]],population[popIndex["IP_2"]]]