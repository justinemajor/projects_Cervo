import numpy as np
import matplotlib.pyplot as mpl
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch

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

path = "/Users/justinemajor/Documents/gph/stage1/documents/iso_vs"
x, y, el = [], {}, []
nb = len(listNameOfFiles(path))

for nom in listNameOfFiles(path):
    # Nom du fichier à importer
    fich = open(path + '/' + nom, "r")
    test_str = list(fich)[14:]
    fich.close()
    xx, yy = [], []
    # Nettoyer les informations
    for j in test_str:
        elem_str = j.replace(",", ".").replace("\n", "").replace("\t", ",")
        elem = elem_str.split(",")
        xx.append(float(elem[0]))
        yy.append(float(elem[1]))

    x = xx
    y[nom] = yy
    el.append(yy)

#points importants
max_ips = max(y["iso_ips_lum.txt"])
max_maison = max(y["iso_maison_lum.txt"])
x_ips = x[y["iso_ips_lum.txt"].index(max_ips)]
x_maison = x[y["iso_maison_lum.txt"].index(max_maison)]

#imprimer les spectres
fig1, (ax2, ax3) = mpl.subplots(2)
"""
ax1.plot(x, y["iso_probe.txt"])
ax1.set_xlabel('Wavenumber (cm-1)')
ax1.set_ylabel('Intensité (counts)')
ax1.set_title("Test avec la probe IPS à 21,4mW à la source (15 secondes d'intégration)")
"""

ax2.plot(x, y["iso_ips_lum.txt"], '#17becf', label="IPS avec lumière, 40mW")
ax2.plot(x, y["iso_maison_lum.txt"], '#e377c2', label="maison avec lumière, 47mW")
ax2.set_xlabel('Wavenumber')
ax2.set_ylabel('Intensité (counts)')
ax2.legend()
ax2.annotate(f'pic max IPS = {max_ips} counts', xy=(x_ips, max_ips), xytext=(1000, 40000),
        arrowprops=dict(facecolor='#17becf', shrink=0.05, width=1, headwidth=4))
ax2.annotate(f'pic max maison = {max_maison} counts', xy=(x_maison, max_maison), xytext=(1000, 25000),
        arrowprops=dict(facecolor='#e377c2', shrink=0.05, width=1, headwidth=4))
ax2.annotate(f'{x_maison} cm-1', xy=(x_maison-40, 40000), xytext=(-50, 40000),
        arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=4, headlength=2))
ax2.set_title("Isopropanol avec lumière (10 secondes d'intégration)")

ax3.plot(x, y["iso_maison_ln.txt"], '#e377c2', label="maison sans lumière, 47mW")
ax3.plot(x, y["iso_ips_ln.txt"], '#17becf', label="IPS sans lumière, 40mW")
ax3.set_xlabel('Wavenumber')
ax3.set_ylabel('Intensité (counts)')
ax3.legend()
ax3.set_title("Isopropanol sans lumière (10 secondes d'intégration)")

mpl.tight_layout()
mpl.show()