import numpy as np
import matplotlib.pyplot as mpl
from scipy import special
import math
from shapely.geometry import LineString
from scipy.optimize import curve_fit
import pandas as pd
from tkinter.filedialog import askopenfile

#Module tkinter pour ne pas à avoir à écrire la destination du fichier
fileName = askopenfile(title="Choisir le fichier")
données=pd.read_csv(fileName, sep = ";")

print(données.head())
# x = valeurs sur les abscisses
x = np.array(list(données.x))
# y = valeurs sur les ordonnées
y = np.array(list(données.y))

#définir un nombre de points pour avoir une fonction qui a du sens

z = np.linspace(min(x),max(x),100)
# Définir la fonction ainsi que ses paramètres
def fonction(X, a, b, c, d):
    return a*np.sin((X*b)+c)+d

sinus = 3*np.sin((z*4)+5)+6

# Curvefit où p0 = [a, b, c, d] qui donne une approximation d'où chercher pour le curvefit
popt, pcov = curve_fit(fonction, x, y) #p0=[1, 4, 4, 6] 

print(*popt)

# Afficher les données et le curvefit
fig1, ax1 = mpl.subplots()          # Figure 1
ax1.plot(x, y, 'r')                 # Données

ax1.plot(z, fonction(z,*popt), 'b')        # Curvefit
ax1.set_xlabel("x") # Titre des abscisses
ax1.set_ylabel("y") # Titre des ordonnées
ax1.set_title("Curvefit d'un sinus")      # Titre du graphique

# Afficher les popt

mpl.text(-2.85, 2.9, f'Popt = {popt}')  

# Afficher la figure
mpl.show()