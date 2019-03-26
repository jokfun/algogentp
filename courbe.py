from math import exp
from random import randint
import os

#On créé l'alphabet du type [A-Z_0-9]


alphabet = map(chr, range(65, 91))
poss= [k for k in alphabet]+["_"]+[str(i) for i in range(10)]


#mot de passe original
mdp = "_CH3NI_P4N__"

#la fonction à exécuter
classique = "ibi_2018-2019_fitness_windows.exe 10"

def toString(lst):
    """
        On va convertir le tableau en String
    """
    res = ""
    for k in lst:
        res+=" "+k
    return res

def plusproche(mdp,alphabet):
    """
        Fonction du plus proche caractère, suivant l'aphabet utilisé
        ex : A et C sont plus proches que A et D
    """
    result = [mdp]
    for i in range(len(mdp)):
        pos = alphabet.index(mdp[i])
        if pos == len(alphabet)-1:
            pos=0
        else:
            pos+=1
        mdp = list(mdp)
        mdp[i] = alphabet[pos]
        mdp = ''.join(mdp)
        result.insert(0,mdp)
    return result

def plusloin(mdp,alphabet):
    """
        Fonction du plus proche caractère, suivant l'aphabet utilisé
        ex : A et D sont plus éloignés que A et C
    """
    loin = int(len(alphabet)/2)
    result = [mdp]
    for i in range(len(mdp)):
        pos = alphabet.index(mdp[i])
        if pos+loin >= len(alphabet):
            pos=pos+loin-len(alphabet)
        else:
            pos+=loin
        mdp = list(mdp)
        mdp[i] = alphabet[pos]
        mdp = ''.join(mdp)
        result.insert(0,mdp)
    return result

def aleatoire(mdp,alphabet):
    """
        Les char sont générés aléatoirement
        On a donc des distances aléatoires
    """
    loin = int(len(alphabet)/2)
    result = [mdp]
    for i in range(len(mdp)):
        pos = randint(0,len(alphabet)-1)
        mdp = list(mdp)
        mdp[i] = alphabet[pos]
        mdp = ''.join(mdp)
        result.insert(0,mdp)
    return result

def alletter(mdp,alphabet):
    for i in range(len(mdp)):
        pos = alphabet.index(mdp[i])
        if pos-18 < 0:
            pos=len(alphabet)-1-abs(pos-18)
        else:
            pos=pos-18
        mdp = list(mdp)
        mdp[i] = alphabet[pos]
        mdp = ''.join(mdp)
        print(mdp)
    print(alphabet)
    result = []
    for i in range(len(mdp)):
        pos = alphabet.index(mdp[i])
        for j in range(0,19):
            if pos==len(alphabet)-1:
                pos = 0
            mdp = list(mdp)
            mdp[i] = alphabet[pos]
            mdp = ''.join(mdp)
            result.append(mdp)
            pos+=1
            print(mdp)
        """
        cop = mdp
        for j in range(int(len(alphabet)/2)):
            pos = alphabet.index(mdp[i])
            if j+pos > len(alphabet)-1:
                pos+=j-len(alphabet)
            else:
                pos+=j
            #print(pos)
            cop = mdp[:]
            cop = list(cop)
            cop[i] = alphabet[pos]
            cop = ''.join(cop)
            """
    return result

def add(tab):
    """
        On créé un nouvel axe au graphique suivant la fonction de procimité utilisé
    """
    proche = toString(tab)
    result = os.popen(classique+proche).read()
    result = result.split("\n")

    absc = []
    ordo = []

    for i in range(0,len(result)-1):
        val = result[i]
        val = val.split("\t")
        val = [val[0],float(val[1])]
        result[i] = val
        absc.append(i+1)
        ordo.append(float(val[1]))
    return absc,ordo

import matplotlib.pyplot as plt

"""
proche = plusproche(mdp,poss)
absc,ordo = add(proche)
plt.plot(absc, ordo,'b',label="plus proche")

proche = plusloin(mdp,poss)
absc,ordo = add(proche)
plt.plot(absc, ordo,'r',label="plus loin")

proche = aleatoire(mdp,poss)
absc,ordo = add(proche)
plt.plot(absc, ordo,'g',label="aleatoire")
"""
proche = alletter(mdp,poss)
absc,ordo = add(proche)
plt.plot(absc, ordo,'ro',label="fitness evolution")
#plt.plot(absc, ordo,'r')

plt.legend()
plt.show()
