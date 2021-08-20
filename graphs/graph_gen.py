import numpy as np
from numpy import *
import matplotlib.pyplot as mpl
import scipy as sp
from scipy.optimize import curve_fit
from scipy.signal import peak_widths
from sympy import *
from shapely.geometry import LineString
#from scipy.misc import derivative
#import math
#from lmfit import Model


di = np.array([0.882, 0.864, 0.849, 0.842, 0.831, 0.823, 0.816, 0.808, 0.801, 0.795, 0.787, 0.782, 0.778, 0.772, 0.769, 0.765, 0.762, 0.758, 0.755, 0.750, 0.745, 0.741, 0.736, 0.732, 0.728, 0.721, 0.718, 0.710, 0.703, 0.696, 0.687, 0.675, 0.660, 0.648, 0.641, 0.636, 0.632, 0.629, 0.625, 0.620, 0.615, 0.612, 0.554])
P = np.array([0.399, 0.389, 0.38, 0.375, 0.365, 0.358, 0.35, 0.342, 0.33, 0.317, 0.3, 0.283, 0.272, 0.250, 0.24, 0.224, 0.213, 0.202, 0.184, 0.167, 0.149, 0.132, 0.121, 0.107, 0.096, 0.082, 0.071, 0.061, 0.051, 0.041, 0.031, 0.020, 0.010, 0.00525, 0.003, 0.00164, 0.001, 0.000644, 0.000408, 0.000245, 0.000160, 0.000131, 0.0000262])


def fct(x,a,b,c,d):
    return a * sp.special.erf(x * b + c) + d

popt, pcov = curve_fit(fct, di, P, p0=[0, 20, -20, 0])
#print(popt)

def dev(x, a, b, c, d):
    return (2*a*b) / (np.exp((c + b*x)**2) * math.sqrt(np.pi))

"""
deb, fin, qte = di[-1], di[0], 1000
peak = sp.signal.find_peaks(dev(np.linspace(deb,fin,qte), *popt))[0]
l = sp.signal.peak_widths(dev(np.linspace(deb,fin,qte), *popt), peak, rel_height=0.5)[0]
larg = l * (fin-deb)/qte
#print(l)
#print(larg)
"""

xx = np.linspace(min(di),max(di),1000000)

mid = dev(-popt[2]/popt[1],*popt)/2
#print(mid)
#print(2*popt[0]*popt[1]/math.sqrt(np.pi)/2)
ymid = [mid]*len(xx)
courbe1 = LineString(np.column_stack((xx,dev(xx,*popt))))
courbe2 = LineString(np.column_stack((xx,ymid)))

isct = courbe1.intersection(courbe2)
dist = (np.array(isct[1])[0]-np.array(isct[0])[0])*25.4

xmin = np.array(isct[0])[0]
xmax = np.array(isct[1])[0]


fig1, ax1 = mpl.subplots()
ax1.plot(di, P)
ax1.plot(di, fct(di, *popt), 'r-')
ax1.set_xlabel('distance [m"]')      # titre des abscisses
mpl.ylabel('Puissance [W]')      # titre des ordonnées
mpl.title('erf(x)') # titre du graphique

fig2, ax2 = mpl.subplots()
ax2.plot(di, dev(di, *popt), 'g-')
ax2.plot(np.linspace(xmin, xmax, len(xx)), ymid, 'b--')
ax2.plot([xmin, xmax], ymid[0:2], 'bo')
mpl.xlabel('distance [m"]')      # titre des abscisses
mpl.ylabel('Puissance relative [W/m"]')      # titre des ordonnées
mpl.title('gaussienne') # titre du graphique
mpl.text(0.55, 3, f'largeur = {round(dist, 4)} mm')
mpl.show()