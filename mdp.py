# -*- coding: utf-8 -*

from random import randint,uniform
import sys
import subprocess
from math import exp,log
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.stats

def fct(k):
    return k

def mdp(poss,popmax,generationmax,Tmutation,prob_CO=0.7, c=0.90, freq_bad=0.10, freq_rand=0.10):
    """
        Fonction principale, va effectuer la boucle principale des algos génétiques
        password : le mot de passe à retrouver
        poss : les différentes valeurs que peut prendre un chromosome
        popmax : la population à créer
        generationmax : le nombre maximale d'itération à générer
        Tmutation : le taux de mutation d'un élement
        keep : le taux de population choisie lors de la sélection, le reste sera pris au hasard
    """
    # Initialisation
    meanFitnesses = []
    bestFitnesses = []

    # Fitness max jamais rencontrée
    MAX = 0

    genes = []
    for i in range(0,popmax):
        new = []
        for j in range(0,12):
            new.append(poss[randint(0,len(poss)-1)])
        genes.append(new)

    # Main loop
    for i in range(0,generationmax):
        fit = fitness(genes)
        val = genes[fit.index(max(fit))]
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

        if i % 50 == 0:
            print(i, word)
            print("MAX :", MAX, "max :", maxi, "mean :", fit_moy)
            #fit.sort()
            #fit.reverse()
            #print(fit)
            #print(genes)


        # Selection + mutation
        genes = selection(genes,fit,prob_CO, c, freq_bad, freq_rand)
        genes = mutation(genes,Tmutation,poss)

        #Si on trouve le bon mot de passe, on quitte la boucle
        if maxi==1:
            return([WORD, meanFitnesses, bestFitnesses])

    return([WORD, meanFitnesses, bestFitnesses])


def selection(population, fitnesses, prob_CO, c = 0.90, freq_bad = 0.10, freq_rand = 0.10):
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
    # Indices des individus les plus mauvais
    #bad_indexes = np.argsort(weights)[:int(N*freq_bad)]

    # Indices des parents selectionnés aleatoirement, parmis les plus mauvais et avec la roulette
    inds_randoms = np.random.choice(range(0,N),  int(N * freq_rand))
    inds_mauvais = np.argsort(weights)[:int(N*freq_bad)]
    inds_roulette = np.random.choice(range(len(population)), N - len(inds_randoms) - len(inds_mauvais), p=weights)

    # Indices de tous les parents
    indParents = np.concatenate((inds_randoms, inds_roulette, inds_mauvais))
    np.random.shuffle(indParents)
    #print(indParents)
    i = 0
    while(i < N):
        r = random.random()
        if r < prob_CO:
            # Crossing over classique ou tirage aleatoire pour chaque caractere a partir des 2 parents
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
        result.append(fct(k))
    return result


def mutation(tab,Tmut,poss):
    """
        fontion de mutation : chaque position a une chance de Tmut d'etre muté
    """
    for k in range(len(tab)):
        for i in range(len(tab[k])):
            if uniform(0,1)<Tmut:
                r = random.random()
                if r < 0.5 or i == len(tab[k]) - 1:
                    tab[k][i] = poss[randint(0,len(poss)-1)]
                else:
                    tab[k][i], tab[k][i+1] = tab[k][i+1], tab[k][i]
    return tab

# =============================================================================
#     result = []
#     for k in tab:
#         new = []
#         for ele in k:
#             if uniform(0,1)<Tmut:
#                 new.append(poss[randint(0,len(poss)-1)])
#             else:
#                 new.append(ele)
#         result.append(new)
#     return result
# =============================================================================



#Les paramètres choisis ici ont été affinés après plusieurs essais afin de converger le plus vite possible
#Ils ne sont pas forcément optimaux

poss=[str(i) for i in range(0,10)]+['_',"A", "B", "C", "D", "E", "F", "G", "H", "I", "G", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

#La population max est assez conséquente afin de pouvoir tester beaucoup d'individus
popmax = 400

#Le nombre d'iteration max est fixé à 1000, qui est suffisant pour la plupart des exemples
generationmax = 10000000

#Le taux de mutation est assez faible mais pas trop : il faut converger vite sans pour autant créer trop d'aléatoire
Tmutation = 0.15

#Proba de crossing over entre les parents lors de la selection
prob_CO = 0.60

#Parametre lors de la selection par rang
c = 0.95

#Proportion des individus les plus mauvais gardés à chaque tour
freq_bad = 0.15

#Proportio d'individus choisis aleatoirement a chaque tour
freq_rand = 0.10



results = mdp(poss,popmax,generationmax,Tmutation,prob_CO, c, freq_bad, freq_rand)


# =============================================================================
# def selection(tab,fit,keep):
#     """
#         Fonction de sélection en fonction de la fitness de chaque élement
#         Reprendre une roulette de choix dont chaque partie a plus ou moins de chance d'être selectionnée
#         Si keep < 1, une part de la nouvelle génération sera sélectionnée aléatoirement
#     """
#     tab = tab[:]
#     result = []
#     tailleMax= len(tab)
#     fitPond = [k for k in fit]
#     fitMax = sum(fitPond)
#     for i in range(0,int(keep*tailleMax)):
#         val = 0.0
#         choix = uniform(0,fitMax)
#         j = 0
#         while val<choix:
#             val+=fitPond[j]
#             j+=1
#         j-=1
#         result.append(tab[j])
#     while(len(result)<tailleMax):
#         result.append(tab[randint(0,tailleMax-1)])
#     return result
# =============================================================================




# =============================================================================
# def croisement(tab):
#     """
#         Implémentation du croisement génétique
#         On coupe à une position aléatoire les deux gènes et
#         la partie gauche de l'un va aller avec la partie droite de l'autre afin de créer un nouveau gènes
#     """
#     result = []
#     for i in range(0,len(tab),2):
#         pos1,pos2 = randint(0,len(tab)-1),randint(0,len(tab)-1)
#         while(pos1==pos2):
#             pos2 = randint(0,len(tab)-1)
#         val = randint(0,len(tab[0])-1)
#         new1 = tab[pos1][0:val] + tab[pos2][val:]
#         new2 = tab[pos2][0:val] + tab[pos1][val:]
#         result.append(new1)
#         result.append(new2)
#     return result
# =============================================================================
