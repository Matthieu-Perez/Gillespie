#Variables de l'algorithme.
K 	 = 1	#nombre d'experiences e lancer
Tmax = 10	#Duree de l'experience (en heures ?)
Nmax = 1000000 #Nombre maximal d'etapes
seed = 1001	#Graine aleatoire
# M reactions
# N especes

popNames = ["proie", "predateur"] #nom de chaque population
N = len(popNames)
popIndex = dict(zip(popNames, range(N)))
populationInit = [1000.,1000.] 			#populations initiales


#Reactions : les N premieres cases sont les reactants, les N autres dernieres cases sont les produits.
R=[]
reactions = []
reactions.append("1proie = 2proie")
reactions.append("1proie + 1predateur = 2predateur") 
reactions.append("1predateur = ") #mort naturelle predateurs


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
dt = 0.001

#booleens d'affichage/enregistrement
printing = True
printInterpol = False
printAllResults = True
printAllResultsSame = False
printMoyErrorDet = False
saveFigs = False
saveData = False
verbose = True
createDatas = False
computeCumulatedMeanTauAP = False


def alpha(t):
    alpha = 1.
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
    T_AP = 10
    return T_AP

def T_IP_1(t):
    T_IP_1 = 12
    return T_IP_1

def T_IP_2(t):
    T_IP_2 = 12
    return T_IP_2

def c(t):
    cRes = []
    cRes.append(10)
    cRes.append(0.01)
    cRes.append(10)
    return cRes
    
def h(population):
	return [population[popIndex["proie"]], population[popIndex["proie"]]*population[popIndex["predateur"]], population[popIndex["predateur"]]]