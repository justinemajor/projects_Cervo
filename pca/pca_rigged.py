import csv
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np

A = np.array([1, 1, 1, 3, 1])
B = np.array([1, 1, 1, 1, 5])
C = np.array([1, 1, 3, 1, 1])
D = np.array([2, 1, 1, 1, 1])

X = np.array([A, B, C, D, 3*A+B, D+B, 5*C+A, C+D+B, 3*A+D+2*B])

def PCA(X , num_components):
     
    #Step-1
    X_meaned = X - np.mean(X , axis = 0)
     
    #Step-2
    cov_mat = np.cov(X, rowvar=False)
    print(cov_mat)
     
    #Step-3
    eigen_values , eigen_vectors = np.linalg.eigh(cov_mat)
     
    #Step-4
    sorted_index = np.argsort(eigen_values)[::-1]
    sorted_eigenvalue = eigen_values[sorted_index]
    sorted_eigenvectors = eigen_vectors[:,sorted_index]
     
    #Step-5
    eigenvector_subset = sorted_eigenvectors[:,0:num_components]
    
    #Step-6
    X_reduced = np.dot(eigenvector_subset.transpose() , X.transpose() ).transpose()
    X_reduced
     
    return X_reduced

PCA(X, 4)