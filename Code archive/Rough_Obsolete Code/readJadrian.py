#This file reads in Jadrian's 10 trk files and puts them in a single trk file. I (Zach) wrote
#this file under the assumption that we would be only the fibers that Jadrian had clustered.
#The output track file is not useful for data collection, but it gave us an interesting image 
#for the paper. This file was modified to create getJadrianCluster, which returns the ground truth
#clustering for the whole set of long fibers

import math, random, struct, numpy
import os

#stores the memory addresses of all the fibers
def getMemoryAddresses():
    directoryPath=os.getcwd()
    memoryAddresses=[0 for i in range(10)]
    #numpy.zeros(shape=(10))
    totalNumF=0
    for i in range(10):
        f = open(directoryPath + '/GTClusters/jadrian' + str(i) +'.trk', mode='rb')
        binContent = f.read()
        #Skip the bytes in the header
        offset=1000
        #Number of fibers in the data set (on our current set, it is about 250000)
        numF=struct.unpack("i", binContent[988:992])[0]#Number of fibers in the set
        totalNumF=totalNumF+numF
        memoryAddresses[i]=numpy.zeros(shape=(numF,2))
        for j in range(numF):
            memoryAddresses[i][j][0]=offset
            tempLength=struct.unpack("i", binContent[offset:offset+4])[0]
            memoryAddresses[i][j][1]=int(tempLength)
            offset=12*tempLength+offset+4        
    return memoryAddresses, totalNumF

#Reads in all the fibers into a numpy array
def getFibers(memoryAddresses,totalNumF):
    #this keeps track of location of the next fiber
    currentNumF=0
    fibers=[0 for i in range(totalNumF)]#numpy.zeros(shape=(totalNumF))
    directoryPath=os.getcwd()
    for i in range(10):
        f = open(directoryPath + '/GTClusters/jadrian' + str(i) +'.trk', mode='rb')
        binContent=f.read()
        numF=struct.unpack("i", binContent[988:992])[0]#Number of fibers in the set
        #Skip the bytes in the header
        offset=1000
        for j in range(numF):
            #find the number of points in each fiber
            numPoints=int(memoryAddresses[i][j][1])
            offset=int(memoryAddresses[i][j][0]+4)
            #set the ith entry of fiberArray equal to a blank array with the correct number of points
            fibers[currentNumF]=numpy.zeros(shape=(numPoints,3))
            #fill the array corresponding to a fiber with points
            for x in range(numPoints):
                for y in range(3):
                    fibers[currentNumF][x][y]=struct.unpack("f", binContent[offset:offset+4])[0]
                    offset=offset+4
            currentNumF=currentNumF+1
    return fibers

#This method copies the header from the first cluster and the fibers from all the clusters
#into a single track file
def writeTrkFile(fibers,memoryAddresses,totalNumF):
    numF=len(fibers)
    print numF
    directoryPath=os.getcwd()
    newFile = open(directoryPath + "/jadrianSubSet.trk", "w")
    for i in range(10):
        f = open(directoryPath + '/GTClusters/jadrian' + str(i) +'.trk', mode='rb')
        binContent=f.read()
        numF=struct.unpack("i", binContent[988:992])[0]#Number of fibers in the set
        #Copy the header from the first cluster (except for the number of fibers)
        if(i==0):
            header=binContent[0:988]
            newFile.write(header)
            newFile.write(struct.pack('<i',totalNumF))
            endHeader=binContent[992:1000]
            newFile.write(endHeader)
        for j in range(numF):
            offset=int(memoryAddresses[i][j][0])
            length=int(memoryAddresses[i][j][1])
            newFile.write(binContent[offset:offset+12*length+4])

#This method writes the ground truth clustering of the subset to a txt file
#However, this clustering isn't what we want and it is in a bad format.
def getClustering(memoryAddresses):
    gtCluster=[0 for i in range(10)]
    currentIndex=0
    for i in range(10):
        fibersInCluster=int(len(memoryAddresses[i]))
        gtCluster[i]=[0 for k in range(fibersInCluster)]
        for j in range(fibersInCluster):
            gtCluster[i][j]=currentIndex
            currentIndex=currentIndex+1
    directoryPath=os.getcwd()
    newFile = open(directoryPath + "/groundTruth.txt", "w")
    newFile.write(str(gtCluster))

def main():
    temp=getMemoryAddresses()
    memoryAddresses=temp[0]
    totalNumF=temp[1]
    fibers=getFibers(memoryAddresses,totalNumF)
    writeTrkFile(fibers,memoryAddresses,totalNumF)
    getClustering(memoryAddresses)

if __name__ == "__main__":

    main()
            