from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 09:43:43 2015

@author: Andre
"""

"""
Exercise 4
Discrete-time Markov chains
@author: jembrown
"""

"""
In this exercise, we will explore Markov chains that have discrete state spaces
and occur in discrete time steps. To set up a Markov chain, we first need to 
define the states that the chain can take over time, known as its state space.
To start, let's restrict ourselves to the case where our chain takes only two
states. We'll call them A and B.
"""

# Create a tuple that contains the names of the chain's states
markStates = ("A","B")
print(markStates)


"""
The behavior of the chain with respect to these states will be determined by 
the probabilities of taking state A or B, given that the chain is currently in 
A and B. Remember that these are called conditional probabilities (e.g., the 
probability of going to B, given that the chain is currently in state A is 
P(B|A).)
We record all of these probabilities in a transition matrix. Each row
of the matrix records the conditional probabilities of moving to the other
states, given that we're in the state associated with that row. In our example
row 1 will be A and row 2 will be B. So, row 1, column 1 is P(A|A); row 1, 
column 2 is P(B|A); row 2, column 1 is P(A|B); and row 2, column 2 is P(B|B). 
All of the probabilities in a ROW need to sum to 1 (i.e., the total probability
associated with all possibilities for the next step must sum to 1, conditional
on the chain's current state).
In Python, we often store matrices as "lists of lists". So, one list will be 
the container for the whole matrix and each element of that list will be 
another list corresponding to a row, like this: mat = [[r1c1,r1c2],[r2c1,r2c2]]. 
We can then access individual elements use two indices in a row. For instance,
mat[0][0] would return r1c1. Using just one index returns the whole row, like
this: mat[0] would return [r1c1,r1c2].
Define a transition matrix for your chain below. For now, keep the probabilties
moderate (between 0.2 and 0.8).
"""

# Define a transition probability matrix for the chain with states A and B
probmat = [[0.7,0.3],[0.6,0.4]]

# Try accessing a individual element or an individual row 
# Element
probmat[1][0] #This will access the position 1 list and position 0 element

# Row
probmat[1] #This will access the entire position 1 list

"""
Now, write a function that simulates the behavior of this chain over n time
steps. To do this, you'll need to return to our earlier exercise on drawing 
values from a discrete distribution. You'll need to be able to draw a random
number between 0 and 1 (built in to scipy), then use your discrete sampling 
function to draw one of your states based on this random number.
"""
# Import scipy U(0,1) random number generator

from scipy.stats import rv_discrete

# Paste or import your discrete sampling function

def DiscreteSample(xk,pk,numbOfTrial): #Adding size because it allows more 
    #flexibility to this function
    #Line below apparently necessary in order for rv_discrete to work?    
    discrete = rv_discrete(name='discrete', values=(xk,pk)) 
    sample = discrete.rvs(size=numbOfTrial)
    x = []
    x.append(sample)
    y = x[0]
    return y

numbOfTrial = 1
arbEvents = [5,6,7,8,9]
prob = [0.3,0.1,0.2,0.2,0.2]
y=DiscreteSample(arbEvents,prob,numbOfTrial)
#So, I add the line below, because it takes y array and extracts the first 
#indexed list from that array (y[0]). I found that it was much easier to work with
#a list than an array. For instance, I was unable to use the count method on an 
#array, but was able to use it with a list.
print y

# Write your Markov chain simulator below. Record the states of your chain in 
# a list. 

#I modeled this code after Jeremy's. Extremenly helpful to study that code in 
#order to better understand how Markov chains work.

def MarkovChSim(n,state=["A","B"],allProbs=[[0.5,0.5],[0.5,0.5]]):
    """
    This is a Markov chain simulation function with discrete time and states.
    The first argument (n) defines the number of steps in the simulation (and 
    thus equals the length of the list output). The second argument defines the 
    state space (in this case only two alternatives), and the third argument 
    defines the transition matrix.
    """
    
    chainStates = []

#Draw a random state to initiate the chain.
    state=["A","B"]
    prob=[0.5,0.5]
    numbOfTrial=1 #I only want one output to initiate the chain
    currState=DiscreteSample(state,prob,numbOfTrial)
    chainStates.extend(currState)
    #Now I want to simulate the chain states for the interval n-1 (everything
    #after the initial state)
    for step in range(1,n):
        probability = allProbs[state.index(currState)] # Here I get a whole row
        #from the allProbs array associated with the current state
        currState = DiscreteSample(state,probability,1)
        chainStates.extend(currState)
    return chainStates


#I still haven't gotten the above code to work smoothly...this week has been a bit hectic. I'll be focusing bigtime on 
#Python over the weekend!!

# Run a simulation of 10 steps and print the output.



# ----> Try to finish the above lines before Tues, Feb. 10th <----

# Now try running 100 simulations of 100 steps each. How often does the chain
# end in each state? How does this change as you change the transition matrix?




# Try defining a state space for nucleotides: A, C, G, and T. Now define a 
# transition matrix with equal probabilities of change between states.



         
# Again, run 100 simulations of 100 steps and look at the ending states. Then
# try changing the transition matrix.
