from scipy import integrate
import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl
import math
import time


a = [[1, 2, 3]]
b = [[4, 5, 6]]

c = np.vstack((a, b))
print(c)
d = np.linalg.pinv(c)
print(d)
e = c@d
print(e)
"""
def isYouPretty():
    return True

def move_stage():
    print("yay")

print("joie")

dico = {'yo':[1, 2, 3]}
print(dico.keys())
"""