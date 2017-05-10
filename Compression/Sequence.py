import sys
import copy
import numpy as np

class Cell:
    def __init__(self, index, seqChar, refChar, refNum):
        self.index = index
        self.seqChar = seqChar
        self.refChar = refChar
        self.refNum = refNum
        self.penalty = 1
        self.mismatches = []
        self.stateChanges = []
        
    def updateFrom(self, prevColumn, maxPenalty):
        mismatchPenalty = 1 if self.seqChar != self.refChar else 0
        bestPrevCell = None
        bestPenalty = sys.maxsize

        for prevCell in prevColumn:
            stateChangePenalty = 1 if prevCell.refNum != self.refNum else 0
            if prevCell.penalty + mismatchPenalty +  stateChangePenalty < bestPenalty:
                bestPenalty = prevCell.penalty + mismatchPenalty +  stateChangePenalty
                bestPrevCell = prevCell      
        
        if bestPenalty > maxPenalty:
            return False, maxPenalty
        
        if bestPenalty + 1 < maxPenalty:
            maxPenalty = bestPenalty + 1
                
        mismatch = [ (self.index, self.refChar) ] if mismatchPenalty == 1 else []
        stateChange = [ (self.index, self.refNum) ] if bestPrevCell.refNum != self.refNum else []

        self.penalty = bestPenalty
        self.mismatches = bestPrevCell.mismatches + mismatch
        self.stateChanges = bestPrevCell.stateChanges + stateChange
        
        return True, maxPenalty
        
    def __lt__(self, other):
        return self.penalty < other.penalty
        
        
class CompressedSeq:
    def __init__(self, seq, refs, full=False):
        self.stateChanges = []
        self.mismatches = []
        self.totalStored = len(seq)
        #self.indices = self._getIndices(seq, refs)
        self.indices = self._getIndices2(seq, refs)
        if full:
            self._compressFull(seq, refs)
        else:
            if len(refs) > 40:
                self._compressNumpy(seq, refs)
            else:
                self._compress(seq, refs)
    
    def _getIndices(self, seq, refs):
        differIndices = np.zeros( len(seq), dtype=bool)
        for ref in refs:
            seqArr = np.array( list(seq) )
            refArr = np.array( list(ref) )
            differIndices = np.logical_or( differIndices, seqArr != refArr )
        return np.where( differIndices == True )[0]

    def _getIndices2(self, seq, refs):
        differIndices = []
        for i in range( len(seq) ):
            for ref in refs:
                if seq[i] != ref[i]:
                    differIndices.append(i)
                    break
        return differIndices

    def _compressFull(self, seq, refs):
        column = []
        for refNum, ref in enumerate(refs):
            cell = Cell(-1, ' ', ' ', refNum)
            cell.stateChanges = [ (-1, refNum) ]
            column.append( cell )
            
        for index in self.indices:
            seqChar = seq[index]
            prevColumn = copy.copy(column)
            column = []
            maxPenalty = sys.maxsize
            for refNum, ref in enumerate(refs):
                cell = Cell( index, seqChar, ref[index], refNum)
                boolAdd, maxPenalty = cell.updateFrom(prevColumn, maxPenalty)
                if boolAdd: 
                    column.append(cell)
            
        bestCell = min(column)
        self.totalStored, self.stateChanges, self.mismatches = \
            bestCell.penalty, bestCell.stateChanges, bestCell.mismatches
            
    def _compress(self, seq, refs):
        column = []
        for i in range(len(refs)):
            column.append((1,i))
            
        for index in self.indices:
            seqChar = seq[index]
            prevColumn = copy.copy(column)
            column = []
            maxPenalty = sys.maxsize
            for refNum, ref in enumerate(refs):
                bestPenalty = sys.maxsize
                mismatchpenalty = 1 if ref[index] != seqChar else 0

                for pen, prevRefNum in prevColumn:
                    stateChangePenalty = 1 if refNum != prevRefNum else 0
                    penalty = pen + mismatchpenalty + stateChangePenalty
                    if penalty < bestPenalty: 
                        bestPenalty = penalty
                if bestPenalty + 1 < maxPenalty:
                    maxPenalty = bestPenalty + 1
                if bestPenalty <= maxPenalty:
                    column.append( (bestPenalty, refNum) )
            
        self.totalStored = min(column)[0]

    def _compressNumpy(self, seq, refs):
        n = len(refs)
        column = np.ones(n)
            
        for index in self.indices:
            seqChar = seq[index]
            prevColumn = np.copy(column) + 1
            column = np.zeros(n)
            for refNum, ref in enumerate(refs):
                mismatchPenalty = 1 if ref[index] != seqChar else 0 
                prevColumn[refNum] -= 1
                column[refNum] = prevColumn.min() + mismatchPenalty
                prevColumn[refNum] += 1
            
        self.totalStored = column.min()
        
'''
#Example Usage:
seq = 'CACGTCTAGTAATGTG'
refs = [ 'AACGACTAGTAATTTG', 'CACGTCTAGTAATTCG', 'AACTACTGGTAATGTG']
compressed = CompressedSeq(seq, refs, full = True)
print( compressed.totalStored )
print( compressed.stateChanges )
print( compressed.mismatches )
'''
