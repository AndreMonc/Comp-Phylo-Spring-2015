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
probmat = [[0.7,0.3],[0.6,0.4]] #probmat is an array--a list of lists

# Try accessing a individual element or an individual row 
# Element
probmat[1][0] #This code will access the position 1 list and position 0 element

# Row
probmat[1] #This code will access the entire position 1 list (the first row in
#in the transition probability matrix)

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
arbEvents = [1,2]
prob = [0.9,0.1]
test=DiscreteSample(arbEvents,prob,numbOfTrial)
print test

# Write your Markov chain simulator below. Record the states of your chain in 
# a list. 

#I modeled this code after Jeremy's. Extremenly helpful to study that code in 
#order to better understand how Markov chains work.

def MarkovChSim(n,state=[1,2],allProbs=[[0.5,0.5],[0.5,0.5]]):
    """
    This is a Markov chain simulation function with discrete time and states.
    The first argument (n) defines the number of steps in the simulation (and 
    thus equals the length of the list output). The second argument defines the 
    state space (in this case only two alternatives), and the third argument 
    defines the transition matrix.
    """
    
    chainStates = []

    #Draw a random state to initiate the chain.
    numbOfTrial=1 #I only want one output to initiate the chain
    #The middle argument in the DiscreteSample function below simply generates
    #a list of equal probabilities for all the elements in list "state"    
    currState=DiscreteSample(state,[1.0/len(state) for x in state],numbOfTrial)
    chainStates.extend(currState)
    #Now I want to simulate the chain states for the interval n-1 (everything
    #after the initial state)
    for step in range(1,n):
        probability = allProbs[state.index(currState)] # Here I get a whole row
        #from the allProbs array associated with the current state
        currState = DiscreteSample(state,probability,1)
        chainStates.extend(currState) 
    return chainStates


# Run a simulation of 10 steps and print the output.

Markov10step = MarkovChSim(n=10,state=[1,2],allProbs=[[0.5,0.5],[0.5,0.5]])
print ("10-step Markov Chain simulation: " + str(Markov10step))
    

# ----> Try to finish the above lines before Tues, Feb. 10th <----

# Now try running 100 simulations of 100 steps each. How often does the chain
# end in each state? How does this change as you change the transition matrix?

sim100 = []
for step in range(100): #This "for loop" just runs the indented code 100 times
    Markov100step = MarkovChSim(n=100,state=[1,2],allProbs=[[0.5,0.5],[0.5,0.5]])
    endState =  Markov100step[99]   
    sim100.append(endState)
print sim100

count1 = sim100.count(1)
count2 = sim100.count(2)

print("The number of simulations out of 100 that end in state 1: " + str(count1))
print("The number of simulations out of 100 that end in state 2: " + str(count2))

#Now I'm gonna change the transition matrix so that state 1 is favored
sim100Fav1 = []
for step in range(100):
    Markov100step = MarkovChSim(n=100,state=[1,2],allProbs=[[0.8,0.2],[0.8,0.2]])
    endState =  Markov100step[99]   
    sim100Fav1.append(endState)
print sim100Fav1

countfav1_1 = sim100Fav1.count(1)
countfav1_2 = sim100Fav1.count(2)

print("The number of simulations out of 100 that end in state 1 (weighted towards 1): " + str(count1))
print("The number of simulations out of 100 that end in state 2 (weighted towards 1: " + str(count2))


# Try defining a state space for nucleotides: A, C, G, and T. 
NucStateSpace = ("A","C","G","T")

#Now define a transition matrix with equal probabilities of change between 
#states.


NucTransMat = [[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]
     
# Again, run 100 simulations of 100 steps and look at the ending states. Then
# try changing the transition matrix.

'''
I've been having a lot of trouble using letter labels in my state space. Thus,
I will make the following assignments: A=1,C=2,G=3,T=4.
'''

sim100Nucleo = []
for step in range(100):
    Markov100step = MarkovChSim(n=100,state=[1,2,3,4],allProbs=NucTransMat)
    endState =  Markov100step[99]   
    sim100Nucleo.append(endState)
print sim100Nucleo

sim100Nucleo.count(1)
sim100Nucleo.count(2)
sim100Nucleo.count(3)
sim100Nucleo.count(4)


#In order to see a really clear increase in endstates with "G" (or 4), I had
#increase the row 1 probability of T given A by a lot!
NucTransMatFavT = [[0.04,0.03,0.03,0.9],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]

sim100NucleoFavT = []
for step in range(100):
    Markov100step = MarkovChSim(n=100,state=[1,2,3,4],allProbs=NucTransMatFavT)
    endState =  Markov100step[99]   
    sim100NucleoFavT.append(endState)
print sim100NucleoFavT

sim100NucleoFavT.count(1)
sim100NucleoFavT.count(2)
sim100NucleoFavT.count(3)
sim100NucleoFavT.count(4)

#Here I increase the probability of T given any previous nucleotide.
#The number of T endstates is a little smaller here than for the above scenario
#Though note that that T is not favored nearly as much in any given row
NucTransMatFavTall = [[0.1,0.2,0.3,0.4],[0.1,0.2,0.3,0.4],[0.1,0.2,0.3,0.4],[0.1,0.2,0.3,0.4]]

sim100NucleoFavTany = []
for step in range(100):
    Markov100step = MarkovChSim(n=100,state=[1,2,3,4],allProbs=NucTransMatFavT)
    endState =  Markov100step[99]   
    sim100NucleoFavTany.append(endState)
print sim100NucleoFavTany

sim100NucleoFavTany.count(1)
sim100NucleoFavTany.count(2)
sim100NucleoFavTany.count(3)
sim100NucleoFavTany.count(4)
   
