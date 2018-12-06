# -*- coding: utf-8 -*

from random import randint,uniform
import sys
import subprocess
from math import exp,log

def fnc(k):
	return 2**(5*(1)
def mdp(password,poss,popmax,generationmax,Tmutation,keep):
	"""
		Fonction principale, va effectuer la boucle principale des algos génétiques
		password : le mot de passe à retrouver
		poss : les différentes valeurs que peut prendre un chromosome
		popmax : la population à créer
		generationmax : le nombre maximale d'itération à générer
		Tmutation : le taux de mutation d'un élement
		keep : le taux de population choisie lors de la sélection, le este sera pris au hasard
	"""
	taille = len(password)
	genes = []
	for i in range(0,popmax):
		new = []
		for j in range(0,12):
			new.append(poss[randint(0,len(poss)-1)])
		genes.append(new)
	#print(genes)
	for i in range(0,generationmax):
		fit = fitness(genes,password)
		val = genes[fit.index(max(fit))]
		maxi = max(fit)
		
		word = ""
		for k in val:
			word+=k
		print("Best :",word," score :",maxi)
		genes = selection(genes,fit,keep)
		genes = croisement(genes)
		genes = mutation(genes,Tmutation,poss)

		#Si on trouve le bon mot de passe, on quitte la boucle
		if maxi==2:
			break
		

def distance(tab1,tab2):
	"""
		fonction de distance entre deux mots, elle est exponentielle, en effet on a f(x) = 2^x
		best retournera True si il y a un match parfait
	"""
	
	val = subprocess.check_output(['./ibi_2018-2019_fitness_linux', "10", "XXXXXXXXXXXX"])
	val = float((str(val).split("\\")[1])[1:])
	"""
	tot = 1
	best = True
	for i in range(0,len(tab1)):
		if tab1[i] == tab2[i]:
			tot*=2
		else:
			best = False
	"""
	if val == 1:
		best=True
	else:
		best=False
	
	return val,best

def selection(tab,fit,keep):
	"""
		Fonction de sélection en fonction de la fitness de chaque élement
		Reprendre une roulette de choix dont chaque partie a plus ou moins de chance d'être selectionnée
		Si keep < 1, une part de la nouvelle génération sera sélectionnée aléatoirement
	"""
	tab = tab[:]
	result = []
	tailleMax= len(tab)
	fitPond = [k for k in fit]
	fitMax = sum(fitPond)
	for i in range(0,int(keep*tailleMax)):
		val = 0.0
		choix = uniform(0,fitMax)
		j = 0
		while val<choix:
			val+=fitPond[j]
			j+=1
		j-=1
		result.append(tab[j])
	while(len(result)<tailleMax):
		result.append(tab[randint(0,tailleMax-1)])
	return result

def fitness(tab,mdp):
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
		result.append(fnc(k))
	return result	
	
def mutation(tab,Tmut,poss):
	"""
		Fonction implémententant la mutation génétique
	"""
	result = []
	for k in tab:
		new = []
		for ele in k:
			if uniform(0,1)<Tmut:
				new.append(poss[randint(0,len(poss)-1)])
			else:
				new.append(ele)
		result.append(new)
	return result

def croisement(tab):
	"""
		Implémentation du croisement génétique
		On coupe à une position aléatoire les deux gènes et 
		la partie gauche de l'un va aller avec la partie droite de l'autre afin de créer un nouveau gènes
	"""
	result = []
	for i in range(0,len(tab),2):
		pos1,pos2 = randint(0,len(tab)-1),randint(0,len(tab)-1)
		while(pos1==pos2):
			pos2 = randint(0,len(tab)-1)
		val = randint(0,len(tab[0])-1)
		new1 = tab[pos1][0:val] + tab[pos2][val:]
		new2 = tab[pos2][0:val] + tab[pos1][val:]
		result.append(new1)
		result.append(new2)
	return result	
	
	
	


#Les paramètres choisis ici ont été affinés après plusieurs essais afin de converger le plus vite possible
#Ils ne sont pas forcément optimaux

poss=[str(i) for i in range(0,10)]+['_',"A", "B", "C", "D", "E", "F", "G", "H", "I", "G", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
password='salut_alexis_pister'
if (len(sys.argv)>=2):
	password = sys.argv[1]
	
#La population max est assez conséquente afin de pouvoir tester beaucoup d'individus
popmax=100

#Le nombre d'iteration max est fixé à 1000, qui est suffisant pour la plupart des exemples
generationmax = 100000

#Le taux de mutation est assez faible mais as trop : il faut converger vite sans pour autant créer trop d'aléatoire
Tmutation = 0.01

#Dans la sélection, on gardera 80% de la population sélectionnée, le reste sera pris aléatoirement
keep = 0.70

mdp(password,poss,popmax,generationmax,Tmutation,keep)
