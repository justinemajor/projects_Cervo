import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, SparsePCA
import numpy as np
import matplotlib.pyplot as plt

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

fig2, ax2 = plt.subplots()
ax2.plot(donnees_tot_x, ordo[0], '#e377c2')
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN 1') # titre du graphique

fig3, ax3 = plt.subplots()
ax3.plot(donnees_tot_x, ordo[3], '#17becf')
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN 3') # titre du graphique

fig4, ax4 = plt.subplots()
ax4.plot(donnees_tot_x, ordo[7], 'b-')
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN 4') # titre du graphique

fig1, ax1 = plt.subplots()
ax1.plot(donnees_tot_x, ordo[1], 'r-')
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN 2') # titre du graphique

"""
fig5, ax5 = plt.subplots()
ax5.plot(donnees_tot_x, ordo[13], '#e377c2')
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN tous') # titre du graphique
"""

pca = PCA(n_components=5)
principalComponents = pca.fit_transform(ordo)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2', 'principal component 3', 'principal component 4', 'principal component 5'])
print(principalDf)
#print(StandardScaler().fit_transform(principalDf))
#print(listNameOfFiles(path).index("0100_10.txt"))
#print(listNameOfFiles(path)[4:6])
#print(pca.components_.transpose())
print(pca.explained_variance_ratio_)
print(sum(pca.explained_variance_ratio_))

PC1 = pca.components_[0]
PC2 = pca.components_[1]
PC3 = pca.components_[2]
PC4 = pca.components_[3]
PC5 = pca.components_[4]

PC = [PC1, PC2, PC3, PC4, PC5]
index = [0, 1 , 3, 7]

C1, C2, C3, C4= np.zeros(1039), np.zeros(1039), np.zeros(1039), np.zeros(1039)
liste = [C1, C2, C3, C4]

for i in range(4):
    for ii in range(5):
        liste[i] += principalComponents[index[i]][ii]*PC[ii]

fig6, ax6 = plt.subplots()
ax6.plot(donnees_tot_x, PC1*principalComponents[3][0], '#17becf')
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN PC1') # titre du graphique

fig7, ax7 = plt.subplots()
ax7.plot(donnees_tot_x, PC2*principalComponents[0][1], "#e377c2")
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN PC2') # titre du graphique

fig8, ax8 = plt.subplots()
ax8.plot(donnees_tot_x, PC3*principalComponents[7][2]+PC4*principalComponents[7][3], "b-")
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN PC3') # titre du graphique

"""
fig9, ax9 = plt.subplots()
ax9.plot(donnees_tot_x, PC4, 'r-')
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN PC4') # titre du graphique
"""

fig10, ax10 = plt.subplots()
ax10.plot(donnees_tot_x, PC5*principalComponents[1][4], 'r-')
plt.xlabel('Wavenumber')      # titre des abscisses
plt.ylabel('Intensité')      # titre des ordonnées
plt.title('Spectres RAMAN PC4') # titre du graphique

plt.show()

"""
print(PCA(ordo, 4))
print(listNameOfFiles(path).index("0001_10.txt"))
print(listNameOfFiles(path).index("0010_10.txt"))
print(listNameOfFiles(path).index("0100_10.txt"))
print(listNameOfFiles(path).index("1000_10.txt"))
print(PCA(ordo, 4)[7])
"""
