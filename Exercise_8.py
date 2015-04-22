"""
Exercise 8 - Introduction to Markov chain Monte Carlo (MCMC)
@author: jembrown
In this example, we will set up a basic MCMC sampler to estimate the probability of success (p) for a binomial distribution.
"""

testPrior = False

from scipy.stats import binom
from scipy.stats import uniform
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

# Define data set
n = 200
p_true = 0.5                # True value to be estimated later
data = binom.rvs(n,p_true)  # Drawing a 'data set'

# Define parameter to be estimated and starting value
p = 0.1     # Starting far away from true value to demonstrate burn-in

# Define prior on parameters of interest
def prior(p_in):
    """
    A function to return the prior density for a given value of p.
    """
    return uniform.pdf(p_in,0,1)

# Define likelihood
def likelihood(p_in):
    """
    A function to return the likelihood for a given value of p.
    """
    if (testPrior):     # Allows us to test the prior, by ignoring the data
        return 1
    elif (not testPrior):   # Returns a likelihood score for actual data
        if (p_in >= 0 and p_in <= 1):
            return binom.pmf(data,n,p_in)
        else:
            return 0    # Returns value of 0 (rather than non) if p outside bounds.
    
# Define proposal distribution
def drawP(p_in):
    """
    This function provides proposed values for p, given a current value.
    """
    newP = uniform.rvs(loc=p_in-0.25,scale=0.5) # min = loc, max = loc+scale
    return newP
    
# Set chain length and run it
ngens = 10000          # Total length of chain
sampleFreq = 1      # Change this to something >1 if you want to space out samples.
updateFreq = 10000   # Frequency of screen updates to make sure chain is running.
samples = []        # Vector to hold sampled values

for gen in range(ngens):
    p_prop = drawP(p)
    p_prop_post = prior(p_prop)*likelihood(p_prop)
    p_post = prior(p)*likelihood(p)
    if (p_prop_post >= p_post): # If proposed value has posterior density > curr value
        p = p_prop
    elif (p_prop_post < p_post): # If proposed value has posterior density < curr value
        r = p_prop_post/p_post
        ranUnifDraw = uniform.rvs()
        if (ranUnifDraw <= r):
            p = p_prop
    else:
        print "Problem calculating proposal ratio!"
        print (p_prop,p_prop_post)
        print (p,p_post)
        print ""
    if (gen % sampleFreq == 0):
        samples.append(p)
    if (gen % updateFreq == 0):
        print "Generation %s" % gen

# Summarizing MCMC samples

# Numerical summaries
burnin = int((ngens/sampleFreq)*0.1)
postBurnSamples = samples[burnin+1:]
print("Posterior Mean: %f" % np.mean(postBurnSamples))
postBurnSamples.sort()  # post-burnin samples will be sorted after this is called
print("Posterior 95% credibility interval: "+"(%f,%f)" % (postBurnSamples[int(len(postBurnSamples)*0.025)],postBurnSamples[int(len(postBurnSamples)*0.975)]))

# Marginal histogram
pl.figure()
pl.xlim(0,1)
pl.hist(postBurnSamples)
pl.show()

# Trace plot
plt.figure()
plt.plot(range(ngens/sampleFreq),samples)
plt.ylim(0,1)
plt.ylabel("P")
plt.xlabel("Sample Number")
plt.show()      

"""
Play around with different settings for the analyses outlined above and try to 
answer these questions:
(1) How do trace plots differ if we record samples from every generation or if 
we space out our sampling? If samples are recorded every generation, the trace plot
will tend to look very dense ("fuzzy caterpillar look"). When I changed the sampling 
to every 200 generations, the plot looked more like a single line that varied around
a mean value (very poorly sampled). 
(2) How does the width of the 95% credible interval change as we add/subtract data?
Subtracting data (ngens) led to steadily narrowing 95% credible intervals. When
I reduced the number of generations to 10, the credible interval became 0 (0.514, 0.514).
(3) How does the trace plot change if the proposal window becomes much bigger 
or smaller for a given amount of data? When I changed the scale to 10, the trace 
plt became really blocky. The "manhatten skyline look." This shows that a given 
area of sampling space was sampled only briefly before jumping to a very different 
area of sampling space. When I changed scale to 0.3, the tracer plot showed some
difficulty in reaching optimal sampling space quickly (I would need to extend the
burn-in). 
"""
