'''
This file calculates agreement between two clusterings of the same data set.
I did not have time to get the compareCLusterings method to appropriately
take the curves not included in the ground truth into account.
@author Yuen Hsi
'''
import numpy, math

#This method compares each pair of fibers in the two clusterings and
#categorizes their agreement.
def compareClusterings(groundTruth, clustering):
    numClusG=0
    for i in range(len(groundTruth)):
        if(groundTruth[i]=='nc'):
            pass
        elif(groundTruth[i]>numClusG):
            numClusG=groundTruth[i]
        else:
            pass
    numClusC=int(max(clustering))
    contingencyTable=numpy.zeros(shape=(2,2))
    for i in range(len(groundTruth)):
        for j in range(len(clustering)):
            if(i==j):
                pass
            elif(groundTruth[i]=='nc' or groundTruth[j]=='nc'):
                pass
            else:
                inG=0
                inC=0
                if(groundTruth[i]==groundTruth[j]):
                    inG=1
                if(clustering[i]==clustering[j]):
                    inC=1
                contingencyTable[inG][inC]+=1
    contingencyTable=contingencyTable/2
    return contingencyTable
                           
#This method calculates the Rand Index for an input clustering comparison
def randIndex(pairCategoryTable):
	a=pairCategoryTable[0][0]
	b=pairCategoryTable[0][1]
	c=pairCategoryTable[1][0]
	d=pairCategoryTable[1][1]
	M=a+b+c+d
	return (a+d)/M

#This method calculates the Adjusted Rand Index
def adjustedRandIndex(pairCategoryTable):
	a=pairCategoryTable[0][0]
	if(a==0):
	    return 0
	b=pairCategoryTable[0][1]
	c=pairCategoryTable[1][0]
	d=pairCategoryTable[1][1]
	M=a+b+c+d
	if(a==M or d==M):
	    return 1
	elif(b==M or c==M):
	    return 0
	else:
	    m1=a+b
	    m2=a+c
	    if((a-(m1*m2)/M)/((m1+m2)/2-(m1*m2)/M)>0):
	        return (a-(m1*m2)/M)/((m1+m2)/2-(m1*m2)/M)
	    else:
	        return 0
	
	
def main():
    #fibers=[0,1,2,3,4]
    #n=len(fibers)
    groundTruth=[0,1,1,2,2]
    clustering=[0,1,0,0,2]
    #contingencyTable=makeContingencyTable(groundTruth,clustering)
    #pairType=makePairCategoryTable(n,contingencyTable)
    pairType=compareClusterings(groundTruth,clustering)
    print pairType
    print randIndex(pairType)
    print adjustedRandIndex(pairType)

if __name__ == "__main__":

    main()