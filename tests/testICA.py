from sklearn.decomposition import FastICA, PCA
import numpy as np
import matplotlib.pyplot as mpl

spec1 = np.array((0, 2, 3, 4, 5, 0, 2, 0, 4, 2, 3, 1, 2, 3, 1))
spec2 = np.array((0, 2, 0, 0, 3, 1, 0, 4, 7, 3, 4, 1, 1, 3, 1))
spec3 = np.array((1, 0, 3, 0, 1, 4, 3, 1, 3, 5, 2, 3, 1, 1, 1))
spec4 = np.array((0, 0, 0, 0, 0, 1, 5, 1, 2, 0, 2, 2, 4, 1, 3))
spec5 = np.array((0, 1, 0, 5, 0, 2, 3, 1, 1, 0, 0, 1, 4, 2, 1))
spec6 = np.array((4, 1, 2, 1, 5, 3, 0, 3, 2, 4, 1, 5, 1, 1, 3))
spec7 = np.array((4, 0, 0, 1, 5, 0, 1, 5, 3, 2, 0, 0, 1, 3, 4))
# spec5 = spec3
# spec6 = spec1
# spec7 = spec2

coefs = np.random.randint(0, 10)


def setCombinations(nb_spectra):
    spectra = [spec1, spec2, spec3, spec4, spec5, spec6, spec7]
    for i in range(nb_spectra):
        newSpec = np.zeros(15)
        newSpec += coefs * spec1
        newSpec += coefs * spec2
        newSpec += coefs * spec3
        newSpec += coefs * spec4
        newSpec += coefs * spec5
        newSpec += coefs * spec6
        newSpec += coefs * spec7
        spectra.append(newSpec)
    for ind, el in enumerate(spectra):
        spectra[ind] = list(el)
    return spectra


spectra = setCombinations(71)
# print(spectra)

# Decomposition with PCA
pca = PCA(n_components=7)
pcaCoefs = pca.fit_transform(spectra)
pcaComponents = pca.components_

inverse = np.linalg.pinv(pcaComponents)
moy = np.array(pca.mean_)
m = moy@inverse
coefficients = pcaCoefs + m
compo = coefficients@pcaComponents

# Decomposition with ICA
ica = FastICA(n_components=7)
icaCoefs = ica.fit_transform(spectra)
icaComponents = ica.components_

# Set spectra display, raw-pca-ica
setup = np.arange(0, 7*3, 1).reshape(7, 3)
fig1, setup = mpl.subplots(7, 3)

for ind, trio in enumerate(setup):
    trio[0].plot(spectra[ind], 'o-')
    trio[1].plot(compo[ind], 'o-')
    trio[2].plot(icaComponents[ind], 'o-')

mpl.show()
