from __future__ import division
import numpy
import random
import math
from scipy.linalg import expm #necessary for the matrix exponentiation (to find marginal probabilities)

class DNAevo(object):
    def __init__(self,
                 bases = ["A","C","G","T"],
                 Qmatrix =[[-1.916,0.541,0.787,0.588], #Copied Q matrix from Huelsenbeck reading
                          [0.148,-1.069,0.415,0.506],
                          [0.286,0.170,-0.591,0.135],
                          [0.525,0.236,0.594,-1.355]], 
                 brl = 1):
        self.bases = bases #Here I set the four nucleotides as the elements that comprise a sequence
        self.Qmatrix = Qmatrix #Here I set the default Q matrix
        self.brl = brl #Here I set the default branchlength for DNA evolution
        
        '''        
        Now I want to calculate the transition probability matrix from the 
        Q matrix. This involves dividing all positive elements by the absolute
        value of the diagonal.
        '''
        transProbs = {} #I store the four transition probabilites in a dict as values with key "base"
        diagonals = {} #I store the diagonals in a dict as values with key "base"
        for nuc in bases:
            row = Qmatrix[bases.index(nuc)]
            diagonals[nuc] = -1*min(row)
            transProbs[nuc] = [val/(min(row)*-1) for val in row]
        self.transProbs = transProbs
        self.diagonals = diagonals
        #Qexp = self.calcMargProb() #Qexp (Q matrix exponentiated) holds the generated marginal probabilities 
        #self.statfreq = Qexp[0] #Here I store just one row of the margProb matrix (a row of the four margProb values)
        
d = DNAevo()

print d.diagonals
print d.transProbs
        
