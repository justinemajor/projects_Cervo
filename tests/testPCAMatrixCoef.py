from sklearn.decomposition import PCA
import numpy as np
import unittest
from pca.changeOfSpectraSet import PCBasis


class TestChangeOfBasis(unittest.TestCase):
    base = PCBasis()


"""
Things to check:
- size of every matrix used, obtained
- resemblance between what is expected and obtained (reconstructed spectra and concentrations)
- type of values in arrays
- works when first transformed? for example with HPF
- has to work with integer concentrations and also floating numbers
- with huge sets of data as well as small
- method of inv?
"""