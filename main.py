from GenomeData import simulateData, readData
import params
import pickle
import os

plot1 = []
plot2 = []

def getResults(length, levels, numIters, mutationRate, compressionFunc):
    runTimes = []
    storages = []
    for level in levels:
        overallRunTime = 0.0
        overallStorage = 0.0
        for i in range(numIters):
            if params.datatype == 'file':
                dataset, rootRef = readData.fromFile( params.filepath )
            else:
                dataset, rootRef, root = simulateData.simulatePopulation(length, 2, level, mutationRate)
            runningTime, totalStored, _ , _ = compressionFunc(dataset, rootRef, verbose = params.verbose)
            overallRunTime += runningTime
            overallStorage += totalStored
        runTimes.append( overallRunTime / numIters )
        storages.append( overallStorage / numIters )
    return runTimes, storages

for label, func in zip(params.funcLabels, params.compressionFuncs):
    if params.datatype == 'file':
        runTimes, storages = getResults(params.length, [1], 
            1, params.mutationRate, func)
    else: 
        runTimes, storages = getResults(params.length, params.levels, 
            params.numIterations, params.mutationRate, func)        
    plot1.append( (params.levels, runTimes, label) ) 
    plot2.append( (params.levels, storages, label) )
    print(label)

with open("results.pkl", "wb") as f:
    pickle.dump([ plot1, plot2 ], f, 2)

if params.datatype == 'file':
    os.system('python Visualization/plotBar.py RunTimePython.pdf CompressionPython.pdf')
else:
    os.system('python Visualization/plotLine.py RunTimePython.pdf CompressionPython.pdf')