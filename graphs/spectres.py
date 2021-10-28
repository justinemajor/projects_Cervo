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

path = "/Users/justinemajor/Documents/ecole/gph/stage1/documents/spectres/base"
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


# imprimer les spectres
fig1, ax3 = mpl.subplots()
ax3.plot(x, y["lumiamb_usb2000.txt"], '#e377c2', label="lumière ambiante")
#ax3.plot(x, y["laser.txt"], '#17becf', label="laser")
ax3.set_xlabel('Wavenumber')
ax3.set_ylabel('Intensité (counts)')
ax3.legend()
ax3.set_title("Quelque chose")

mpl.tight_layout()
mpl.show()