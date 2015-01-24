'''
We used this file to generate a managable set of fibers from our complete
tractograchy data set (about 250000 fibers). Both short and long fibers are
filtered out. The resulting data set contains about 30,000 fibers for the
threshold values we used. 
@author Yuen Hsi
'''

import math, random, struct, numpy
import os

#stores the memory addresses of all the fibers
def getMemoryAddresses():
    directoryPath=os.getcwd()
    f = open(directoryPath + '/ImportantTrk/dti.trk', mode='rb')
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

#Reads in the fibers
def getFibers(memoryAddresses):
    directoryPath=os.getcwd()
    f = open(directoryPath + '/ImportantTrk/dti.trk', mode='rb')
    binContent=f.read()
    numF=struct.unpack("i", binContent[988:992])[0]#Number of fibers in the set
    #Skip the bytes in the header
    offset=1000
    fibers=[0 for i in range(numF)]
    for i in range(len(memoryAddresses)):
        #find the number of points in each fiber
        numPoints=memoryAddresses[i][1]
        offset=memoryAddresses[i][0]+4
        #set the ith entry of fiberArray equal to a blank array with the correct number of points
        fibers[i]=numpy.zeros(shape=(numPoints,3))
        #fill the array corresponding to a fiber with points
        for x in range(numPoints):
            for y in range(3):
                fibers[i][x][y]=struct.unpack("f", binContent[offset:offset+4])[0]
                offset=offset+4
    return fibers

#This method filters out fibers with length above highThreshold or length below
#lowThreshold
def selectLongFibers(fibers,memoryAddresses,highThreshold,lowThreshold):
    #This array stores the indices of fibers that we are not filtering out
    fibersUsed=[]
    directoryPath=os.getcwd()
    #Test whether each fiber is too long or too short
    for i in range(len(fibers)):
        if(aboveThreshold(fibers[i],highThreshold,lowThreshold)):
            fibersUsed.append(memoryAddresses[i])
    #Write the indices of the selected fibers to a text file
    newFile = open(directoryPath + "/ImportantTrk/fiberIndices.txt", "w")
    newFile.write(str(fibersUsed))
    
    return fibersUsed
    
def aboveThreshold(fiber,highThreshold, lowThreshold):
    diff=fiber[0:-1,:]-fiber[1:,:]
    length=sum(numpy.sqrt(sum(diff*diff,0)))
    if(length<highThreshold):
        if(length>lowThreshold):
            return True
        else:
            return False
    else:
        return False

#This method writes the subset of fibers to a trk file
def writeTrkFile(memoryAddresses):
    numF=len(memoryAddresses)
    print numF
    directoryPath=os.getcwd()
    f = open(directoryPath + '/dti.trk', mode='rb')
    binContent = f.read()
    newFile = open(directoryPath + "/ImportantTrk/newTrack.trk", "w")
    header=binContent[0:988]
    newFile.write(header)
    newFile.write(struct.pack('<i',numF))
    endHeader=binContent[992:1000]
    newFile.write(endHeader)
    for i in range(numF):
        offset=memoryAddresses[i][0]
        length=memoryAddresses[i][1]
        #print offset
        newFile.write(binContent[offset:offset+12*length+4])

def main():
    memoryAddresses=getMemoryAddresses()
    fibers=getFibers(memoryAddresses)
    #3rd argument upper bound
    #4th argument lower bound
    longFiberAddresses=selectLongFibers(fibers,memoryAddresses,36,25)
    writeTrkFile(longFiberAddresses)

if __name__ == "__main__":

    main()