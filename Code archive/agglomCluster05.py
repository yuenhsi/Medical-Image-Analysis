'''
This file performs agglomerative clustering of a set (or random subset) of fibers.
First, the fibers are put into an array (methods are contained in subsetFinder).
Then a matrix is created that stores the pairwise distance between fibers. This method uses either
the closest point distance, the mean minimum distance or the Hausdorff distance
Next the fibers are clustered using single linkage agglomerative clustering
The tree output of agglomerative clustering can be converted into a clustering with k clusters
using the findKthLevel method.
@author Yuen Hsi
'''

import math, random, struct, numpy
import os
from subsetFinder import *

#Calculates distance between two points. Takes x,y,z coordinates of each point as arguments
def d(x1,y1,z1,x2,y2,z2):
    intermediate = math.pow((x1-x2),2) + math.pow((y1-y2),2) + math.pow((z1-z2),2)
    return math.sqrt(intermediate)
#Calculates the mean minimum distance between 2 fibers. f1 and f2 are arrays
def meanD1(f1,f2):
    #sum1 and counter are used to calculate the average
    sum1=0
    counter=0
    #for each point in f1
    for x in range(len(f1)):
        #set the minimum distance high
        minD=999
        #Loop through each point in f2
        for y in range(len(f2)):
            #if the distance between x in f1 and y in f2 is less than minD
            if(d(f1[x][0],f1[x][1],f1[x][2],f2[y][0],f2[y][1],f2[y][2]) < minD):
                #change the value of minD to that distance
                minD=d(f1[x][0],f1[x][1],f1[x][2],f2[y][0],f2[y][1],f2[y][2])
        #Add the minD for each point x to sum1
        sum1+=minD
        counter+=1
        #print minD, "x, y = ", x, y
        #counter+=1
    #after finding the minD for each point in f1, the average is calculated and returned
    if(counter!=0):
        #print counter
        #print sum1
        return sum1/counter
    else:    
        return 1000

#Mean D between 2 fibers is not necessarily symmetric. This method averages the meanD of 2 fibers.
#This is the metric used in the Corouge paper.
def meanD(f1,f2):
    return (meanD1(f1,f2)+meanD1(f2,f1))/2
    
#Crappy Distance metric that returns the minimum distance between the two fibers
def minD(f1,f2):
    currentMin=1000
    #for each point in f1
    for x in range(len(f1)):
        #Loop through each point in f2
        for y in range(len(f2)):
            #if the distance between x in f1 and y in f2 is less than minD
            if(d(f1[x][0],f1[x][1],f1[x][2],f2[y][0],f2[y][1],f2[y][2]) < currentMin):
                #change the value of currentMin to that distance
                currentMin=d(f1[x][0],f1[x][1],f1[x][2],f2[y][0],f2[y][1],f2[y][2])
    return currentMin

#the Hausdorf distance is the maximum distance between a point in f1 and the closest point in f2
def hausD1(f1,f2):
    #set the maximum distance low
    maxD=0
    #for each point in f1
    for x in range(len(f1)):
        currentD=1000
        #Loop through each point in f2
        for y in range(len(f2)):
            #if the distance between x in f1 and y in f2 is greater than maxD
            if(d(f1[x][0],f1[x][1],f1[x][2],f2[y][0],f2[y][1],f2[y][2]) < currentD):
                #change the value of maxD to that distance
                currentD=d(f1[x][0],f1[x][1],f1[x][2],f2[y][0],f2[y][1],f2[y][2])
        if(currentD>maxD):
            maxD=currentD
    return maxD

#returns a symmetric Hausdorff distance
def hausD(f1,f2):
    if(hausD1(f1,f2)>hausD1(f2,f1)):
        return hausD1(f1,f2)
    else:
        hausD1(f2,f1)
    

#This method takes an array of fibers as input. It returns a matrix with entries
#corresponding to the mean distance between pairs of fibers
def makeClusterMatrix(fibers, mode):
    #empty square matrix with numRows equal to the number of fibers
    clusterMatrix=numpy.zeros(shape=(len(fibers),len(fibers)))
    #for each pair of fibers, fill the corresponding entry in the matrix with something
    for i in range(len(fibers)):
        for j in range(len(fibers)):
            #if the fibers are the same, the distance between them is 0
            if(i==j):
                clusterMatrix[i][j]=0
            #if the fibers are different, fill the entry with the mean minimum distance
            else:
                if(mode==1):
                    clusterMatrix[i][j]=meanD(fibers[i],fibers[j])
                elif(mode==2):
                    clusterMatrix[i][j]=hausD(fibers[i],fibers[j])
                else:
                    clusterMatrix[i][j]=minD(fibers[i],fibers[j])
    #print the similarity matrix
    #print clusterMatrix
    return clusterMatrix
    
class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
        self.parent = None
 
 
#This method performs single linkage agglomerative clustering on the similarity matrix
def agglomCluster(clusterMatrix):
    #nodes contains all the leaves in our tree. The data for each node is the index of the fibers it contains
    nodes=[Tree() for i in range(len(clusterMatrix))]
    for i in range(len(clusterMatrix)):
        nodes[i].data=[i]
    #Making the similarity matrix
    #clusterMatrix=makeClusterMatrix(fibers)
    #n is used to determine the stopping point
    n=1
    #while there is more than one cluster
    while(n<len(clusterMatrix)):
        #find the minimum non-zero entry in the matrix
        minEntry=1000
        x = 0
        y = 0
        for i in range(len(clusterMatrix)):
            for j in range(len(clusterMatrix)):
                if(clusterMatrix[i][j]<minEntry and clusterMatrix[i][j]!=0):
                    minEntry=clusterMatrix[i][j]
                    x = i
                    y = j
        #set the x column equal to the min of the x and y columns
        #set the y column equal to 0
        #set the xth entry of each column equal to the min of the xth and yth entry of that column
        #set the yth entry of each column to 0
        #Might need to be changed. Super inefficient.
        for i in range(len(clusterMatrix)):
            clusterMatrix[x][i]=min(clusterMatrix[x][i],clusterMatrix[y][i])
            clusterMatrix[y][i]=0
            clusterMatrix[i][x]=min(clusterMatrix[i][x],clusterMatrix[i][y])
            clusterMatrix[i][y]=0
        #newNode contains our new cluster
        newNode=Tree()
        
        #find the node that represents the cluster containing x
        currNode1=nodes[x]
        while(currNode1.parent!=None):
            if(currNode1.parent.data!=None):
                currNode1=currNode1.parent
        #this node becomes the left child of our new cluster.
        newNode.left=currNode1
        currNode1.parent=newNode
        
        #repeat for y
        currNode2=nodes[y]
        while(currNode2.parent!=None):
            if(currNode2.parent.data!=None):
                currNode2=currNode2.parent
        newNode.right=currNode2
        currNode2.parent=newNode
        
        #the cluster's data contains the data for both of its subclusters
        newData=[0 for i in range(len(currNode1.data)+len(currNode2.data))]
        for i in range(len(currNode1.data)):
            newData[i]=currNode1.data[i]
        for i in range(len(currNode2.data)):
            newData[i+len(currNode1.data)]=currNode2.data[i]
        newNode.data=newData
        exceptions=[]
        for i in range(len(nodes)):
            first=True
            for j in range(len(exceptions)):
                if(i==exceptions[j]):
                    first=False
            if(i!=x and i!=y and first):
                currentNode=nodes[i]
                newParent=Tree()
                while(currentNode.parent!=None):
                    currentNode=currentNode.parent
                if(currentNode.data!=newNode.data):
                    currentNode.parent=newParent
                    newParent.left=currentNode
                    newParent.data=currentNode.data
                    for j in range(len(newParent.data)):
                        exceptions.append(newParent.data[j])
        
        n=n+1
    #finds the root when the clustering is complete
    root=nodes[0]
    while(root.parent!=None):
            root=root.parent
    #the root is returned. We may want to return the array nodes, which contains the leaves instead
    #I'm not really sure how making "cuts" works
    return nodes
    
def findKthLevel(nodes,k):
    exceptions=[]
    kLevel=[0 for i in range(len(nodes)-k)]
    next=0
    for i in range(len(nodes)):
        first=True
        for j in range(len(exceptions)):
            if(i==exceptions[j]):
                first=False
        if(first):
            currentNode=nodes[i]
            n=0
            while(n<k):
                currentNode=currentNode.parent
                n=n+1
            kLevel[next]=currentNode.data
            next=next+1
            for j in range(len(currentNode.data)):
                exceptions.append(currentNode.data[j])
    clustering=[0 for i in range(len(nodes))]
    for i in range(len(kLevel)):
        for j in range(len(kLevel[i])):
            clustering[kLevel[i][j]]=i
    return clustering

def main():
    #read in the set of long fibers, selects and reads in a random subset
    #the subset is stored in a txt file
    #fibers = readFibers(10, 'random')
    memoryAddresses=getRandFibers(10)[0]
    fibers=readFibers(memoryAddresses)
    #Generate the similarity matrix for input fibers and distance type
    clusterMatrix=makeClusterMatrix(fibers)
    #cluster the fibers based on the given similarity matrix
    nodes=agglomCluster(clusterMatrix,0)
    #return two clusterings of the fibers (arbitrary)
    for i in range(2):
        print findKthLevel(nodes,i+4)

if __name__ == "__main__":

    main()