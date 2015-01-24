'''
This file extracts the ground truth clustering of the set of long fibers
that we sent to Jadrian. The clustering is written to a text file.
@author Yuen Hsi
'''

import math, random, struct, numpy
import os

#stores the memory addresses of all the long fibers
def getMemoryAddresses():
    directoryPath=os.getcwd()
    #numpy.zeros(shape=(10))
    f = open(directoryPath + '/ImportantTrk/longFibers.trk', mode='rb')
    binContent = f.read()
    offset=1000
    #Number of fibers in the data set (on our current set, it is about 250000)
    numF=struct.unpack("i", binContent[988:992])[0]#Number of fibers in the set
    memoryAddresses=[[0,0] for i in range(numF)]
    for j in range(numF):
        memoryAddresses[j][0]=offset
        tempLength=struct.unpack("i", binContent[offset:offset+4])[0]
        memoryAddresses[j][1]=int(tempLength)
        offset=12*tempLength+offset+4        
    return memoryAddresses

#gets all the fibers
def getFibers(memoryAddresses):
    fibers=[0 for i in range(len(memoryAddresses))]#numpy.zeros(shape=(totalNumF))
    directoryPath=os.getcwd()
    f = open(directoryPath + '/ImportantTrk/longFibers.trk', mode='rb')
    binContent=f.read()
    numF=struct.unpack("i", binContent[988:992])[0]#Number of fibers in the set
    #Skip the bytes in the header
    offset=1000
    for j in range(numF):
        #find the number of points in each fiber
        numPoints=int(memoryAddresses[j][1])
        offset=int(memoryAddresses[j][0]+4)
        #set the ith entry of fiberArray equal to a blank array with the correct number of points
        fibers[j]=numpy.zeros(shape=(numPoints,3))
        #fill the array corresponding to a fiber with points
        for x in range(numPoints):
            for y in range(3):
                fibers[j][x][y]=struct.unpack("f", binContent[offset:offset+4])[0]
                offset=offset+4
    return fibers

#Gets Jadrian's clusterings of the large data set. We are assuming that if two 
#fibers have the same first point, they are the same fiber. Most of the entries
#in the groundTruth clustering contain 'nc' for not clustered. The ground truth
#clustering is stored in a text file.
def getCluster(fibers):
    clustering=['nc' for i in range(len(fibers))]
    directoryPath=os.getcwd()
    for i in range(10):
        print i
        f = open(directoryPath + '/GTClusters/jadrian' + str(i) +'.trk', mode='rb')
        binContent=f.read()
        numF=struct.unpack("i", binContent[988:992])[0]#Number of fibers in the set
        offset=1000
        for x in range(numF):
            numPoints=struct.unpack("i", binContent[offset:offset+4])[0]
            offset=offset+4
            currentFiber=numpy.zeros(shape=(3))
            for y in range(3):
                currentFiber[y]=struct.unpack("f", binContent[offset:offset+4])[0]
                offset=offset+4
            offset=offset+12*numPoints-12
            for z in range(len(fibers)):
                if(numpy.array_equal(fibers[z][0],currentFiber)):
                    #print fibers[z][0]
                    #print currentFiber
                    clustering[z]=i
                    break
    newFile = open(directoryPath + "/groundTruth.txt", "w")
    newFile.write(str(clustering))
    return clustering

def main():
    memoryAddresses=getMemoryAddresses()
    fibers=getFibers(memoryAddresses)
    clustering= getCluster(fibers)
    #writeTrkFile(fibers,memoryAddresses,totalNumF)
    #getClustering(memoryAddresses)

if __name__ == "__main__":

    main()