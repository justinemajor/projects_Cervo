# encoding utf-8
from raytracing import *
import sys
print(sys.version)

d1, d2 = 200, 200

path = ImagingPath()
path.label="Simple example"
path.append(Space(d=d1))
path.append(Lens(f=50, diameter=25, label="First lens"))
path.append(Space(d=d2))

print(path.forwardConjugate())
print(path.forwardConjugate()[1].magnification())

dist = d1 + d2 + path.forwardConjugate()[0]
magn = path.forwardConjugate()[1].magnification()[0]

path.display(comments=f"distance = {dist}\ngrossissement = {magn}")