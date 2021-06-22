import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as mpl

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

res = '10'
path = "/Users/justinemajor/Documents/ecole/gph/stage1/documents/spectres/" + res
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

    donnees_tot_x = x
    ordo.append(y)
    donnees_tot_y[nom] = y

#méthode d'analyse par les composantes principales, création de la matrice des coefficients
pca = PCA(0.99)
principalCoefficients = pca.fit_transform(ordo)
principalComponents = np.array(pca.components_)
inverse = np.linalg.pinv(principalComponents)
moy = np.array(pca.mean_)
m = moy@inverse
coefs = principalCoefficients + m
#print(sum(pca.explained_variance_ratio_))

#Calculer les concentrations de chaque composante principale
col = ['Concentration 1', 'Concentration 2', 'Concentration 3', 'Concentration 4', 'Concentration 5']
prop = []
for i in range(len(coefs)):
    tot = sum(coefs[i])
    totr = []
    for it in range(len(coefs[i])):
        totr.append(round(coefs[i][it]/tot*100, 0))
    prop.append(totr)

prop = np.array(prop)
names = np.array([listNameOfFiles(path)])
gen = np.hstack((names.transpose(), prop))


#Créer le tableau des concentrations à afficher
if len(pca.components_) == 5:
    principalDf = pd.DataFrame(data=gen, columns=['Solution'] + col)
    pd.set_option('display.max_columns', None)
    principalDf.head()
    print(principalDf)

#Afficher les spectres et leur reconstruction par les composantes PCA
if nb <= 15:
    axs = np.arange(0, 15, 1).reshape(5, 3)
    axs = list(axs)
    for i in range(len(axs)):
        axs[i] = list(axs[i])

    fig1, axs = mpl.subplots(5, 3)
    resp = coefs@(pca.components_)
    print(resp.shape)

    cumul = 0
    for i in axs:
        for ii in range(3):
            if cumul <= nb-1 and res == '01' or cumul <= nb-1 and res == '10':
                id = f'Données brutes du spectre {listNameOfFiles(path)[cumul]}'
                i[ii].plot(donnees_tot_x, ordo[cumul], '#e377c2', label=id)
                i[ii].plot(donnees_tot_x, resp[cumul], '#17becf', linestyle='-', label='Données fittées')
                i[ii].legend()
                cumul += 1
            else:
                pass
    mpl.show()