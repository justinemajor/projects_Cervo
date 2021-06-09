import numpy as np
import matplotlib.pyplot as mpl
from scipy import special
import math
import pandas as pd
from scipy.optimize import curve_fit
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
import scipy as sp
from scipy.signal import peak_widths

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

#Définition des variables pertinentes
path = "/Users/justinemajor/Documents/gph.doc/stage1/documents/spectres/" + res
donnees_tot_x, ordo, donnees_tot_y = [], [], {}
nb = len(listNameOfFiles(path))

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

#Calculer le bruit des spectres
def droite(x, a, b, c):
    return a*x**2 + b*x + c

bruits = []
for i in range(nb):
    popt, pcov = curve_fit(droite, donnees_tot_x[500:800], ordo[i][500:800], p0=[1, 1, 1])
    fct = np.array(droite(donnees_tot_x[500:800], *popt))
    bruit = np.std(ordo[i][500:800]-fct)
    bruits.append(bruit)

#Trouver les pics des spectres et leur ordonnée respective
peaks = []
pkys = []
for i in range(nb):
    peak = sp.signal.find_peaks(ordo[i], height=3*bruits[i]**2)
    peaks.append(peak[0])
    pky = []
    for ii in peak[0]:
        pky.append(ordo[i][ii])
    pkys.append(pky)

#Calculer le rapport SNR à chaque pic trouvé
snr = {}
for i in range(nb):
    snr[listNameOfFiles(path)[i]] = np.array(pkys[i]) / bruits[i]

snrm = {}
for key, val in snr.items():
    snrm[key] = np.mean(val)
print(snrm)

# Afficher les données et les pics
axs = np.arange(0, 15, 1).reshape(5, 3)
axs = list(axs)
for i in range(len(axs)):
    axs[i] = list(axs[i])

fig1, axs = mpl.subplots(5, 3)

cumul = 0
for i in axs:
    for ii in range(3):
        if cumul <= 12 and res == '01' or cumul <= 13 and res == '10':
            yo = peaks[cumul]
            lala = []
            lolo = []
            for x in yo:
                lala.append(ordo[cumul][x])
                lolo.append(donnees_tot_x[x])
            i[ii].plot(lolo, lala, 'o')
            i[ii].plot(donnees_tot_x, ordo[cumul])
            #i[ii].legend()
            cumul += 1
        else:
            pass

mpl.show()