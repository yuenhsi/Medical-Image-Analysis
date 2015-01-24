#This file is an attempt to optimize agglomerative clustering by using numpy matrices
#and their built in functions to manipulate the similarity matrix. However, we did not have time
#to incorporate this code into our agglomerative clustering file.
#Author - Simphiwe Hlophe

import numpy as np
import math

def compareRows(array1,array2):
    '''takes 2 rows of a matrix forms a matrix formed by the mininum entries
takes 2 rows and returns a row or 1*n array'''
    z = np.minimum(array1,array2)
    return z

            
def compareColums(colum1,colum2):
    """ This method takes 2 colums compares them and returns a colum of the smallest values"""

    newColum = np.zeros(7)
    colum1a = colum1.reshape(1,7)
    colum2a = colum2.reshape(1,7)
    z = np.minimum(colum1,colum2)
    print (z)
    return z
def manupulateMatrix(Matrix,size):
    """
       split the rows into 3 parts
       split colums into 3 partsg
       take minimum of each part and then reconccatinate the matrix"""
    first = Matrix[:,:1]
    seconf = Matrix[:,1:2]
    bigpart1 = Matrix[:,2:]
    mininum = np.minimum(first,secondf)
    p = np.concatenate(minimum,bigpart1,1)


def shrink(M,levels):
    """ locate non zero smallest elemnt of aray, finf its cordinates divide the
    matrix up into 3 parts I hope to reduce the search space so i do not have to search places where
    i do not need to search."""
    while levels>2:
    
        listofclust = []
        smallest = np.min(M[np.nonzero(M)])
        xs,ys = np.where(M==smallest)
        
        # x and y cordinates.
        xcord = xs[0]
        ycord = ys[0]
        # split matrix into 3 and gather smallest row.
        ''' this part retuns a matrix with the two rows replaced by the minimum of the two rows
         this matrix is still n*n'''
        #also we split colums into 3
        firstrow = M[:,xcord:xcord+1]
        secondrow = M[:,xcord+1:xcord+2]
        firstcolum = M[:ycord,:]
        secondcolum= M[ycord:ycord+1,:]
        restofRows = M[:,xcord+2:M.shape[0]]
        restofcolums = M[xcord+2:,:]
        # find the minimum of each row and colum
        minrow = np.minimum(firstrow,secondrow)
        mincolum = np.minimum(firstcolum,secondcolum)
        
        newminrow = np.delete(minrow,ycord,0) #This is the new shortened row
        rem = np.delete(M,ycord,0)
        rem2 = np.delete(rem,ycord,1)# rem2 is our final matrix.
        
        print(rem2)
        smallMatrix = rem2
        print(smallMatrix)
        clusterdlist = [xcord,ycord]
        print(clusterdlist)
        print ("clustered",xcord,ycord)
        listofclust.append(clusterdlist)
        
        #return smallMatrix,listofclust
        return shrink(smallMatrix,levels-1)
    
def main():
    

    shrink(x,4)
    
main()
