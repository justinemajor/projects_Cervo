from scipy import integrate
import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl
import math
import time

"""
a = [[1, 2, 3]]
b = [[4, 5, 6]]

c = np.vstack((a, b))
print(c)
d = np.linalg.pinv(c)
print(d)
e = c@d
print(e)

def isYouPretty():
    return True

def :
    print("yay")

print("joie")

dico = {'yo':[1, 2, 3]}
print(dico.keys())
"""

height = 3
width = 3
countWidth = 0
countHeight = 0
countSpectrums = 0
triste = True
while triste:
    #print(f"({countWidth}, {countHeight})")
    if countSpectrums < width*height:
        if countWidth < width - 1 and countHeight % 2 == 0:
            countWidth += 1
            print(f"({countWidth}, {countHeight})")
        elif countWidth == width - 1 and countHeight % 2 == 0:
            countHeight += 1
            if countHeight == height:
                triste = False
            else:
                print(f"({countWidth}, {countHeight})")
        elif 0 < countWidth < width and countHeight % 2 == 1:
            countWidth -= 1
            print(f"({countWidth}, {countHeight})")
        elif countWidth == 0 and countHeight % 2 == 1:
            countHeight += 1
            if countHeight == height:
                triste = False
            else:
                print(f"({countWidth}, {countHeight})")

        else:
            raise Exception("What the hell is going on?")

        countSpectrums += 1

    else:
        triste = False
