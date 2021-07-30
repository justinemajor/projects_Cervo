from scipy import integrate
import scipy as sp
import numpy as np
import threading
import matplotlib.pyplot as mpl
import math
import time
import re

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

height = 4
width = 4
countWidth = 0
countHeight = 0
countSpectrum = 0
triste = True

"""
while triste:
    print(f"{countSpectrum}: ({countWidth}, {countHeight})")
    if countWidth < width - 1:
        # wait for signal... (with a connect?)
        countWidth += 1
        # print(f"{countSpectrum}: ({countWidth}, {countHeight})")
    elif countHeight < height and countWidth == width - 1:
        if countSpectrum < width * height - 1:
            # wait for signal...
            countWidth = 0
            countHeight += 1
            # print(f"{countSpectrum}: ({countWidth}, {countHeight})")
        else:
            triste = False
            # enable_all_buttons()
    else:
        triste = False

    countSpectrum += 1
"""

"""
while triste:
    print(f"{countSpectrum}: ({countWidth}, {countHeight})")
    if countSpectrum < width * height - 1:
        if countHeight % 2 == 0:
            if countWidth < width - 1:
                countWidth += 1
            elif countWidth == width - 1:
                countHeight += 1
        elif countHeight % 2 == 1:
            if countWidth > 0:
                countWidth -= 1
            elif countWidth == 0:
                countHeight += 1
    else:
        triste = False
        # enabled...

    countSpectrum += 1
"""

"""
while triste:
    print(f"{countSpectrum}: ({countWidth}, {countHeight})")
    if countSpectrum < width*height:
        if countWidth < width - 1 and countHeight % 2 == 0:
            countWidth += 1
            # print(f"({countWidth}, {countHeight})")
        elif countWidth == width - 1 and countHeight % 2 == 0:
            countHeight += 1
            if countHeight == height:
                triste = False
            else:
                # print(f"({countWidth}, {countHeight})")
        elif 0 < countWidth < width and countHeight % 2 == 1:
            countWidth -= 1
            # print(f"({countWidth}, {countHeight})")
        elif countWidth == 0 and countHeight % 2 == 1:
            countHeight += 1
            if countHeight == height:
                triste = False
            else:
                # print(f"({countWidth}, {countHeight})")

        else:
            raise Exception("What the hell is going on?")

        countSpectrum += 1

    else:
        triste = False
"""


x = 3
y = 3
l = 8

"""
deb = np.zeros((x, y, l))
yo = np.zeros((x, y, 3))
top = np.zeros((x, y))

deb[0, 0, :] = np.array([1, 2, 3, 4, 5, 6, 7, 8])
deb[0, 1, :] = np.array([1, 1, 1, 1, 1, 1, 1, 1])
deb[1, :, :] = np.array([4, 5, 6, 7, 8, 2, 2, 2])
deb[2, 1, :] = np.array([3, 5, 7, 3, 7, 23, 5, 2])

yo[:, :, 0] = deb[:, :, 0:3].sum(axis=2)
yo[:, :, 1] = deb[:, :, 3:5].sum(axis=2)
yo[:, :, 2] = deb[:, :, 5:l].sum(axis=2)

top = yo.max(axis=2)
top = np.dstack((top, )*3)
yo /= top

print(yo)
for i, x in enumerate(yo):
    for ii, y in enumerate(x):
        print(f"({i}, {ii}) : [")
        for iii, z in enumerate(y):
            if iii != len(y)-1:
                print(f"{z}, ")
            else:
                print(f"{z}]")
"""

"""
a = np.array([1, 2, 3, 4, 5, 6, 7, 8])

a = (1 - 1/a) * 10**2
a = np.round(a, 0)

print(a)

print(int(3.7))
print(np.round(3.7))
print(round(3.7))
"""

"""
b = np.array((2, 4, 7, 8))
b = b.reshape((1, 1, len(b)))
b = np.vstack((b, )*3)
b = np.hstack((b, )*3)

a = np.array((1, 2, 3, 4))
a = a.reshape((1, 1, len(a)))
a = np.vstack((a, )*3)
a = np.hstack((a, )*3)

a = b-a

print(a)
print(np.shape(a))

mimi = [1, 2, 3]  # []
mimi = np.array(mimi)
if not list(mimi):
    print('joie')

if list(mimi):
    print('lol')


class TryToGetInstance:
    def __init__(self):
        self.yolo = "style"
        self.what = 0

    def define(self):
        return self.what

print(TryToGetInstance().yolo)
print(TryToGetInstance().define())
"""

nom = 'spectrum_x10_y3.csv'

tik = time.perf_counter()
matchObj = re.match("([A-Za-z_]*)_x(\\d+)_y(\\d+).*", nom)
if matchObj:
    val1 = str(matchObj.group(1))
    val2 = int(matchObj.group(2))
    val3 = int(matchObj.group(3))
    print(val1, val2, val3)
tok = time.perf_counter()
print(tok-tik)

nom = "spectrum_background.csv"

matchObj = re.match(".*?(_background).*", nom)
if matchObj:
    print(str(matchObj.group(1)))

"""
a = 21
a //= 6
print(a)
"""
