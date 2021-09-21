import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
from scipy import stats, interpolate

# TODO ID analysis steps related to each method used here

# Regression
pixel = [625, 882, 1134, 1149]
nm = [671, 690, 708, 709]

slope, intercept, r_value, p_value, std_err = stats.linregress(pixel, nm)  # More or less efficient than curvefitting?
print(f"a={slope:.5f}", f"b={intercept:.3f}", f"σ={std_err:.3e}")

x_new = np.array(range(1339))  # generalize with len of files/data?
nm = x_new * slope + intercept

cm = 1 / (632.8e-7) - 1 / (nm * 1e-7)

data = glob.glob("*.TXT")

# Spectra
for file in data:
    soln = file.split("_")[2]
    df = pd.read_csv(file)
    y = df.iloc[:, 2]
    y /= max(abs(y))  # why abs? Necessary?
    plt.plot(nm, y, label=f"{soln}", linewidth=0.5)

plt.xlabel("$\lambda$ [nm]")
plt.ylabel("Intensité relative [-]")
plt.legend(loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.1))
# plt.savefig("Spectre_huiles.png")
plt.show()
plt.clf()


"""Second step of the project"""
# TODO not sure about this division, could use a better organisation and titles!


for ind, file in enumerate(data):
    soln = file.split("_")[2]
    print(soln)
    df = pd.read_csv(file)
    y = df.iloc[:, 2]
    # plt.plot(cm, y, label=f"{soln}", linewidth=0.5) # Spectre
    d = 25  # TODO get out of the for loop! (whole section with f2...)
    f2 = interpolate.interp1d(cm[200:][::d], y[200:][::d], kind='quadratic')  # Could rather fit polynomial expression
    y = y[200:1200] - f2(cm[200:1200])  # find more universally the range studied
    y /= max(y)
    mask_1444 = (cm[200:1200] > 1400) & (cm[200:1200] < 1500)  # Why? What is that...
    mask_1661 = (cm[200:1200] > 1600) & (cm[200:1200] < 1700)  # ID cm[...] by itself, with its own variable and why
    I_1444 = max(y[mask_1444])  # intensity, but why 1444 and 1661...
    I_1661 = max(y[mask_1661])
    # plt.plot(cm[200:1200], f2(cm[200:1200]), label=f"{soln}", linewidth=0.5) # Background
    plt.plot(cm[200:1200], y + 2 * ind, label=f"{soln}", linewidth=0.5)  # Not sure about the vertical step of 2
    print(f"r: {I_1444 / I_1661 * 100:.2f}%")


plt.xlabel("ν [1/cm]")
plt.ylabel("Intensité relative [-]")
plt.legend(loc="upper center", ncol=len(data), bbox_to_anchor=(0.5, 1.1))
# plt.savefig("Raman_huiles.png")
plt.show()
plt.clf()  # TODO check usefulness of this command... (x2)
