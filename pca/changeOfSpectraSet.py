from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as mpl


class PCBasis:  # TODO clarify and complete the class with every useful function (ex PCA)
    # Set of example spectra
    spec1 = np.array((0, 2, 3, 4, 5, 0, 2, 0, 4, 2, 3, 1, 2, 3, 1))
    spec2 = np.array((0, 2, 0, 0, 3, 1, 0, 4, 7, 3, 4, 1, 1, 3, 1))
    spec3 = np.array((1, 0, 3, 0, 1, 4, 3, 1, 3, 5, 2, 3, 1, 1, 1))
    spec4 = np.array((0, 0, 0, 0, 0, 1, 5, 1, 2, 0, 2, 2, 4, 1, 3))
    spec5 = np.array((0, 1, 0, 5, 0, 2, 3, 1, 1, 0, 0, 1, 4, 2, 1))
    spec6 = np.array((4, 1, 2, 1, 5, 3, 0, 3, 2, 4, 1, 5, 1, 1, 3))
    spec7 = np.array((4, 0, 0, 1, 5, 0, 1, 5, 3, 2, 0, 0, 1, 3, 4))

    expectedPC = np.vstack((spec1, spec2, spec3, spec4, spec5, spec6, spec7))

    def setCombinations(self, nb_spectra):  # TODO internal method, combinaitions only used within with nb as class arg?
        set = {}
        coefs = np.random.randint(0, 10, (nb_spectra, 7))
        combinations = coefs @ self.expectedPC
        spectra = np.vstack((self.expectedPC, combinations))
        spectra = list(spectra)
        for ind, el in enumerate(spectra):
            spectra[ind] = list(el)
        set['spectra'] = spectra
        set['coefs'] = coefs
        return set


# TODO add a little explination for the method at the beginning...
basis = PCBasis()
set = basis.setCombinations(71)
spectra = set['spectra']
coefs = set['coefs']
print(coefs)


# Decomposition with PCA
pca = PCA(n_components=7)
pcaCoefs = pca.fit_transform(spectra)
pcaComponents = pca.components_

inverse = np.linalg.pinv(pcaComponents)
moy = np.array(pca.mean_)
m = moy@inverse
coefficients = pcaCoefs + m
compo = coefficients@pcaComponents


# Change of coefficients matrix basis
BInv = np.linalg.pinv(basis.expectedPC)
concentration = (coefficients@pcaComponents) @ BInv
print(np.abs(np.round(concentration)))
newResult = concentration @ basis.expectedPC


# Set spectra display : raw sequence of spectra - reconstructed through PCA - reconstructed with known basis
setup = np.arange(0, 7*3, 1).reshape(7, 3)
fig1, setup = mpl.subplots(7, 3)

for ind, trio in enumerate(setup):
    trio[0].plot(spectra[5+ind], '-')
    trio[1].plot(compo[5+ind], '-')
    trio[2].plot(newResult[5+ind], '-')

mpl.show()
