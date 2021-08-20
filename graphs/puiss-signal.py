import numpy as np
import matplotlib.pyplot as mpl
import scipy as sp
from scipy.optimize import curve_fit
from scipy.signal import peak_widths
from sympy import *
from shapely.geometry import LineString

P = np.array([10, 20, 30, 40, 50, 60, 69])
c = np.array([115, 240, 350, 470, 600, 720, 810])

def y(x, a):
    return a*x

popt, pcov = curve_fit(y, P, c, p0=[1])
print(popt)

fig1, ax1 = mpl.subplots()
ax1.plot(P, c, label="courbe expérimentale")
ax1.plot(P, y(P, popt), 'r-', label="courbe théorique")
ax1.set_xlabel('Puissance [mW]')      # titre des abscisses
mpl.ylabel('Intensité [counts]')      # titre des ordonnées
mpl.text(40, 200, f'pente = {round(popt[0], 3)} counts/mW')
mpl.legend()
mpl.title("Intensité des signaux RAMAN selon la puissance d'émission du laser") # titre du graphique

mpl.show()
