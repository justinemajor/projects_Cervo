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

path = "/Users/justinemajor/Documents/gph.doc/stage1/documents/spectres/10"
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

pca = PCA(n_components=5)
principalCoefficients = pca.fit_transform(ordo)

# Définir la fonction ainsi que ses paramètres
def fonction(X, a, b, c, d, e):
    return a*pca.components_[0]+b*pca.components_[1]+c*pca.components_[2]+d*pca.components_[3]+e*pca.components_[4]

coef = []
for i in range(nb):
    popt = []
    pcov = []
    popt, pcov = curve_fit(fonction, donnees_tot_x, ordo[i], p0=[1000, 1000, 1000, 1000, 1000])
    coef.append(popt)

coef = np.array(coef)

sp = coef@pca.components_

# Afficher les données et le curvefit
fig1, ax1 = mpl.subplots()          # Figure 1
ax1.plot(donnees_tot_x, ordo[5], 'r')                 # Données

ax1.plot(donnees_tot_x, sp[5], 'b')        # Curvefit
ax1.set_xlabel("x") # Titre des abscisses
ax1.set_ylabel("y") # Titre des ordonnées
ax1.set_title("Curvefit d'un spectre")      # Titre du graphique

# Afficher la figure
mpl.show()