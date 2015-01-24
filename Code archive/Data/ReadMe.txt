This folder contains some of the "data" that we collected


groundTruth.txt is the ground truth clustering collected by Jadrian

fiberIndices.txt contains the indices of all the curves that Jadrian curves

sampleData is a data set containing Rand and Adjusted Rand indices for 25 subsets of 100 fibers.
The [w,x,y,z] entry is the wth evaluation method performed on the yth clustering algorithm
using xth dissimilarity measure for the zth subset.

w   
0 = Rand Index
1 = Adjusted Rand Index

y
0 = Single Linkage Agglomerative Clustering
1 = Spectral Clustering

x
0 = Closest Point Distance
1 = Mean Minimum Distance
2 = Hausdorff Distance

Subsets.txt contains the indices of the curves in each subset. By storing the subsets, we can repeat
our clusterings and check our results.