from Compression import Sequence
from GenomeData import simulateData
import multiprocessing as mp
from functools import partial
import time
import numpy as np
import pickle
import random

def compressNaive(dataset, rootRef, full = False, verbose = False):
    np.random.shuffle(dataset)
    start = time.clock()
    totalStored = 0.0
    numStateChanges = 0.0
    numMismatches = 0.0
    
    for i,seq in enumerate(dataset):
        compressed = Sequence.CompressedSeq(seq, [ rootRef ], full = full)
        totalStored += compressed.totalStored
        numStateChanges += len( compressed.stateChanges )
        numMismatches += len( compressed.mismatches )
        if verbose: print("Compressed {} / {} sequences".format(i, len(dataset)))
    
    totalStored /= len( dataset )
    numStateChanges /= len( dataset )
    numMismatches /= len( dataset )
    runningTime = (time.clock() - start) / len( dataset )
        
    return runningTime, totalStored, numStateChanges, numMismatches
    
def compressStack(dataset, rootRef, full = False, verbose = False):
    np.random.shuffle(dataset)
    start = time.clock()
    totalStored = 0.0
    numStateChanges = 0.0
    numMismatches = 0.0
    
    for i,seq in enumerate(dataset):
        compressed = Sequence.CompressedSeq(seq, [rootRef] + dataset[:i], full = full)
        totalStored += compressed.totalStored
        numStateChanges += len( compressed.stateChanges )
        numMismatches += len( compressed.mismatches )
        if verbose: print("Compressed {} / {} sequences".format(i, len(dataset)))
        
    totalStored /= len( dataset )
    numStateChanges /= len( dataset )
    numMismatches /= len( dataset )
    runningTime = (time.clock() - start) / len( dataset )
        
    return runningTime, totalStored, numStateChanges, numMismatches

def f(call, dataset, rootRef, numRefs, full, verbose):
    totalStored = 0.0
    numStateChanges = 0.0
    numMismatches = 0.0
    
    for i in call:
        seq = dataset[i]
        if i < numRefs:
            compressed = Sequence.CompressedSeq(seq, [rootRef], full = full)
        else: 
            compressed = Sequence.CompressedSeq(seq, [rootRef] + 
                                        dataset[:numRefs], full = full)        
        if verbose: print("Compressed {} / {} sequences".format(i, len(dataset)))
        
        totalStored += compressed.totalStored
        numStateChanges += len( compressed.stateChanges )
        numMismatches += len( compressed.mismatches )
    
    return totalStored, numStateChanges, numMismatches
        
def compressTree(dataset, rootRef, numRefs, full = False, verbose = False):
    np.random.shuffle(dataset)
    start = time.clock()
    totalStored = 0.0
    numStateChanges = 0.0
    numMismatches = 0.0

    if numRefs < 1: 
        	numRefs = int( len(dataset) * numRefs )
    
    calls = []
    pool = mp.Pool( mp.cpu_count() )
    func = partial(f, dataset = dataset, rootRef = rootRef, full = full, verbose = verbose, numRefs = numRefs)    
    seqList = list( range( len(dataset) ) )
    random.shuffle( seqList )
    for i in range( mp.cpu_count() ):
        i_start = i * (len(dataset) / float(mp.cpu_count()) )
        i_end = (i + 1) * (len(dataset) / float(mp.cpu_count()) )
        if seqList[int(i_start):int(i_end)] != []: 
             calls.append( seqList[int(i_start):int(i_end)] )
    results = pool.map(func, calls)
    pool.close()
        
    for result in results:
        totalStored += result[0]
        numStateChanges += result[1]
        numMismatches += result[2]
        
    totalStored /= len( dataset )
    numStateChanges /= len( dataset )
    numMismatches /= len( dataset )
    runningTime = (time.clock() - start) / len( dataset )
        
    return runningTime, totalStored, numStateChanges, numMismatches

'''
dataset, rootRef, root = sim.simulatePopulation(100000, 2, 5, .001)
runningTime, totalStored, _ , _ = compressNaive(dataset, rootRef)
print("Running Time:", runningTime)
print("Average Compression:", totalStored)
print("---------------------------")
runningTime, totalStored, _ , _ = compressTree(dataset, rootRef, 5)
print("Running Time:", runningTime)
print("Average Compression:", totalStored)
print("---------------------------")
runningTime, totalStored, _ , _ = compressTree(dataset, rootRef, 10)
print("Running Time:", runningTime)
print("Average Compression:", totalStored)
print("---------------------------")
runningTime, totalStored, _ , _ = compressTree(dataset, rootRef, 20)
print("Running Time:", runningTime)
print("Average Compression:", totalStored)
print("---------------------------")
runningTime, totalStored, _ , _ = compressStack(dataset, rootRef)
print("Running Time:", runningTime)
print("Average Compression:", totalStored)
print("---------------------------")
'''
