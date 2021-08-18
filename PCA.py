import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FastICA
import numpy as np
import matplotlib.pyplot as plt


# lire les données
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

path = "/Users/justinemajor/Documents/ecole/gph/stage1/documents/spectres/10"
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

#imprimer les spectres
fig2, [[ax2, ax7], [ax3, ax8], [ax4, ax9], [ax1, ax6]] = plt.subplots(4, 2)
ax2.plot(donnees_tot_x, ordo[0], '#e377c2', label='spectre RAMAN 1')
ax2.set_xlabel('Wavenumber')      # titre des abscisses
ax2.set_ylabel('Intensité')      # titre des ordonnées
ax2.legend()  # titre du graphique

ax3.plot(donnees_tot_x, ordo[3], '#17becf', label='spectre RAMAN 3')
ax3.set_xlabel('Wavenumber')      # titre des abscisses
ax3.set_ylabel('Intensité')      # titre des ordonnées
ax3.legend()  # titre du graphique

ax4.plot(donnees_tot_x, ordo[6], 'b-', label='spectre RAMAN 4')
ax4.set_xlabel('Wavenumber')      # titre des abscisses
ax4.set_ylabel('Intensité')      # titre des ordonnées
ax4.legend()  # titre du graphique

ax1.plot(donnees_tot_x, ordo[1], 'r-', label='spectre RAMAN 2')
ax1.set_xlabel('Wavenumber')      # titre des abscisses
ax1.set_ylabel('Intensité')      # titre des ordonnées
ax1.legend()  # titre du graphique

# méthode d'analyse par les composantes principales
# pca = PCA(n_components=5)
# principalCoefficients = pca.fit_transform(ordo)
# principalDf = pd.DataFrame(data = principalCoefficients, columns = ['principal component 1', 'principal component 2', 'principal component 3', 'principal component 4', 'principal component 5'])

# Analysis method by ICA
ica = FastICA(n_components=4)
fitted = ica.fit_transform(ordo)
principalDf = pd.DataFrame(data = fitted, columns = ['principal component 1', 'principal component 2', 'principal component 3', 'principal component 4'])

# Tableau des coefficients
pd.set_option('display.max_columns', None)
principalDf.head()
print(principalDf)

# Importance de chaque composante principale trouvée
# print(pca.explained_variance_ratio_)

# Total de la variance expliquée par l'utilisation d'un nombre limité de composantes
# print(sum(pca.explained_variance_ratio_))

#vecteurs de base formés des vecteurs singuliers (composantes principales)
#PC = principalCoefficients@pca.components_ + pca.mean_
# PC = pca.components_
PC = ica.components_

PC1 = PC[0]
PC2 = PC[1]
PC3a = PC[2]
PC3 = PC[3]
# PC4a = PC[4]
# PC4 = PC[6]

"""
PC = [PC1, PC2, PC3, PC4, PC5]
index = [0, 1 , 3, 7]

C1, C2, C3, C4= np.zeros(1039), np.zeros(1039), np.zeros(1039), np.zeros(1039)
liste = [C1, C2, C3, C4]

for i in range(4):
    for ii in range(5):
        liste[i] += principalCoefficients[index[i]][ii]*PC[ii]
"""

# Imprimer les spectres des composantes principales obtenues
ax6.plot(donnees_tot_x, PC1, "#e377c2", label='spectre RAMAN PC1')
ax6.set_xlabel('Wavenumber')      # titre des abscisses
ax6.set_ylabel('Intensité')      # titre des ordonnées
ax6.legend() # titre du graphique

# fig7, ax7 = plt.subplots()
ax7.plot(donnees_tot_x, PC2, 'r', label='spectre RAMAN PC2')
ax7.set_xlabel('Wavenumber')      # titre des abscisses
ax7.set_ylabel('Intensité')      # titre des ordonnées
ax7.legend() # titre du graphique

# fig8, ax8 = plt.subplots()
ax8.plot(donnees_tot_x, PC3, '#17becf', label='spectre RAMAN PC4')
ax8.set_xlabel('Wavenumber')      # titre des abscisses
ax8.set_ylabel('Intensité')      # titre des ordonnées
ax8.legend() # titre du graphique

# fig10, ax10 = plt.subplots()
# ax10.plot(donnees_tot_x, PC4a, 'b', label='spectre RAMAN PC5')
# ax10.set_xlabel('Wavenumber')      # titre des abscisses
# ax10.set_ylabel('Intensité')      # titre des ordonnées
# ax10.legend() # titre du graphique

# fig9, ax9 = plt.subplots()
ax9.plot(donnees_tot_x, PC3a, 'b', label='spectre RAMAN PC3')
ax9.set_xlabel('Wavenumber')      # titre des abscisses
ax9.set_ylabel('Intensité')      # titre des ordonnées
ax9.legend() # titre du graphique

plt.tight_layout()
plt.show()



