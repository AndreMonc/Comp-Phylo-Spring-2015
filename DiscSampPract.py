# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 21:45:44 2015

@author: Andre Moncrieff
Written for Computational Phylogenetics, taught by Jeremy Brown
Guidelines from Jeremy marked by """ """
Comments by Andre Moncrieff marked by #
"""

# 1. 
"""   
Write a function that multiplies all consecutively decreasing numbers 
between a maximum and a minimum supplied as arguments. (Like a factorial, 
but not necessarily going all the way to 1). This calculation would look 
like max * max-1 * max-2 * ... * min.
"""

def SeriesMult(min,max): # SeriesMult stands for series multiplier
    product = max
    for integer in range(min,max):
        product = product * integer
    return product

#print(SeriesMult(min,max))     
print(SeriesMult(1,6))   

# 2. 
"""
Using the function you wrote in (1), write a function that calculates the 
binomial coefficient (see Definition 1.4.12 in the probability reading). 
Actually, do this twice. The first time (2a) calculate all factorials fully. 
Now re-write the function and cancel as many terms as possible so you can 
avoid unnecessary multiplication (see the middle expression in Theorem 1.4.13).
"""     
    # 2a. 
def BinomialCoeff(n,k): 
    if k>n:
        return 0
    else:
        BinomialCoeff = SeriesMult(1,n)/(SeriesMult(1,n-k)*SeriesMult(1,k))
    return BinomialCoeff
    
print(BinomialCoeff(5,2))

    # 2b.
def BinomialCoeffFast(n,k): #Binomial Coefficient Fast cancels identical terms 
# in numerator and denominator and therefore bipasses unnecessary multiplication.
    if k>n:
        return 0
    else:
        BinomialCoeffFast = SeriesMult(n-k+1,n)/SeriesMult(1,k)
    return BinomialCoeffFast
print(BinomialCoeffFast(5,2))

# 3.
"""
Try calculating different binomial coefficients using both the functions 
from (2a) and (2b) for different values of n and k. Try some really big values 
there is a noticeable difference in speed between the (2a) and (2b) function. 
Which one is faster? By roughly how much?
"""
"""
# Comparison Number 1
import time
start1 = time.time()
print(BinomialCoeff(50000,3000))
end1 = time.time()
TimeBinomialCoeff = end1 - start1
print("Speed of calculation using BinomialCoeff function (n=50000,k=3000): " + str(TimeBinomialCoeff))
#1.6739 sec
start2 = time.time()
print(BinomialCoeffFast(50000,3000))
end2 = time.time()
TimeBinomialCoeffFast = end2 - start2
print("Speed of calculation using BinomialCoeffFast function (n=50000,k=3000): " + str(TimeBinomialCoeffFast))
#0.0099 sec
# 2b function is ~1.66 seconds faster
"""
"""
# Comparison Number 2
import time
start3 = time.time()
#print(BinomialCoeff(70000,30000))
end3 = time.time()
TimeBinomialCoeff = end3 - start3
#print("Speed of calculation using BinomialCoeff function (n=70000,k=30000): " + str(TimeBinomialCoeff))
#2.6709 sec
start4 = time.time()
#print(BinomialCoeffFast(70000,30000))
end4 = time.time()
TimeBinomialCoeffFast = end4 - start4
#print("Speed of calculation using BinomialCoeffFast function (n=70000,k=30000): " + str(TimeBinomialCoeffFast))
#0.6909 sec
# 2b function is 1.98 seconds faster
"""
# 4.
"""
Use either function (2a) or (2b) to write a function that calculates the 
probability of k successes in n Bernoulli trials with probability p. This is 
called the Binomial(n,p) distribution. See Theorem 3.3.5 for the necessary 
equation. Hint: pow(x,y) returns x^y (x raised to the power of y).
"""
def BernTrial(n,p,k):
    if k<0 or k>n:
        return 0
    else: 
        Binomcoeff = BinomialCoeffFast(n,k)       
        Pofk = Binomcoeff*(pow(p,k))*(pow(1-p,n-k))
    return Pofk
    
print(BernTrial(8,0.5,5))
  
# 5.
'''Now write a function to sample from an arbitrary discrete distribution. 
This function should take two arguments. The first is a list of arbitrarily 
labeled events and the second is a list of probabilities associated with these 
events. Obviously, these two lists should be the same length.'''

from scipy.stats import rv_discrete


def DiscreteSample(xk,pk,numbOfTrial): #Adding size because it allows more flexibility to function
    discrete = rv_discrete(name='discrete', values=(xk,pk)) 
    sample = discrete.rvs(size=numbOfTrial)
    x = []
    x.append(sample)
    return x

numbOfTrial = 2
arbevents = [5,6,7,8,9]
prob = [0.3,0.1,0.2,0.2,0.2]
y=DiscreteSample(arbevents,prob, numbOfTrial)
y = y[0]
print y


'''---> Sampling sites from an alignment <---

Imagine that you have a multiple sequence alignment with two kinds of sites. 
One type of site pattern supports the monophyly of taxon A and taxon B. 
The second type supports the monophyly of taxon A and taxon C.'''


# 6.
'''For an alignment of 400 sites, with 200 sites of type 1 and 200 of type 2, 
sample a new alignment (a new set of site pattern counts) with replacement 
from the original using your function from (5). Print out the counts of the 
two types.'''

"""
Fail below... arghh
def onelistmaker(n):
    listOfOnes = [1]*n
    return listOfOnes

def twolistmaker(n):
    listOfTwos = [2]*n
    return listOfTwos

def problistmaker(n):
    listOfProb = [0.0025]*n
    return listOfProb

numbOfTrial = 400
SitesOrig = onelistmaker(200)+twolistmaker(200)
#print(SitesOrig)
ListOfProb = problistmaker(400)
#print(ListOfProb)
z = DiscreteSample(SitesOrig,ListOfProb,numbOfTrial)
z = z[0]
print z
"""
import numpy
list1 = []
list2 = []

def MultipleSeqAlign(num):
    for x in range (0,num):
        SiteTypes = [1,2]
        Prob = [0.5,0.5]
        siz = 400
        NewAlignment = DiscreteSample(SiteTypes,Prob, siz)
        NewAlignment = NewAlignment[0]
        NewAlignment = numpy.array(NewAlignment).tolist()
        list1.append(NewAlignment.count(1))
        list2.append(NewAlignment.count(2))
    return NewAlignment

NewAlignment = MultipleSeqAlign(1)

print("Number of type 1 sites: " + str(NewAlignment.count(1)))
print("Number of type 2 sites: " + str(NewAlignment.count(2)))

# 7.
'''Repeat (6) 100 times and store the results in a list.'''

#Thank you Oscar for helping here!!!

list1 = []
list2 = []

howMany = input("how many times would you like to run the simulation? ")
NewValue = MultipleSeqAlign(howMany)

print "List of type 1 sites in each repeat: ", list1
print "List of type 2 sites in each repeat: ", list2

"""
failed way below ...
for i in range(100):
    SitesOrig=[1,2]
    ListOfProb=[0.5,0.5]
    numbOfTrial=[400]
    SequenceAlignx100 = DiscreteSample(SitesOrig,ListOfProb,numbOfTrial)
    SequenceAlignx100 = SequenceAlignx100[0]
    #print SequenceAlignx100
    SequenceAlignx100 = numpy.array(SequenceAlignx100).tolist()
    #print SequenceAlignx100
counting1 = SequenceAlignx100.count(1)
counting2 = SequenceAlignx100.count(2)
        
print("List of sites in output when DiscreteSample function is run 100x: " + str(SequenceAlignx100))
print("Number of type 1 sites when DiscreteSample function is run 100x: " + str(counting1))
print("Number of type 2 sites when DiscreteSample function is run 100x: " + str(counting2))
"""

# 8.
'''Of those 100 trials, summarize how often you saw particular proportions 
of type 1 vs. type 2.'''

import matplotlib.pyplot as plt
print("Histogram of type 1 distribution for 100 repeats") 
plt.hist(list1)
print("Histogram of type 2 distribution for 100 repeats") 
plt.hist(list2)

#now to find proportion
proportions = []
for i in range(0,100):
    if list1[i] > list2[i]:
        x = float(list2[i] / list1[i])
        proportions.append(x)
    else: 
        x = float(list1[i] / list2[i])
        proportions.append(x)

plt.hist(proportions)
plt.xlabel("proportions type 1 and type 2 sites")
plt.ylabel("frequency")
#weird histogram output! One outlier?
 
# 9.
'''Calculate the probabilities of the proportions you saw in (8) using the 
binomial probability mass function (PMF) from (4).'''
BernoulliProb = []

###Could not complete this problem.

for val in proportions:
    n=400
    p=0.5
    k=val
    BernoulliList.append(BernTrial(n,p,k))
    
print BernoulliList
    

# 10.
'''Compare your results from (8) and (9).'''

# 11.
'''Repeat 7-10, but use 10,000 trials.'''

    
    
