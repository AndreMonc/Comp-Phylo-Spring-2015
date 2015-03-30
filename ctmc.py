from __future__ import division
import numpy
import random
import math
from scipy.linalg import expm #necessary for the matrix exponentiation (to find marginal probabilities)

'''
Code I wrote with lots of help from Subir. Learned a lot by studying his code.
Compared to my earlier code, this version of a continuous Markov simulation 
will be much easier to integrate with simulations on a tree.
'''

class DNAevo(object):
    def __init__(self,
                 bases = ["A","C","G","T"],
                 Qmatrix =[[-1.916,0.541,0.787,0.588], #Copied Q matrix from Huelsenbeck reading
                          [0.148,-1.069,0.415,0.506],
                          [0.286,0.170,-0.591,0.135],
                          [0.525,0.236,0.594,-1.355]], 
                 arbBrl = 1):
        self.bases = bases #Here I set the four nucleotides as the elements that comprise a sequence
        self.Qmatrix = Qmatrix #Here I set the default Q matrix
        self.arbBrl = arbBrl #Here I set the arbitrary (or default) branchlength for DNA evolution
        
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
        Qexp = self.margProbMat() #Qexp (Q matrix exponentiated) holds the generated marginal probabilities 
        self.statfreq = Qexp[0] #Here I store just one row of the margProb matrix (a row of the four margProb values)
        
    def discSamp(self, nuclist, problist, outputLength = 1):
        #Purpose of this method is to provide a random sequence of bases (but based on marginal probs) from a discrete distribution
        output = []
        for value in range(outputLength):
            cumfreq = []
            x = 0
            for prob in range(len(problist)):
                cumfreq.append(x + problist[prob])
                x = cumfreq[prob]
            rand = random.random()
            for num in cumfreq:
                if rand <= num:
                    output.append(nuclist[cumfreq.index(num)])
                    break
        return output
 
    
class contMarkov(DNAevo):
    #This first method will actually perform the continuous Markov chain simulation
    def cmSim(self, startSeq=None, seqL = 10):
        finalStateString = "" #The last states of each simulation for a given site
        if startSeq is None:
            startSeq = self.discSamp(self.bases,self.statfreq, outputLength = seqL) #Here I generate a sequence (in a list) of length 30 based on marginal probabilities
            startSeq = ''.join(startSeq) #This handy line converts the sequence list to a sequence string
        else:
            startSeq = startSeq[0]
        for num in range(len(startSeq)):
            startNuc = startSeq[num]
            totalBrl, wTime = 0, 0
            stateList, wTimeList = [], []
            while totalBrl <= self.arbBrl:
                stateList.append(startNuc)
                wTimeList.append(wTime)
                wTime = (-1/self.diagonals[startNuc])*math.log(random.random()) #Since diagonals is a dictionary that pairs the starting nucleotide with its diagonal, I can easily access the diagonal. Yay! 
                potentStates3 = list(filter(lambda x:x != startNuc, self.bases)) #include all nucleotides in potentStates except the startNuc
                probs3 = list(filter(lambda x:x != -1, self.transProbs[startNuc]))
                nextNuc = self.discSamp(potentStates3, probs3)
                totalBrl += wTime #updates the total branch length
                startNuc = nextNuc[0] #resets the starting nucleotide to the one select by the discSample method. Does this until while loop broken. Then startNuc set to second site . . .
            finalStateString += stateList[-1]
        return finalStateString
    
    def margProbMat(self, branchlength=100):
        return (expm(numpy.array(self.Qmatrix) * branchlength))
        
            
            
        


d = contMarkov()
#print d.discSamp(nuclist = d.bases, problist = [0.1, 0.7, 0.1, 0.1])
#print d.transProbs
#print d.diagonals
print d.cmSim()


               
        


        
