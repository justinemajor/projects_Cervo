import numpy as np
import matplotlib.pyplot as mpl
from scipy import special
import math
from scipy.optimize import curve_fit
import pandas as pd
from tkinter.filedialog import askopenfile
import argparse
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

#Choisir la résolution étudiée et le type d'analyse
parser = argparse.ArgumentParser()
parser.add_argument("reso", type=str,
                    help="Decide the resolution of the spectrums", choices=['01', '10'])
parser.add_argument("-pca", "--pca", action="store_true",
                    help="Choose the PCA method for the analysis")
parser.add_argument("-exp", "--exp", action="store_true",
                    help="Choose the experimental method for the analysis")
parser.add_argument("-un", "--nombre", action="store_true", help="Choose if you want to show all spectrums or just one.")
args = parser.parse_args()
res = args.reso
if not args.pca and not args.exp or args.pca and args.exp:
    raise Exception("Please choose a method.")
if not args.nombre:
    num = None

#Définition des variables pertinentes
path = "/Users/justinemajor/Documents/ecole/gph.doc/stage1/documents/spectres/" + res
donnees_tot_x, ordo, donnees_tot_y = [], [], {}
nb = len(listNameOfFiles(path))

#choisir le(s) spectre(s) à afficher
if args.nombre:
    print("Choisissez le numéro de spectre à imprimer")
    num = int(input())
    if res == '01':
        if num >= nb or num < 0:
            raise Error("L'indice du spectre n'existe pas.")
    if res == '10':
        if num >= nb or num < 0:
            raise Error("L'indice du spectre n'existe pas.")
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("num", type=int,
                        help="Decide the index of one spectrum to show.", choices=np.linspace(0, nb, 1))
    args = parser.parse_args()
    num = args.num
    """

"""
print("Choisissez la résolution des spectres à étudier (temps d'intégration de 01 ou 10)")
res = str(input())
if res not in ['01', '10']:
    raise Error('Choisir entre 01 et 10.')

print("Choisir le type d'analyse (exp ou pca)")
analyse = str(input())
if analyse not in ['exp', 'pca']:
    raise Error("Choisir entre exp (pour la proportion des spectres expérimentaux de base) ou pca (pour l'utilisation des vecteurs singuliers)")

#Définition des variables pertinentes
path = "/Users/justinemajor/Documents/ecole/gph/stage1/documents/spectres/" + res
donnees_tot_x, ordo, donnees_tot_y = [], [], {}
nb = len(listNameOfFiles(path))

#choisir le(s) spectre(s) à afficher
print("N'afficher qu'un spectre ou tous? (un/tous)")
meth = str(input())
if meth == 'tous':
    num = None
"""

#création des listes de données
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

#Méthode d'analyse par composantes principales et définir la fonction ainsi que ses paramètres
if args.exp:
    pca = PCA(n_components=4)
    col = ['Concentration 1', 'Concentration 2', 'Concentration 3', 'Concentration 4']
    p = [1, 1, 1, 1]
    def fonction(X, a, b, c, d):
        i1 = listNameOfFiles(path).index(f'0001_{res}.txt')
        i2 = listNameOfFiles(path).index(f'0010_{res}.txt')
        i3 = listNameOfFiles(path).index(f'0100_{res}.txt')
        i4 = listNameOfFiles(path).index(f'1000_{res}.txt')
        return a*ordo[i1]+b*ordo[i2]+c*ordo[i3]+d*ordo[i4]

elif args.pca:
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

#Calculer les concentrations de chaque composante principale
prop = []
for i in range(len(coef)):
    tot = sum(coef[i])
    totr = []
    for it in range(len(coef[i])):
        totr.append(round(coef[i][it]/tot*100, 0))
    prop.append(totr)

prop = np.array(prop)
names = np.array([listNameOfFiles(path)])
gen = np.hstack((names.transpose(), prop))
principalDf = pd.DataFrame(data = gen, columns = ['Solution']+col)

#Tableau des concentrations et des fichiers
print(principalDf)

#reconstruction des spectres avec les vecteurs singuliers
#sp = coef@pca.components_
"""
tous = []
for i in range(nb):
    ax = f"ax{i}"
    tous.append(ax)
"""

# Afficher les données et le curvefit
if num is None:
    axs = np.arange(0, 15, 1).reshape(5, 3)
    axs = list(axs)
    for i in range(len(axs)):
        axs[i] = list(axs[i])

    fig1, axs = mpl.subplots(5, 3)

    cumul = 0
    for i in axs:
        for ii in range(3):
            if cumul <= nb-1 and res == '01' or cumul <= nb-1 and res == '10':
                i[ii].plot(donnees_tot_x, ordo[cumul], '#e377c2', label=f'Données brutes du spectre {listNameOfFiles(path)[cumul]}')
                i[ii].plot(donnees_tot_x, fonction(donnees_tot_x, *coef[cumul]), '#17becf', linestyle=':', label='Données fittées')
                i[ii].legend()
                cumul += 1
            else:
                pass

if num is not None:
    fig1, ax1 = mpl.subplots()          # Figure 1
    ax1.plot(donnees_tot_x, ordo[num], '#e377c2', label='Données brutes')                 # Données

    ax1.plot(donnees_tot_x, fonction(donnees_tot_x, *coef[num]), '#17becf', linestyle='-.', label='Données fittées')        # Curvefit #sp[num]
    ax1.set_xlabel("x") # Titre des abscisses
    ax1.set_ylabel("y") # Titre des ordonnées
    ax1.set_title("Curvefit d'un spectre")      # Titre du graphique
    ax1.legend()

# Afficher la figure
mpl.show()