'''
This file performs spectral clustering on a set of fibers. agglomCluster05 is imported, which
allows us to generate a similarity matrix and read in the fibers. 
Author: Yuen Hsi 
'''

import os
import numpy
import math
import heapq
import struct
import Pycluster
from agglomCluster05 import *
from scipy import linalg

#This method combines steps 1-5 and returns a clustering
def spectralCluster(similarityMatrix, k, sigma):
    matrix1 = step1(similarityMatrix, sigma)
    matrix2 = step2(matrix1)
    matrix3 = step3(matrix2, k)
    matrix4 = step4(matrix3)
    clusterID = step5(matrix4, k)
    print clusterID
    return clusterID

def step1(similarityMatrix, sigma):
    # Given our "distance matrix", get the square root of the number of elements 
    # which is the number of rows as similarityMatrix is a square matrix
    A = numpy.matrix(numpy.exp(-(numpy.asarray(similarityMatrix)**2)/(2*sigma**2)))
    for i in range(A.shape[0]):
        A[i,i] = 0
    return A

def step2(affinityMatrix):
    D = numpy.diag(1.0/numpy.sqrt(numpy.squeeze(numpy.asarray(numpy.sum(affinityMatrix,1)))))
    return D*affinityMatrix*D

def step3(matrixL, k):
    eigenValues, eigenVectors = numpy.linalg.eigh(matrixL) # array containing vectors
    sortedEigenvalues = numpy.argsort(-eigenValues)
    eigenValues = numpy.matrix(numpy.diag(eigenValues[sortedEigenvalues]))
    eigenVectors = eigenVectors[:,sortedEigenvalues]
    return eigenVectors[:,:k]

    #Given a numpy matrix or array, returns the same as an array with its
    #rows converted into unit vectors.
def step4(matrixX):
    Y = numpy.asarray(matrixX)
    lengths = numpy.reshape(numpy.sqrt(numpy.sum(Y**2,1)), (-1,1))
    return Y / numpy.tile(lengths, [1,Y.shape[1]])

def step5(matrixY, k):
    # Treat each row of Y as a point, cluster each of the points into k clusters
    #print matrixY
    clusterid, error, nfound = Pycluster.kcluster(matrixY, k)
    return clusterid

def findSigma(similarityMatrix, lBound, uBound, step):
    maxVar = 0
    while (lBound < uBound):
        if (numpy.var(step1(similarityMatrix, lBound)) > maxVar):
            maxVar = numpy.var(step1(similarityMatrix, lBound))
            sigma = lBound
        lBound = lBound + step
    return sigma

def main():
    memoryAddresses=getRandFibers(10)[0]
    fibers=readFibers(memoryAddresses)
    A=makeClusterMatrix(fibers,1)
    sigma = findSigma(A, 10, 40, 3)
    spectralCluster(A,3,sigma)

if __name__ == "__main__":

    main()