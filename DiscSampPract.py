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

#Defining new function. The two-part argument is inclusive for min
#but exclusive for max. I therefore make the product variable to equal max.
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
# Just using a simple if/else designation so that the code knows how to hand 
# different values of k.    
    if k>n:
        return 0
    else:
        BinomialCoeff = SeriesMult(1,n)/(SeriesMult(1,n-k)*SeriesMult(1,k))
    return BinomialCoeff
    
print(BinomialCoeff(5,2))

    # 2b.
def BinomialCoeffFast(n,k): #Binomial Coefficient Fast cancels identical terms 
# in numerator and denominator and therefore bipasses unnecessary multiplication.
# As shown in the next step, this function is noticeably faster in its calculations.
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

# Comparison Number 1
# Not to self: When timing events, import time
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


# Comparison Number 2
import time
start3 = time.time()
print(BinomialCoeff(70000,30000))
end3 = time.time()
TimeBinomialCoeff = end3 - start3
print("Speed of calculation using BinomialCoeff function (n=70000,k=30000): " + str(TimeBinomialCoeff))
#2.6709 sec
start4 = time.time()
print(BinomialCoeffFast(70000,30000))
end4 = time.time()
TimeBinomialCoeffFast = end4 - start4
print("Speed of calculation using BinomialCoeffFast function (n=70000,k=30000): " + str(TimeBinomialCoeffFast))
#0.6909 sec
# 2b function is 1.98 seconds faster

# 4.
"""
Use either function (2a) or (2b) to write a function that calculates the 
probability of k successes in n Bernoulli trials with probability p. This is 
called the Binomial(n,p) distribution. See Theorem 3.3.5 for the necessary 
equation. Hint: pow(x,y) returns x^y (x raised to the power of y).
"""
#So, perhaps I should have named this function BinomialDistribution or 
# binomialPMF?
def BernTrial(n,p,k):
    if k<0 or k>n:
        return 0
    else: 
        Binomcoeff = BinomialCoeffFast(n,k)       
        #Pofk refers to the probability of k success in n Bernoulli trials
        Pofk = Binomcoeff*(pow(p,k))*(pow(1-p,n-k))
    return Pofk
    
print(BernTrial(8,0.5,5))
  
# 5.
'''Now write a function to sample from an arbitrary discrete distribution. 
This function should take two arguments. The first is a list of arbitrarily 
labeled events and the second is a list of probabilities associated with these 
events. Obviously, these two lists should be the same length.'''

#Based on finding by Glaucia, the rv_discrete variable seemed appropriate for 
#necessary calculation.
from scipy.stats import rv_discrete


def DiscreteSample(xk,pk,numbOfTrial): #Adding size because it allows more flexibility to function
    #Line below apparently necessary in order for rv_discrete to work?    
    discrete = rv_discrete(name='discrete', values=(xk,pk)) 
    sample = discrete.rvs(size=numbOfTrial)
    x = []
    x.append(sample)
    return x

numbOfTrial = 2
arbevents = [5,6,7,8,9]
prob = [0.3,0.1,0.2,0.2,0.2]
y=DiscreteSample(arbevents,prob, numbOfTrial)
#So, I add the line below, because it takes y array and extracts the first 
#indexed list from that array (y[0]). I found that it was much easier to work with
#a list than an array. For instance, I was unable to use the count method on an 
#array, but was able to use it with a list.
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
# Next attempt here seems to work--heavily based on Oscar's code. numpy and 
#tolist were useful in converting my array "NewAlignment" into a list. I could 
#then count 1s and 2s in the lists.
import numpy
#Setting up two blank lists, and later I append lists into these lists. 
list1 = []
list2 = []

#the num argument allows me to run the function as many times as I want. 
#This is very useful later on.
def MultipleSeqAlign(num):
    for x in range (0,num):
        SiteTypes = [1,2]
        Prob = [0.5,0.5]
        siz = 400
        #the DiscreteSample function outputs an array which is hard to work with
        #I could not figure out how to count 1s and 2s otherwise.        
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

#Here I tell the MultipleSeqAlign function to repeat the calculation in 
#(6) 100 times.
MultipleSeqAlign(100)

print "List of number of type 1 sites in each of 100 repeats: ", list1
print "List of number of type 2 sites in each of 100 repeats: ", list2

"""
failed code below ...
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
#So here I show histograms of the distributions of the number of 1s and 2s 
#counted in each of the 100 repeats (in separate histograms). This is not a
#direct measure of the proportions though . . . It looks as if the proportions
#however calculated should be very close to one.

import matplotlib.pyplot as plt
print("Histogram of type 1 distribution for 100 repeats") 
plt.hist(list1)
print("Histogram of type 2 distribution for 100 repeats") 
plt.hist(list2)

#Below is a crack at measuring the proportion directly, but the 
#output seemed really odd.
'''
#now to find proportion
proportions = []
for i in range(0,len(list1)):
    if list1[i] > list2[i]:
        x = float(list2[i] / list1[i])
        proportions.append(x)
    else: 
        x = float(list1[i] / list2[i])
        proportions.append(x)

plt.hist(proportions)
plt.xlabel("proportion of two sites")
plt.ylabel("frequency")
#weird histogram output! One outlier?
'''

# 9.
'''Calculate the probabilities of the proportions you saw in (8) using the 
binomial probability mass function (PMF) from (4) (which calculates the 
probability of k successes in n Bernoulli trials with probability p).'''

#A handy storage location for the output of a forloop is an empty list.
#This is something important I've learned from this assignment.
BernoulliProb = []

#The values in list1 are all the counts of the type one sites
# or "successes." So I'm applying the BernTrial Probability Mass Function on 
# each of the 100 type one sites or "success" values and storing the result in
#list BernoulliProb.
for val in list1:
    n=400
    p=0.5
    k=val
    BernoulliProb.append(BernTrial(n,p,k))
    
print BernoulliProb
  

# 10.
'''Compare your results from (8) and (9).'''
plt.hist(BernoulliProb)
plt.xlabel("K success (type 1 site)")
plt.ylabel("Probability Mass Function")


# 11.
'''Repeat 7-10, but use 10,000 trials.'''

list1 = []
list2 = []
MultipleSeqAlign(10000)
print "List of type 1 sites in each of 10000 repeats: ", list1
print "List of type 2 sites in each of 10000 repeats: ", list2

import matplotlib.pyplot as plt
print("Histogram of type 1 distribution for 10000 repeats") 
plt.hist(list1)
print("Histogram of type 2 distribution for 10000 repeats") 
plt.hist(list2)
BernoulliProb = []

for val in list1:
    n=400
    p=0.5
    k=val
    BernoulliProb.append(BernTrial(n,p,k))
    
print BernoulliProb
