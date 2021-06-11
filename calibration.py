import numpy as np
import matplotlib.pyplot as mpl
from scipy import signal
import math
import statistics
from scipy.optimize import curve_fit
import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch

#lire les données
def listNameOfFiles(directory: str, extension="csv") -> list:
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

path = "/Users/justinemajor/Documents/ecole/gph/stage1/documents/calib"
absi, ordo, donnees_tot_y = [], [], {}
nb = len(listNameOfFiles(path))

#création des listes de données
for nom in listNameOfFiles(path):
    # Nom du fichier à importer
    fich = open(path + '/' + nom, "r")
    test_str = list(fich)
    fich.close()
    x, y = [], []
    # Nettoyer les informations
    for j in test_str:
        elem_str = j.replace("\n", "")
        elem = elem_str.split(",")
        x.append(float(elem[0]))
        y.append(float(elem[1]))

    absi.append(x)
    ordo.append(y)
    donnees_tot_y[nom] = y

fig1, [ax1, ax2, ax3] = mpl.subplots(1, 3)
for i in range(nb):
    ax1.plot(absi[i], ordo[i], label=f'{i}-{listNameOfFiles(path)[i]}')
ax1.legend()

absi[0], ordo[0] = absi[0][0:300], ordo[0][0:300]
absi[1], ordo[1] = absi[1][0:600], ordo[1][0:600]
absi[2], ordo[2] = absi[2][200:700], ordo[2][200:700]
absi[3], ordo[3] = absi[3][400:800], ordo[3][400:800]

def fonction(X, a, b, c):
    return a * np.exp(-(X-b)**2 / (2*c**2))

pics = []
for i in range(nb):
    popt, pcov = curve_fit(fonction, absi[i], ordo[i], p0=[10000, 10000, 10000])
    fit = fonction(absi[i], *popt)
    ax2.plot(absi[i], ordo[i], label=f'{i}-{listNameOfFiles(path)[i]}')
    ax2.plot(absi[i], fit, label=f'fit {listNameOfFiles(path)[i]}')
    pics.append(popt[1])

print(pics)

def yo(X, a, b, c):
    return a*X**2 + b*(X) - c

xo = np.array([800, 850, 900, 940], dtype=np.float64)
popt, pcov = curve_fit(yo, xo, pics, p0=[1, 1, 1])
print(popt)
ax3.plot(xo, yo(xo, *popt))
ax3.plot(xo, pics)
ax2.legend()

mpl.show()