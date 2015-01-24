'''
This method is what we would use to collect our data. It selects random subsets
from a large set of fibers. Then it obtains ground truth, spectral and
agglomerative clusterings of those subsets. Then it evaluates similarity between
clusterings using a variation of the Rand Index. Finally, it writes all of the
subsets and cluster evaluations to two separate text files. Since
our clustering algorithms were slow and our time was limited, we were unable to
collect data on clusters of significant size. 
@author Yuen Hsi
'''

from agglomCluster05 import *
from clusterEvaluation import *
from subsetFinder import *
from specCluster import *
import numpy

def main():
    #Number of Subsets to Cluster
    numSubsets=25
    #Number of Fibers in each subset
    lenSubset=100
	#stores the Rand and Adjusted Rand Indices for each clustering of each subset
    data=numpy.zeros(shape=(2,3,3,numSubsets))
	#stores the indices of the fibers in each subset
    subsets=[0 for i in range(numSubsets)]
	#test on a certain number of subsets
    for i in range(numSubsets):
		#find the subset
		fiberInfo=getRandFibers(lenSubset)
		fiberSubset=readFibers(fiberInfo[0])
		subsets[i]=fiberInfo[1]
		#method that returns the ground truth clustering of the subset
		groundTruth=getGTCluster(fiberInfo[1])
		k= 10
		for j in range(3):
			#make the similarity matrix
			simMatrix=makeClusterMatrix(fiberSubset,j)
			
			#Do single linkage agglomerative clustering
			aggTree=agglomCluster(simMatrix)
			aggCluster=findKthLevel(aggTree,lenSubset-k)
	        
			#Do spectral clustering
			sigma=findSigma(simMatrix,10,40,3)
			specCluster=list(spectralCluster(simMatrix,k,sigma))
			
			#Compare s-link to ground truth
			aggCT=compareClusterings(groundTruth,aggCluster)
			print aggCT
			print randIndex(aggCT)
			
			#compare spec to groundtruth
			specCT=compareClusterings(groundTruth,specCluster)
			print specCT
			print randIndex(specCT)
			data[0,j,0,i]=randIndex(aggCT)
			data[1,j,0,i]=adjustedRandIndex(aggCT)
			
			data[0,j,1,i]=randIndex(specCT)
			data[1,j,1,i]=adjustedRandIndex(specCT)
	#write data and subsets to 3 separate files
    directoryPath=os.getcwd()
    newFile = open(directoryPath + "/Data/data.txt", "w")
    newFile.write(str(data))
    newFile1 = open(directoryPath + "/Data/subsets.txt", "w")
    newFile1.write(str(subsets))
    #Now that we have the Rand and Adjusted Rand Indices for many subsets
    #and for each combination of measures, we could perform statistical analysis on data
    #to get meaningful results
    
if __name__ == "__main__":

    main()
			