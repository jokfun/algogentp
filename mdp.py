# -*- coding: utf-8 -*

from random import randint,uniform
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.stats

def phenotypes_to_genotypes(phenotypes, poss):
    """
        Converti une liste de phenotypes d'individus en une liste de genotypes correspondant
        Un element du phenotype est traduit en gene par son indice dans la liste des elements phenotypiques possibles
        phenotypes : liste de phenotypes
        poss : liste des caracteres possibles des phenotypes
    """
    genotypes = []
    for phenotype in phenotypes:
        genome = []
        for char in phenotype:
            genome.append(poss.index(char))
        genotypes.append(genome)
    return genotypes

def genotypes_to_phenotypes(genotypes, poss):
    """
        Converti une liste de genotypes d'individus en une liste de phenotypes correspondant
        genotypes : liste de genotypes
        poss : liste des caracteres possibles des phenotypes
    """
    phenotypes = []
    for genotype in genotypes:
        phenotype = []
        for gene in genotype:
            phenotype.append(poss[gene])
        phenotypes.append(phenotype)
    return phenotypes

def mdp(poss,popmax,generationmax,Tmutation,prob_CO=0.7, c=0.90, freq_bad=0.10, freq_rand=0.10):
    """
        Fonction principale, va effectuer la boucle principale des algos génétiques
        poss : les différentes valeurs possibles des briques elementaires du phenotype
        popmax : Nb d'individus à creer
        generationmax : le nombre maximale d'itération à générer
        Tmutation : le taux de mutation d'un élement du genotype
        prob_CO : probabilité que 2 individus choisis lors de la selection font un crossing over
        freq_bad : proportion de mauvais individus selectionné lors de la selection
        freq_rand : proportion de individus selectionné au hasard lors de la selection
    """
    # On sauvegrade les fitness max et moyenne a chaque generation dans ces listes
    meanFitnesses = []
    bestFitnesses = []

    # Fitness max jamais rencontrée au cours de la simulation
    MAX = 0

    # Initialisation aléatoire des phenotypes des individus
    phenotypes = []
    for i in range(0,popmax):
        new = []
        for j in range(0,12):
            new.append(poss[randint(0,len(poss)-1)])
        phenotypes.append(new)


    for i in range(0,generationmax):
        # Main loop

        # Fitness des individus
        fit = fitness(phenotypes)
        # On sauvegarde le meilleurs mdp, la fitness max et moyenne
        val = phenotypes[fit.index(max(fit))]
        maxi = max(fit)
        word = ""
        for k in val:
            word+=k
        if maxi > MAX:
            MAX = maxi
            WORD = word
        fit_moy = np.mean(fit)
        bestFitnesses.append(maxi)
        meanFitnesses.append(fit_moy)

        # Print toutes les 50 générations
        if i % 50 == 0:
            print(i, word)
            print("MAX :", MAX, "max :", maxi, "mean :", fit_moy)

        # Converti les phenotypes des individus en genotypes
        genotypes = phenotypes_to_genotypes(phenotypes, poss)
        # Selection + mutation (sur les genotypes)
        genotypes = selection(genotypes,fit,prob_CO, c, freq_bad, freq_rand)
        genotypes = mutation(genotypes,Tmutation,poss)
        # Reconversion en phenotypes
        phenotypes = genotypes_to_phenotypes(genotypes, poss)

        #Si on trouve le bon mot de passe, on quitte la boucle
        if maxi==1:
            return([WORD, meanFitnesses, bestFitnesses])

    return([WORD, meanFitnesses, bestFitnesses])


def selection(population, fitnesses, prob_CO, c = 0.90, freq_bad = 0.10, freq_rand = 0.10):
    """
        Fonction de selection par les individus
        Une proportion freq_bad des individus sont selectionnés parmis les plus mauvais individus
        Une proportion freq_rand des individus sont selectionnés au hasard
        Le reste sont selectionnés à l'aide d'une roulette exponentielle par rang
        Les individus selectionnes sont ensuite parcouru aleatoirement 2 par 2 et ont chance de prob_CO
        de réaliser un crossing over pour donner les enfants
        population : liste de genotype
        fitnesses : liste des fitness des individus
    """
    newGeneration = [] # Nouveaux indvidus apres selection
    N = len(population) # Nb d'individus

    # Construction de la matrice des poids (selection par le rang)
    weights = []
    rangs = scipy.stats.rankdata(fitnesses)
    for r in rangs:
        # Exponentielle
        weights.append((c - 1) * c**(N - r) / (c**N - 1))
        # Lineaire
        #weights.append(2 * (r -1) / (N * (N-1)))

    # Applique un scalaire pour que la somme des poids = 1
    weights = np.array(weights) / sum(weights)

    # Indices des parents selectionnés aleatoirement, parmis les plus mauvais et avec la roulette
    inds_randoms = np.random.choice(range(0,N),  int(N * freq_rand))
    inds_mauvais = np.argsort(weights)[:int(N*freq_bad)]
    inds_roulette = np.random.choice(range(len(population)), N - len(inds_randoms) - len(inds_mauvais), p=weights)

    # Indices de tous les parents
    indParents = np.concatenate((inds_randoms, inds_roulette, inds_mauvais))
    np.random.shuffle(indParents) # Melange
    i = 0
    while(i < N):
        r = random.random()
        if r < prob_CO:
            # Crossing over classique ou tirage aleatoire pour chaque caractere a partir des 2 parents
            # 1 chance sur 2 pour les 2 méthodes
            r2 = random.random()
            if r2 < 0.5:
                enfant1 = []
                enfant2 = []
                for ind in range(len(population[0])):
                    rand = random.random()
                    if rand < 0.5:
                        enfant1.append(population[indParents[i]][ind])
                        enfant2.append(population[indParents[i+1]][ind])
                    else:
                        enfant1.append(population[indParents[i]][ind])
                        enfant2.append(population[indParents[i+1]][ind])
            else:
                k = random.randint(1,12)
                #print(population[indParents[0]])
                enfant1 = population[indParents[i]][:k] + population[indParents[i+1]][k:]
                enfant2 = population[indParents[i]][:k] + population[indParents[i+1]][k:]
                #print('ENFANTS :', enfant1, enfant2)

        else:
            # Pas de crossing over
            enfant1 = population[indParents[i]]
            enfant2 = population[indParents[i+1]]

        newGeneration.append(enfant1)
        newGeneration.append(enfant2)
        i += 2

    return newGeneration


def fitness(tab):
    """
        Créer la fitness de chaque élement en fonction de la distance de chacun au password
        tab : liste des phenotypes
    """
    result = []
    execute = ['./ibi_2018-2019_fitness_linux', "10"]
    for k in tab:
        mot = ""
        for i in k:
            mot+=i
        execute.append(mot)
    val = str(subprocess.check_output(execute))
    val = val.split("\\n")
    for i in range(0,len(val)-1):
        val[i] = float((val[i].split("t"))[1])
    val = val[:-1]
    for k in val:
        result.append(k)
    return result


def mutation(genomes,Tmut,poss):
    """
        fontion de mutation : chaque position a une chance de Tmut d'etre muté
        genomes : liste de genotypes
        poss : liste des caracteres possible pour le phenotype
        si un gene mute, sa valeur est incrementée d'une loi normal de moyenne 0 et d'un ecart type de 10
    """
    for k in range(len(genomes)):
        for i in range(len(genomes[k])):
            if uniform(0,1)<Tmut:
                r = random.random()
                if r < 0.95 or i == len(genomes[k]) - 1:
                    genomes[k][i] = (int(np.random.normal(genomes[k][i], 10))%len(poss))
                else:
                    genomes[k][i], genomes[k][i+1] = genomes[k][i+1], genomes[k][i]
    return genomes



#Les paramètres choisis ici ont été affinés après plusieurs essais afin de converger le plus vite possible
#Ils ne sont pas forcément optimaux
poss=["A", "B", "C", "D", "E", "F", "G", "H", "I", "G", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] + [str(i) for i in range(0,10)] + ["_"]

#La population max est assez conséquente afin de pouvoir tester beaucoup d'individus
popmax = 400

#Nb de generations
generationmax = 10000000

#On met un taux de mutation assez elevé pour brasser l'ensemble des phenotypes possibles
Tmutation = 0.15

#Proba de crossing over entre les parents lors de la selection
prob_CO = 0.75

#Parametre lors de la selection par rang (on conserve en priorité les meilleurs individus)
c = 0.95

#Proportion des individus les plus mauvais gardés à chaque tour
freq_bad = 0.15

#Proportio d'individus choisis aleatoirement a chaque tour
freq_rand = 0.05


results = mdp(poss,popmax,generationmax,Tmutation,prob_CO, c, freq_bad, freq_rand)


#%% Plot fitness max et moyenne au cours des generations
plt.plot(results[1])
plt.plot(results[2])
plt.legend(['fitness moyenne' ,'fitness max'])
plt.xlabel('generation')
plt.ylabel('fitness')
plt.savefig('./fitness.png')
plt.show()

print('mot de passe :', results[0])





