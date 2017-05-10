from Compression import Compress
from functools import partial

#datatype should be either 'simulate' or 'file'
datatype = 'simulate'

#File path to saved genome data
filepath = 'GenomeData/chr17_genomes.csv.gz'

#params for simulating data 
length = 5000    #length of each simulated sequence
levels = [3,4,5,6,7]    #number of levels in simulation tree
numIterations = 1    #number of iterations for simulation
mutationRate = .005    #mutation rate of each sequence

#compression functions to apply to data
#must beone of Compress.compressNaive, 
# partial(Compress.compressTree,numRefs= somefloat)
# or Compress.compressStack
compressionFuncs = [ Compress.compressNaive, 
partial(Compress.compressTree,numRefs=.02),
partial(Compress.compressTree,numRefs=.05),
partial(Compress.compressTree,numRefs=.10) ]

#labels for each compression function
funcLabels = [ 'Naive',
'Tree (k=.02)',
'Tree (k=.05)',
'Tree (k=.10)' ]

#change to False to hide user output
verbose = True