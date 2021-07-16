import pandas as pd
import os
import fnmatch
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as mpl

# Read the data
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


# Useful Information and instances
path = "/Users/justinemajor/Documents/raman/kelly_nonstop/spectra"
donnees_tot_x, ordo, donnees_tot_y = [], [], {}
nb = len(listNameOfFiles(path))
# print(nb)

# Create lists of the data
for nom in listNameOfFiles(path):
    # File name
    fich = open(path + '/' + nom, "r")
    test_str = list(fich)
    fich.close()
    x, y = [], []
    # Clean the information
    for j in test_str:
        elem_str = j.replace("\n", "")
        elem = elem_str.split(",")
        x.append(float(elem[0]))
        y.append(float(elem[1]))

    donnees_tot_x = np.array(x)
    ordo.append(np.array(y))
    donnees_tot_y[nom] = np.array(y)

fich2 = open("/Users/justinemajor/Documents/raman/kelly_nonstop/spectrum_background.csv", "r")
test_str2 = list(fich2)
fich2.close()
xBack, yGround = [], []
# Clean the information
for j in test_str2:
    elem_str = j.replace("\n", "")
    elem = elem_str.split(",")
    xBack.append(float(elem[0]))
    yGround.append(float(elem[1]))

# yGround = np.array(yGround)

# for ind, spec in enumerate(ordo):
    # ordo[ind] -= yGround

# print(ordo[2])

# Principal components analysis and creation of the coefficient matrix
pca = PCA(n_components=2)  # or n_components=5 or 0.99
principalCoefficients = pca.fit_transform(ordo)
principalComponents = np.array(pca.components_)
inverse = np.linalg.pinv(principalComponents)
moy = np.array(pca.mean_)
m = moy@inverse
coefs = principalCoefficients + m
print(pca.explained_variance_ratio_)
print(sum(pca.explained_variance_ratio_))


# Compute the concentration of every PC in every raw spectrum data
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


# Create the table of concentrations and show
if len(pca.components_) <= 5:
    principalDf = pd.DataFrame(data=gen, columns=['Solution'] + col[0:len(pca.components_)])
    pd.set_option('display.max_columns', None)
    principalDf.head()
    print(principalDf)

PC = pca.components_

PC1 = PC[0]
PC2 = PC[1]

fig2, (ax5, ax6, ax7, ax8) = mpl.subplots(4)

#Imprimer les spectres des composantes principales obtenues
ax6.plot(donnees_tot_x, PC1, "#e377c2", label='spectre RAMAN PC1')
ax6.set_xlabel('wavelength')      # titre des abscisses
ax6.set_ylabel('Intensity')      # titre des ordonnées
ax6.legend() # titre du graphique

ax7.plot(donnees_tot_x, PC2, 'r', label='spectre RAMAN PC2')
ax7.set_xlabel('wavelength')      # titre des abscisses
ax7.set_ylabel('Intensity')      # titre des ordonnées
ax7.legend()  # titre du graphique

ax5.plot(donnees_tot_x, ordo[2], 'r', label='spectre RAMAN x12 y11')
ax5.set_xlabel('wavelength')      # titre des abscisses
ax5.set_ylabel('Intensity')      # titre des ordonnées
ax5.legend()  # titre du graphique

ax8.plot(donnees_tot_x, ordo[895], 'r', label='spectre RAMAN lamelle')
ax8.set_xlabel('wavelength')      # titre des abscisses
ax8.set_ylabel('Intensity')      # titre des ordonnées
ax8.legend()  # titre du graphique

mpl.tight_layout()
mpl.show()
