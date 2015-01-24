import numpy, math

def makeContingencyTable(groundTruth, clustering):
    gLen=len(groundTruth)
    cLen=len(clustering)
    contingencyTable=numpy.zeros(shape=(gLen,cLen))
    for i in range(gLen):
		for j in range(cLen):
			fiberInCommon=0
			for x in range(len(groundTruth[i])):
				for y in range(len(clustering[j])):
					if(groundTruth[i][x]==clustering[j][y]):
						fiberInCommon+=1
			contingencyTable[i][j]=fiberInCommon
    return contingencyTable
	
def makePairCategoryTable(n, contingencyTable):
	pairCategoryTable=numpy.zeros(shape=(2,2))
	s=len(contingencyTable)
	r=len(contingencyTable[0])
	a=0
	for x in range(s):
		for y in range(r):
			a=a+0.5*contingencyTable[x][y]*(contingencyTable[x][y]-1)
	pairCategoryTable[0][0]=a
	b=0
	for x in range(r):
		u=0
		for y in range(s):
			u=u+contingencyTable[y][x]
		b=b+0.5*u*(u-1)
	pairCategoryTable[0][1]=b-a
	b=pairCategoryTable[0][1]
	c=0
	for x in range(s):
		v=0
		for y in range(r):
			 v=v+contingencyTable[x][y]
		c=c+0.5*v*(v-1)
	pairCategoryTable[1][0]=c-a
	c=pairCategoryTable[1][0]
	pairCategoryTable[1][1]=0.5*n*(n-1)-a-b-c
	return pairCategoryTable

def randIndex(n,pairCategoryTable):
	a=pairCategoryTable[0][0]
	d=pairCategoryTable[1][1]
	M=0.5*n*(n-1)
	return (a+d)/M

def adjustedRandIndex(n,pairCategoryTable):
	a=pairCategoryTable[0][0]
	if(a==0):
	    return 0
	b=pairCategoryTable[0][1]
	c=pairCategoryTable[1][0]
	d=pairCategoryTable[1][1]
	M=0.5*n*(n-1)
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
    fibers=[0,1,2,3,4,5,6,7,8,9]
    n=len(fibers)
    groundTruth=[[0], [1], [2, 4, 7, 6, 8], [3], [5], [9]]
    clustering=[[0], [1], [2, 4, 7, 6, 8, 3], [5], [9]]
    contingencyTable=makeContingencyTable(groundTruth,clustering)
    pairType=makePairCategoryTable(n,contingencyTable)
    print pairType
    print randIndex(n,pairType)
    print adjustedRandIndex(n,pairType)

if __name__ == "__main__":

    main()
	
	
	
		
			