'''
This file reads in a trk file and returns an array containing a subset of the fibers 
and a ground truth clustering of that subset. This file takes the output of 
getJadrianCluster as input. 
@author Yuen Hsi
'''

import math, random, struct, numpy
import os, ast

#This method gets the offset and number of points of each fiber in our trk file
def readinFibersUtil():
    directoryPath=os.getcwd()
    f = open(directoryPath + '/ImportantTrk/longFibers.trk', mode='rb')
    binContent = f.read()
    #Skip the bytes in the header
    offset=1000
    #Number of fibers in the data set (on our current set, it is about 250000)
    numF=struct.unpack("i", binContent[988:992])[0]#Number of fibers in the set
    memoryAddresses=[[0,0] for i in range(numF)]
    for i in range(numF):
        memoryAddresses[i][0]=offset
        tempLength=struct.unpack("i", binContent[offset:offset+4])[0]
        memoryAddresses[i][1]=tempLength
        offset=12*tempLength+offset+4
    return memoryAddresses

#This method randomly selects numF fibers. It returns their memoryAddresses
#and their indices (fiber number)
def getRandFibers(numF):
    directoryPath=os.getcwd()
    f = open(directoryPath + '/ImportantTrk/longFibers.trk', mode='rb')
    binContent = f.read()
    memoryAddresses=readinFibersUtil()
    fibersUsed=[]
    while(len(fibersUsed)!=numF):
        x=random.randint(0,len(memoryAddresses))
        #print x
        if (fibersUsed.count(x)!=0):
            pass
        else:
            fibersUsed.append(x)
                
    fiberIndices=sorted(fibersUsed)
    #print fiberIndices
    
    tempList=[0 for i in range(numF)]
    for i in range(numF):
        #print memoryAddresses[fibersUsed[i]]
        tempList[i]=memoryAddresses[fibersUsed[i]]
    memoryAddresses=tempList
    
    #print fiberIndices
    
    #newFile = open(directoryPath + "/ImportantTrk/subsetFiberIndices.txt", "w")
    #newFile.write(str(fiberIndices))
    return [memoryAddresses, fiberIndices]

#This method reads in fibers corresponding to a set of memory addresses and puts those fibers
#into an array
def readFibers(memoryAddresses):
    directoryPath=os.getcwd()
    f = open(directoryPath + '/ImportantTrk/longFibers.trk', mode='rb')
    binContent = f.read()
    fiberArray=[0 for i in range(len(memoryAddresses))]
    for i in range(len(memoryAddresses)):
        numPoints=memoryAddresses[i][1]
        offset=memoryAddresses[i][0]+4
        #print numPoints
        #set the ith entry of fiberArray equal to a blank array with the correct number of points
        fiberArray[i]=[[0 for x in range(3)] for y in range(numPoints)]
        #fill the array corresponding to a fiber with points
        for x in range(numPoints):
            for y in range(3):
                fiberArray[i][x][y]=struct.unpack("f", binContent[offset:offset+4])[0]
                offset=offset+4
    #print fiberArray
    return fiberArray

#This method returns the ground truth clustering for each fiber in the subset.
def getGTCluster(fibersUsed):
    directoryPath=os.getcwd()
    f = open(directoryPath + '/Data/groundTruth.txt', mode='rb')
    groundTruth=f.read()
    groundTruth=ast.literal_eval(groundTruth)
    numF=len(fibersUsed)
    gtCluster=['nc' for i in range(numF)]
    for i in range(numF):
        gtCluster[i]=groundTruth[fibersUsed[i]]
    return gtCluster
    
def main():
    randInfo=getRandFibers(1000)
    memoryAddresses=randInfo[0]
    fiberIndices=randInfo[1]
    fiberSubset=readFibers(memoryAddresses)
    gtSubset=getGTCluster(fiberIndices)

if __name__ == "__main__":

    main()
    
            
    
    