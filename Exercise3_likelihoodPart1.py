from __future__ import division
from scipy.stats import binom
import scipy
import matplotlib.pyplot as plt

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 11:36:12 2015

@author: Andre
"""


n = 5
p = 0.5 # Change this and repeat

data = binom.rvs(5,0.01)
print data

#We'll arbitrarily define dark marbles as successes and light marbles as failures. 

#The number of successes is 4. So, n=5, k=4, p=unknown. Use these new data 
#to find an interval that you think contains the true value of p.

"""
Record the outcomes here:
Draw 1: 1
Draw 2: 1
Draw 3: 1
Draw 4: 1
Draw 5: 0
Number of 'successes': 4
Now record the observed number of succeses as in the data variable below.
"""

data = 4  # Supply observed number of successes here.
numTrials = 5


"""
Since we are trying to learn about p, we define the likelihood function as;
L(p;data) = P(data|p)
If data is a binomially distributed random variable [data ~ Binom(5,p)]
P(data=k|p) = (5 choose k) * p^k * (1-p)^(n-k)
So, we need a function to calculate the binomial PMF. Luckily, you should have 
just written one and posted it to GitHub for your last exercise. Copy and paste 
your binomial PMF code below. For now, I will refer to this function as 
binomPMF(). 
"""

#I cut and pasted my functions from previous assignment below:

#The two-part argument is inclusive for min but exclusive for max. I therefore 
#make the product variable to equal max.
def SeriesMult(min,max): # SeriesMult stands for series multiplier
    product = max
    for integer in range(min,max,1):
        product = product * integer
    return product

#Binomial Coefficient Fast cancels identical terms in numerator and 
#denominator and therefore bipasses unnecessary multiplication
def BinomialCoeffFast(n,k): 
    if k>n:                 
        return 0
    else:
        BinomialCoeffFast = SeriesMult(n-k+1,n)/SeriesMult(1,k)
    return BinomialCoeffFast
    
def binomialPMF(n,p,k):
    if k<0 or k>n:
        return 0
    else: 
        Binomcoeff = BinomialCoeffFast(n,k)       
        #Pofk refers to the probability of k success in n Bernoulli trials
        Pofksuccesses = Binomcoeff*(pow(p,k))*(pow(1-p,n-k))
    return Pofksuccesses
      
binomialPMF(3,0.5,2) #just to double-check that function works. 
#output 0.375, so it does work.


"""
Now we need to calculate likelihoods for a series of different values for p to 
compare likelihoods. There are an infinite number of possible values for p, so 
let's confine ourselves to steps of 0.05 between 0 and 1.
"""

# Set up a list with all relevant values of p
#pValues is a list that includes potential p values in increments of 0.05 in range 0 to 1
pValues = [x/100 for x in range(0,101,5)]  
print pValues

# Calculate the likelihood scores for these values of p, in light of the data you've collected
likelihood = []

for prob in pValues:
    singleLikelihood = binomialPMF(k=4,n=5,p=prob)
    likelihood.append(singleLikelihood)

print likelihood

# Find the maximum likelihood value of p (at least, the max in this set)
#dict = dict(zip(likelihood,pValues))
maxlikeli = max(likelihood)
dict = dict(zip(likelihood,pValues))#pair likelihood values with p values
print maxlikeli
print dict #Easier to spot corresponding p value
print("Maximum likelihood value of p is: " + str(dict[0.4096]))

plt.figure()
plt.plot(pValues,likelihood)
plt.xlabel("Probability")
plt.ylabel("Likelihood")
plt.title("Maximum Likelihood Estimation")
plt.show()

'''
# What is the strength of evidence against the most extreme values of p (0 and 1)?
My answer: The evidence is very strong because the values of p values of 0 and 1 have
corresponding likelihood values of 0. 
'''

# Calculate the likelihood ratios comparing each value (in the numerator) to the max value (in the denominator)

likeliRatios = []
for x in likelihood:
    ratio=x/0.4096
    likeliRatios.append(ratio)
    
print likeliRatios

"""
Now let's try this all again, but with more data. This time, we'll use 20 draws from our cup of marbles.
"""

data = 12   # Supply observed number of successes here.
numTrials = 20


# Calculate the likelihood scores for values of p, in light of the data you've collected
pValues2 = [x/100 for x in range(0,101,5)]  
print pValues2

likelihood2 = []

for prob in pValues:
    singleLikelihood2 = binomialPMF(k=12,n=20,p=prob)
    likelihood2.append(singleLikelihood2)

print likelihood2

# Find the maximum likelihood value of p (at least, the max in this set)
maxlikeli2 = max(likelihood2)
print maxlikeli2
#The maximum likelihood value is 0.1797... is associated with a p value of 0.6
#dict2 = dict(zip(likelihood2,pValues2))
#print dict2 #Easier to spot corresponding p value
#print("Maximum likelihood value of p is: " + str(dict[]))

plt.figure()
plt.plot(pValues2,likelihood2)
plt.xlabel("Probability")
plt.ylabel("Likelihood")
plt.title("Maximum Likelihood Estimation")
plt.show()

# What is the strength of evidence against the most extreme values of p (0 and 1)?
#My answer: The evidence is very strong because the values of p values of 0 and 1 have
#corresponding likelihood values of 0. 

# Calculate the likelihood ratios comparing each value (in the numerator) to the max value (in the denominator)

likeliRatios2 = []
for x in likelihood2:
    ratio2 = x/0.17970578775468937
    likeliRatios2.append(ratio2)
    
print likeliRatios2

# When is the ratio small enough to reject some values of p?
#Is it <0.05? Or am I conflating this number with alpha values?
# Note: You will empirically investigate this on your own later in this exercise.
