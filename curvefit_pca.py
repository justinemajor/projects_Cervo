import numpy as np
import matplotlib.pyplot as mpl
from scipy import special
import math
from shapely.geometry import LineString
from scipy.optimize import curve_fit
import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from tkinter import *

#lire les données
def listNameOfFiles(directory: str, extension="txt") -> list:
    foundFiles = []
    for file in os.listdir(directory):
        if fnmatch.fnmatch(file, f'*.{extension}'):
            foundFiles.append(file)
    return foundFiles

def getFilePaths(directory: str, fileNames: list) -> list:
    filesWithFullPath = []
    for fileName in fileNames:
        filesWithFullPath.append(directory+"/"+fileName)
    return filesWithFullPath

#Choisir la résolution étudiée et le type d'analyse
print("Choisissez la résolution des spectres à étudier (temps d'intégration de 01 ou 10)")
res = str(input())
if res not in ['01', '10']:
    raise Error('Choisir entre 01 et 10.')

print("Choisir le type d'analyse (exp ou pca)")
analyse = str(input())
if analyse not in ['exp', 'pca']:
    raise Error("Choisir entre exp (pour la proportion des spectres expérimentaux de base) ou pca (pour l'utilisation des vecteurs singuliers)")

#choisir le spectre à afficher
print("Choisissez le numéro de spectre à imprimer")
num = int(input())
if res == '01':
    if num >= 13 or num < 0:
        raise Error("L'indice du spectre n'existe pas.")
if res == '10':
    if num >= 14 or num < 0:
        raise Error("L'indice du spectre n'existe pas.")

path = "/Users/justinemajor/Documents/gph.doc/stage1/documents/spectres/" + res
donnees_tot_x, ordo, donnees_tot_y = [], [], {}
nb = len(listNameOfFiles(path))

for nom in listNameOfFiles(path):
    # Nom du fichier à importer
    fich = open(path + '/' + nom, "r")
    test_str = list(fich)[14:]
    fich.close()
    x, y = [], []
    # Nettoyer les informations
    for j in test_str:
        elem_str = j.replace(",", ".").replace("\n", "").replace("\t", ",")
        elem = elem_str.split(",")
        x.append(float(elem[0]))
        y.append(float(elem[1]))

    donnees_tot_x = np.array(x)
    ordo.append(y)
    donnees_tot_y[nom] = y

ordo = np.array(ordo)
pca = np.array([])
col = []
p = []
print(analyse)

#Méthode d'analyse par composantes principales et définir la fonction ainsi que ses paramètres
if analyse == 'exp':
    print('hello')
    pca = PCA(n_components=4)
    col = ['Concentration 1', 'Concentration 2', 'Concentration 3', 'Concentration 4']
    p = [1, 1, 1, 1]
    def fonction(X, a, b, c, d):
        i1 = listNameOfFiles(path).index(f'0001_{res}.txt')
        i2 = listNameOfFiles(path).index(f'0010_{res}.txt')
        i3 = listNameOfFiles(path).index(f'0100_{res}.txt')
        i4 = listNameOfFiles(path).index(f'1000_{res}.txt')
        return a*ordo[i1]+b*ordo[i2]+c*ordo[i3]+d*ordo[i4]

elif analyse == 'pca':
    pca = PCA(n_components=5)
    col = ['Concentration 1', 'Concentration 2', 'Concentration 3', 'Concentration 4', 'Concentration 5']
    p = [1, 1, 1, 1, 1]
    def fonction(X, a, b, c, d, e):
        return a*pca.components_[0]+b*pca.components_[1]+c*pca.components_[2]+d*pca.components_[3]+e*pca.components_[4]

else :
    raise TypeError("La méthode d'analyse n'est pas reconnue")

principalCoefficients = pca.fit_transform(ordo)

#Matrice des coefficients
coef = []
for i in range(nb):
    popt = []
    pcov = []
    popt, pcov = curve_fit(fonction, donnees_tot_x, ordo[i], p0=p)
    coef.append(popt)

coef = np.array(coef)

"""
tot = sum(coef[num])
print(coef[num]/tot)
print(listNameOfFiles(path)[num])
"""

#Calculer les concentrations de chaque composante principale
prop = []
for i in range(len(coef)):
    tot = sum(coef[i])
    totr = []
    for it in range(len(coef[i])):
        totr.append(round(coef[i][it]/tot, 3))
    prop.append(totr)

prop = np.array(prop)
principalDf = pd.DataFrame(data = prop, columns = col)

#Tableau des concentrations
print(principalDf)

elements = pd.DataFrame(data = listNameOfFiles(path), columns=['Solutions'])
print(elements)

#reconstruction des spectres avec les vecteurs singuliers
#sp = coef@pca.components_

# Afficher les données et le curvefit
fig1, ax1 = mpl.subplots()          # Figure 1
ax1.plot(donnees_tot_x, ordo[num], 'r', label='Données brutes')                 # Données

ax1.plot(donnees_tot_x, fonction(donnees_tot_x, *coef[num]), 'b', label='Données fittées')        # Curvefit #sp[num]
ax1.set_xlabel("x") # Titre des abscisses
ax1.set_ylabel("y") # Titre des ordonnées
ax1.set_title("Curvefit d'un spectre")      # Titre du graphique
ax1.legend()

# Afficher la figure
mpl.show()