import numpy as np
from itertools import count
import copy
import random
#import pydot
#from PIL import Image

def simulateOneSeq(seqLength, numRefs, numCuts, mutationRate):
    
    refs = [ "".join( np.random.choice(['A','C','G','T'], size = seqLength) ) for _ in range(numRefs) ]
    cutIndices = [0] + sorted( np.random.randint(1,seqLength,size=numCuts) ) + [seqLength]
    mutationIndices = sorted( np.random.randint(1, seqLength, size = int(mutationRate * seqLength)) )
    
    seq = ""
    currentRef = random.choice( refs )
    for cut in range(1,numCuts+2):
        refs_copy = copy.copy( refs )
        refs_copy.remove( currentRef )
        currentRef = random.choice( refs_copy )
        seq += currentRef[ cutIndices[cut-1] : cutIndices[cut] ]
    
    seq = list(seq) 
    for mutation in mutationIndices:  
        bases = ['A','C','G','T']
        bases.remove( seq[mutation] )
        seq[mutation] = random.choice( bases )
    seq = "".join(seq)
    
    return seq, refs, cutIndices, mutationIndices 
    
'''
#Example Usage:    
seqLength = 10000, numRefs = 10
numCuts = 10, mutationRate = .01

seq, refs, cutIndices, mutationIndices = simulateOneSeq( seqLength, numRefs, numCuts, mutationRate)
compressed = CompressSeq.CompressedSeq( seq, refs, full=True )
print( compressed.totalStored )
print( compressed.stateChanges )
print( compressed.mismatches )
'''

class seqNode:
    _ids = count(0)
    
    def __init__(self, genome):
        self.length = len(genome)
        self.genome = genome
        self.children = []
        
    def _mutateSeq(self, mutationRate):
        mutations = np.random.choice( [False,True], size = self.length, 
                                     p = [1 - mutationRate, mutationRate] )
        mutatedGenome = np.copy( self.genome )
        mutatedGenome[mutations] = np.random.choice(['A', 'C', 'G', 'T'], size = int(mutations.sum()) )
        return mutatedGenome
        
    def makeChildren(self, numChildren, mutationRate):
        for i in range(numChildren):
            child = seqNode( self._mutateSeq(mutationRate) )
            self.children.append( child )        
        return self.children
        
    def __str__(self):
        return "".join(self.genome)

def visualizeHelper(node, treeNode, tree):
    for child in node.children:
        if child.children != []:
            childNode = pydot.Node(next(seqNode._ids), label = "".join(child.genome), shape="box")
        else:
            childNode = pydot.Node(next(seqNode._ids), label = "".join(child.genome), style="filled", fillcolor="green", shape="box" )
        tree.add_node(childNode)
        tree.add_edge(pydot.Edge(treeNode, childNode, label = ''))
        visualizeHelper(child, childNode, tree)
        
def visualize(root):
    tree = pydot.Dot(graph_type='graph')
    rootNode = pydot.Node(next(seqNode._ids) , label = "".join(root.genome), style="filled", fillcolor="red", shape="box")
    tree.add_node(rootNode)
    visualizeHelper(root, rootNode, tree)
    
    tree.write_png('tree.pdf')
    Image.open('tree.png').show()
    
def simulatePopulation(seqLength, numChildren, numLevels, mutationRate, visualize = False):
    
    rootRef = np.random.choice(['A','C','G','T'], size = seqLength)
    root = seqNode(rootRef)
    nodes = [ root ]

    for i in range(numLevels):
        children = []
        for node in nodes:
            children += node.makeChildren( numChildren, mutationRate )
        nodes = children        
        
    seqs = [str(node) for node in nodes]
        
    return seqs, str(root), root

'''
#Example Usage
seqs, rootRef, root = simulatePopulation(10000, 2, 8, .1)
#visualize(root)
'''
    
