import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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

    donnees_tot_x = x
    ordo.append(y)
    donnees_tot_y[nom] = y

ordo = StandardScaler().fit_transform(ordo)
pca = PCA(n_components=4)
principalComponents = pca.fit_transform(ordo)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2', 'principal component 3', 'principal component 4'])
print(principalDf)
print(listNameOfFiles(path).index("0100_10.txt"))
print(listNameOfFiles(path)[4:6])