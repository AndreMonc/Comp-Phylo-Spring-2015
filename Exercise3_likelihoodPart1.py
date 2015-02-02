from __future__ import division
from scipy.stats import binom
import scipy
import matplotlib.pyplot as plt

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 11:36:12 2015


@author: Andre
"""

"""
An Introduction to Likelihood
@author: jembrown
"""
#Random draws. Provided by Jeremy--handy for drawing random outcomes.
n = 5
p = 0.5 # Change this and repeat

data = binom.rvs(5,0.01)
print data


#Arbitrarily defined dark marbles as successes (k) and light marbles as failures. 

#The number of successes is 4. So, n=5 (number of trials), k=4, p=unknown. I used 
#these new data to find an interval that hopefully contains the true value of p.

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

data = 4  #This 4 refers to the number of successes (dark marbles drawn)
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

#I cut and pasted my functions from the previous assignment below:

#The two-part argument is inclusive for min but exclusive for max. I therefore 
#make the product variable to equal max.
def SeriesMult(min,max): # SeriesMult stands for series multiplier. 
    product = max
    for integer in range(min,max,1):
        product = product * integer
    return product

#Binomial Coefficient Fast cancels identical terms in numerator and 
#denominator and therefore bipasses unnecessary multiplication.
def BinomialCoeffFast(n,k): #Calculates the binomial coefficient (or n choose k)
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
      
binomialPMF(3,0.5,2) #Just double-checking that the function works by using the 2 heads in three flips example (I know output should be 0.375)
#output is 0.375, so binomialPMF appears to work.


"""
Now we need to calculate likelihoods for a series of different values for p to 
compare likelihoods. There are an infinite number of possible values for p, so 
let's confine ourselves to steps of 0.05 between 0 and 1.
"""

# Here I set up a list with all relevant values of p
#pValues holds a list that includes potential p values in increments of 0.05 in the range 0 to 1
#It took me forever to realize that using a 0.5 as the step argument in the range function caused problems.
#0.5 is a float . . .
#Much easier to use integers as arguments in the range function and divide by 100!
pValues = [x/100 for x in range(0,101,5)]  
print pValues

# Here I first create an empty list to hold likelihood values associated with the p values
# Using a for loop I calculate likelihoods for each output of the binomialPMF function (p values varying)
# In the loop I append the outputs into my likelihood list
likelihood = []

for prob in pValues:
    singleLikelihood = binomialPMF(k=4,n=5,p=prob)
    likelihood.append(singleLikelihood)

print likelihood

# I thind find the maximum likelihood value of p (from the arbitrary set of ps I chose)
maxlikeli = max(likelihood) #The output here was not as precise as when I printed likelihood values above . . .
# However, I was able to manually figure out which p value corresponded to the maximum likelihood.
# Below, I tried to use a dictionary to match likelihood values with p values, but I couldn't figure out how to automate
# The selection of a likelihood key (partly because of the max(likelihood) rounding problem mentioned above)
#dict = dict(zip(likelihood,pValues))
#dict = dict(zip(likelihood,pValues))#pair likelihood values with p values
print maxlikeli
#print dict #Easier to spot corresponding p value
#print("Maximum likelihood value of p is: " + str(dict[0.4096]))

#It was really helpful to visualize what was going on. The figure helped me double-check that my results made sense.
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

#Here I simply created an empty list to hold the likelihood ratios
#Then I use a for loop to divide all likehood values by the maximum likelihood value.
#Thus, lower likelihood ratios signify a less likely/relevant likelihood value in the numerator.
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
