from __future__ import division
from scipy.stats import binom
import scipy
import matplotlib.pyplot as plt
from numpy import percentile

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 11:36:12 2015

@author: Andre--with help at various points from Glaucia. Directions 
from Jeremy interspersed with my own comments and code.
"""

'''
binom.rvs function below provided by Jeremy--handy for drawing random outcomes
from a binomial distribution. The arguments in the function below are (n,p).
n refers to the number of trials (say, coin flips). p refers to the probability 
of a "success" (say, heads). Thus, if n=100 and p=0.5, one would expect to have 
around 50 heads or successes if flipping a fair coin. I messed around with the
function, inputting various numbers, and it worked well.
'''

data = binom.rvs(100,0.5)
print data

'''
The class arbitrarily defined dark marbles as successes (k) and light marbles 
as failures. Jeremy provided this data for below calculations: the number of 
successes is 4. So, n=5 (number of trials), k=4, p=unknown. I use these new 
data to find an interval that hopefully contains the true value of p.
'''

data = 4  #This 4 refers to the number of successes (dark marbles drawn)
numTrials = 5 #Number of draws (or could be coin flips in another scenario)


"""
Jeremy: Since we are trying to learn about p, we define the likelihood function as;
L(p;data) = P(data|p). If data is a binomially distributed random variable 
[data ~ Binom(5,p)] P(data=k|p) = (5 choose k) * p^k * (1-p)^(n-k).
So, we need a function to calculate the binomial PMF. Luckily, you should have 
just written one and posted it to GitHub for your last exercise. Copy and paste 
your binomial PMF code below. For now, I will refer to this function as 
binomPMF(). 
"""

#I cut and pasted my functions from the previous assignment below:

#The two-part argument of SeriesMult is inclusive for min but exclusive for max. 
#I therefore make the product variable to equal max.
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
      
test = binomialPMF(7,0.5,5)
print test

test = binomialPMF(3,0.6666,2)
print test


 #Just double-checking that the function works by using 
#the 2 heads in three flips example (I know output should be 0.375)
#output is 0.375, so binomialPMF appears to work.


"""
Jeremy: Now we need to calculate likelihoods for a series of different values for p to 
compare likelihoods. There are an infinite number of possible values for p, so 
let's confine ourselves to steps of 0.05 between 0 and 1.
"""
'''
Here I set up a list with all relevant values of p. The pValues variable holds 
a list that includes potential p values in increments of 0.05 in the range 0 
to 1. It took me forever to realize that using a 0.5 as the step argument in 
the range function caused problems. 0.5 is a float . . . Much easier to use 
integers as arguments in the range function and divide by 100!
'''
pValues = [x/100 for x in range(0,101,5)]  
print pValues

numPval = len(pValues)
print numPval

'''
Below I first create an empty list to hold likelihood values associated with 
the p values I generated above. Using a "for loop" I calculate likelihoods for 
each output of the binomialPMF function (p values varying). In the loop I 
append the outputs into my likelihood list.
'''
likelihood = []

for prob in pValues:
    singleLikelihood = binomialPMF(k=4,n=5,p=prob)
    likelihood.append(singleLikelihood)

#print likelihood

'''
Now I want to find the maximum likelihood value of p (from the arbitrary set 
of p I chose):
'''
maxlikeli = max(likelihood)
#print maxlikeli

'''
#The maxlikelihood value printed above was not as precise as the likelihood 
values stored in the list "likelihood." The "max" function appears to round 
the value. This caused difficulties for me in trying to automate the matching 
of the maximum likelihood value with its corresponding p value. However, I was 
able to manually figure out which p value corresponded to the maximum 
likelihood. Below, I tried to use a dictionary to match likelihood values with
p values, but I couldn't figure out how to automate the process. The selection 
of a likelihood key was tricky (partly because of the max(likelihood) 
rounding problem mentioned above).
'''

#dict = dict(zip(likelihood,pValues))
#dict = dict(zip(likelihood,pValues))#pair likelihood values with p values

#print dict #Easier to spot corresponding p value
print("Maximum likelihood value of p is: " + str(0.8))
#MLV is 0.4096 and MLVofP is 0.8

'''
It was really helpful to visualize what was going on. The figure helped me 
double-check that my results made sense.
plt.figure()
plt.plot(pValues,likelihood)
plt.xlabel("Probability")
plt.ylabel("Likelihood")
plt.title("Maximum Likelihood Estimation")
plt.show()
'''

'''
Jeremy: What is the strength of evidence against the most extreme values of 
p (0 and 1)? My answer: The evidence is very strong because the p values of 
0 and 1 have corresponding likelihood values of 0. 

Jeremy: Calculate the likelihood ratios comparing each value 
(in the numerator) to the max value (in the denominator)

Below I simply created an empty list to hold the likelihood ratios. Then I used 
a "for loop" to divide all likehood values by the maximum likelihood value.
Thus, lower likelihood ratios signify a less likely/relevant likelihood value 
in the numerator.
'''

likeliRatios = []
for x in likelihood:
    ratio=x/0.4096
    likeliRatios.append(ratio)
    
print likeliRatios

"""
Jeremy: Now let's try this all again, but with more data. This time, we'll 
use 20 draws from our cup of marbles.
"""

data = 12   #number of successes = k.
numTrials = 20 #number of trials = n.

'''
Jeremy: Calculate the likelihood scores for values of p, in light of the 
data you've collected.

Below I simply generate a list of p values ranging from 0 to 1 in 
increments of 0.05.
'''

pValues2 = [x/100 for x in range(0,101,5)]
print pValues2

likelihood2 = [] #This is a list to store the likelihood values for each of 
#the p values I generated above.

for prob in pValues:
    singleLikelihood2 = binomialPMF(k=12,n=20,p=prob)
    likelihood2.append(singleLikelihood2)

print likelihood2

#Jeremy: Find the maximum likelihood value of p (at least, the max in this set)

maxlikeli2 = max(likelihood2)
print maxlikeli2

'''
The maximum likelihood value is 0.1797... and it is associated with a 
p value of 0.6.

Never quite got this to work:
dict2 = dict(zip(likelihood2,pValues2))
print dict2 #Easier to spot corresponding p value
print("Maximum likelihood value of p is: " + str(dict[]))
'''
plt.figure()
plt.plot(pValues2,likelihood2)
plt.xlabel("Probability")
plt.ylabel("Likelihood")
plt.title("Maximum Likelihood Estimation")
#plt.show()

'''
Jeremy: What is the strength of evidence against the most extreme values of p 
(0 and 1)?

My answer: The evidence is very strong because the p values of 0 and 1 have 
corresponding likelihood values of 0. 
'''

'''
# Jeremy: Calculate the likelihood ratios comparing each value (in the 
numerator) to the max value (in the denominator)
'''
likeliRatios2 = []
for x in likelihood2:
    ratio2 = x/0.17970578775468937
    likeliRatios2.append(ratio2)
    
print likeliRatios2

'''
Jeremy: When is the ratio small enough to reject some values of p?
My answer: Is it when the ratio falls in the lower 5% of the distribution
of likelihood ratio values (with the maximum likelihood ratio (1) at the 
opposite end of the the distribution)? 
Note: You will empirically investigate this on your own later in this exercise.
'''


# **** EVERYTHING ABOVE HERE TO BE POSTED TO GITHUB BY TUESDAY, FEB. 3RD. ****
# **** CODE BELOW TO BE POSTED TO GITHUB BY THURSDAY, FEB. 5TH ****


"""
Jeremy: Sometimes it will not be feasible or efficient to calculate the 
likelihoods for every value of a parameter in which we're interested. Also, 
that approach can lead to large gaps between relevant values of the parameter. 
Instead, we'd like to have a 'hill climbing' function that starts with some 
arbitrary value of the parameter and finds values with progressively better 
likelihood scores. This is an ML optimization function. There has been a lot 
of work on the best way to do this. We're going to try a fairly simple approach
that should still work pretty well, as long as our likelihood surface is 
unimodal (has just one peak). Our algorithm will be: (1) Calculate the 
likelihood for our starting parameter value (we'll call this pCurr) (2) 
Calculate likelihoods for the two parameter values above (pUp) and below 
(pDown) our current value by some amount (diff). So, pUp=pCurr+diff and 
pDown=pCurr-diff. To start, set diff=0.1, although it would be nice to allow 
this initial value to be set as an argument of our optimization function.
(3) If either pUp or pDown has a better likelihood than pCurr, change pCurr 
to this value. Then repeat (1)-(3) until pCurr has a higher likelihood than 
both pUp and pDown. (4) Once L(pCurr) > L(pUp) and L(pCurr) > L(pDown), reduce
diff by 1/2. Then repeat (1)-(3). (5) Repeat (1)-(4) until diff is less than 
some threshold (say, 0.001). (6) Return the final optimized parameter value.
Write a function that takes some starting p value and observed data (k,n) for 
a binomial as its arguments and returns the ML value for p. To write this 
function, you will probably want to use while loops. The structure of
these loops is while (someCondition):
    code line 1 inside loop
    code line 2 inside loop
As long as the condition remains True, the loop will continue executing. If the
condition isn't met (someCondition=False) when the loop is first encountered, 
the code inside will never execute. If you understand recursion, you can use it 
to save some lines in this code, but it's not necessary to create a working 
function.
"""

'''
I worked quite a bit with Glaucia to understand and write the code below. 
Thanks Glaucia!! In class we realized that this function would be quite a 
bit faster if we could first run it with a large diff and then automate the
switch to a smaller diff once the function was nearer to finding the max
likelihood of p.

Jeremy: Write a function that finds the ML value of p for a binomial, given 
k and n. #So this function "searches" for the p value with the maximum 
likelihood.
'''

def MaxLikValofP(n,k,pCurr,diff): 
    while diff > 0.0001:
        pUp=pCurr+diff
        pDown=pCurr-diff    
        Lik_pCurr = binomialPMF(n,pCurr,k)
        Lik_pUp = binomialPMF(n,pUp,k)
        Lik_pDown = binomialPMF(n,pDown,k)             
        while Lik_pCurr < Lik_pUp or Lik_pCurr < Lik_pDown:
            if Lik_pUp > Lik_pCurr:         
                pCurr = pUp #value by step diff each time the "if" statement is met                
            elif Lik_pDown > Lik_pCurr: #this "while" section decreases each
                pCurr = pDown #value by step diff each time the "if" statement is met
            pUp=pCurr+diff
            pDown=pCurr-diff    
            Lik_pCurr = binomialPMF(n,pCurr,k)
            Lik_pUp = binomialPMF(n,pUp,k)
            Lik_pDown = binomialPMF(n,pDown,k)  
        #Here I want to hone the value so I reduce diff by half            
        diff *= 0.5
    return pCurr #I want to get back the p value

maxLikValP = MaxLikValofP(3,2,0.5,0.4) #This seems to return the right value
print maxLikValP


"""
In the exercise above, you tried to find an intuitive cutoff for likelihood ratio
scores that would give you a reasonable interval in which to find the true value of 
p. Now, we will empirically determine one way to construct such an interval. To do 
so, we will ask how far away from the true value of a parameter the ML estimate 
might stray. Use this procedure: (1) start with a known value for p, (2) simulate
a bunch of datasets, (3) find ML parameter estimates for each simulation, and then 
(4) calculate the likelihood ratios comparing the true parameter values and the ML
estimates. When you do this, you will be constructing a null distribution of
likelihood ratios that might be expected if the value of p you picked in (1)
was true. Note that the ML values for these replicates are very often greater than
L(true value of P), because the ML value can only ever be >= L(true value). Once 
you have this distribution, find the likelihood ratio cutoff you need to ensure 
that the probability of seeing a LR score that big or greater is <= 5%. 
"""

# Set a starting, true value for p

#trueP = 0.7

# Simulate 1,000 datasets of 200 trials from a binomial with this p
# If you haven't already done so, you'll want to import the binom class from scipy:
#from scipy.stats import binom
#binom.rvs(n,p) # produce a draw from the corresponding binomial.

import matplotlib.pyplot as plt
from scipy.stats import rv_discrete

'''
The function below is one that I used in the first exercise. It draws random 
numbers from a discrete binomial distribution.
'''
def randomDraw(xk,pk,numTrials): 
    discrete = rv_discrete(name='discrete', values=(xk, pk))
    simulation1 = discrete.rvs(size=numTrials)
    listResult = list(simulation1)
    return listResult
    
'''
The range in the "for loop" below includes 0 through 999 (thereby generating 
1000 simulations). I've set up the simulations such that there are two possible
outcomes or outputs (0 or 1). The convention I follow is that an output of "1" 
means a success. The probability of a success in any given trial is is 0.7. One
simulation essentially involves flipping a coin weighted in favor of heads
200 times and counting the number of heads. I store this number in a list
(simulation1000) and then repeat 999 more times.
'''
simulation1000=[]
for i in range(1000): 
    dataset1 = randomDraw(xk=[0,1],pk=[0.3,0.7],numTrials=200)
    numSuccess1 = dataset1.count(1)
    simulation1000.append(numSuccess1)
#print simulation1000    

    
'''
Jeremy: Now find ML parameter estimates for each of these trials

Below I find the p value that corresponds to the maximum likelihood value
for each of the 1000 simulations I ran above.
'''

MLvalueP = [] 
for succ in simulation1000:
    MLvalofP1 = MaxLikValofP(n=200,pCurr=0.01,k=succ,diff=0.001) 
    MLvalueP.append(MLvalofP1)
#print MLvalueP

'''
Jeremy: Calculate likelihood ratios comparing L(trueP) in the numerator to the 
maximum likelihood (ML) in the denominator. Sort the results and find the 
value corresponding to the 95th percentile.
'''

LtrueP = []
for ksucc in simulation1000:
    LwithTrueP = binomialPMF(n=200,k=ksucc,p=0.7)
    LtrueP.append(LwithTrueP)
#print(LtrueP)

'''
With the function defined below I can get maximum likelihood values (note 
that output is Lik_Curr rather than pCurr, as in the similar function above)
'''

def MaxLikVal(n,pCurr,k,diff): 
    while diff > 0.0001:
        pUp=pCurr+diff
        pDown=pCurr-diff    
        Lik_pCurr = binomialPMF(n,pCurr,k)
        Lik_pUp = binomialPMF(n,pUp,k)
        Lik_pDown = binomialPMF(n,pDown,k)             
        while Lik_pCurr < Lik_pUp or Lik_pCurr < Lik_pDown:
            if Lik_pUp > Lik_pCurr:         
                pCurr = pUp #value by step diff each time the "if" statement is met                
            elif Lik_pDown > Lik_pCurr: #this "while" section decreases each
                pCurr = pDown #value by step diff each time the "if" statement is met
            pUp=pCurr+diff
            pDown=pCurr-diff    
            Lik_pCurr = binomialPMF(n,pCurr,k)
            Lik_pUp = binomialPMF(n,pUp,k)
            Lik_pDown = binomialPMF(n,pDown,k)  
        #Here I want to hone the value so I reduce diff by half            
        diff *= 0.5
    return Lik_pCurr 

MaxLikValue = MaxLikVal(n=3,pCurr=0.6,k=2,diff=0.01)
print MaxLikValue

#Using the function defined above to find ML values
MLV = []
for ksucc in simulation1000:
    maxLV = MaxLikVal(n=200,pCurr=0.01,k=ksucc,diff=0.01)
    MLV.append(maxLV)
#print MLV

LikeRatios = [float(ltp)/float(mlv) for ltp,mlv in zip(LtrueP,MLV)]
#print LikeRatios

#Here I calculate the 95th percentile of my likelihood ratios
print percentile(LikeRatios,95)
   
#Now, I convert the likelihood ratios (LRs) to -2ln(LRs) values.
from math import log
natlogval = []
for LR in LikeRatios:
    logval = (-2)*(log(LR))
    natlogval.append(logval)
#print natlogval

'''
Jeremy: Find the 95th percentile of these values. Compare these values to this table:
https://people.richland.edu/james/lecture/m170/tbl-chi.html. In particular, look
at the 0.05 column. 
Do any of these values seem similar to the one you calculated?
'''

print percentile(natlogval,95)

list1 = [1,2,3,4,5,6,7,8,9,10]
#print percentile(list1, 5)

'''
I get 3.58, which is not too far from 3.841 in the 1 df row and 0.05 column.
Taking the 95th percentile allows one to identify the point at which all 
higher values will have a <5% chance of occuring.

Jeremy: Any idea why that particular cell would be meaningful? 

It represents the alpha level for the chi-square test (the measure of when
a chi-square test is significant or not at the 0.05 level). Since binomial
trials have 1 degree of freedom, this cell indicates the 0.05 alpha level for 
a binomial as well. I think . . .

Jeremy: Based on your results (and the values in the table), what LR statistic 
value [-2ln(LR)] indicates that a null value of p is far enough away from the 
ML value that an LR of that size is <=5% probable if that value of p was true?

I think any natural log likelihood ratio value greater than 3.58. It is 
important to note that there is an inverse relationship between the -2ln(LR)
and the LR. This is why it makes sense to remove the top 5% of the values. 
(They are the furthest values from the maximum likelihood, if I am interpreting
the analysis correctly).

# Using this cutoff, what interval might you report for the 5- and 20-trial data
# sets above?
'''

#5 trial data set


print likeliRatios
print likeliRatios2
test1 = []

for rat in likeliRatios:
    if rat == 0.0:
        print "Value discarded, because it produces an undefined LR."
    else: 
        conv = (-2)*(log(rat))
        test1.append(conv)
print test1
length1 = len(test1)
print length1



#Looking over the ratio outputs I think I can eliminate ~ p = 0 through p = 0.35. 
#Also, I can eliminate p = 1. So, CI of 0.4 to 0.95. (I am eliminating LR
# >3.85 and = 0.)
      
test2 = [] 
#20 trials 
for ratio in likeliRatios2:
    if ratio == 0.0:
        print "Value discarded, because it produces an undefined LR."
    else: 
        conversion = (-2)*(log(ratio))
        test2.append(conversion)
print test2
length2 = len(test2)
print length2


#Looking over the ratio outputs I think I can eliminate ~ p = 0 through p = 0.35. 
#Also, I can eliminate p = 0.8 through 1.0. So, CI of 0.4 to 0.75. (I am eliminating 
#LR >3.85 and = 0.)



# We've talked in previous classes about two ways to interpret probabilities. Which
# interpretation are we using here to define these intervals?
#Frequentist approach! Collecting masses of data and deriving results thereof.
