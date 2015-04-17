from __future__ import division
import ctmc
import numpy
import math
from scipy.linalg import expm #necessary for the matrix exponentiation (to find marginal probabilities)


'''
Thanks to Subir for substantial help in completing this code!!
'''



class Node(object):
    
    def __init__(self,name="",parent=None,children=None, branchlength = 0, sequence = None):
        self.name = name
        self.parent = None
        if children is None:
            self.children = []
        else:
            self.children = children
        self.brl = branchlength
        if sequence is None:
            self.sequence = []
        else:
            self.sequence = sequence
        self.likeli  = [] #to save marginal probs
        


class Tree(Node):
    """
    Defines a class of phylogenetic tree, consisting of linked Node objects.
    """
    
    def __init__(self, stringNewick, model = None, inpSeqMat = None):
        self.root = Node("root")
        self.divideNewick(stringNewick, self.root) #Divides newickString in order to create a tree with name+branchlength info associated with each node
        self.setModels(self.root) #I've set the default starting sequence length to 10 (each of the 10 sites undergoes a Markov chain simulation. Default qMatrix is that in the Huelsenbeck reading.)
        #Also, I've set the root to always be "node" in the setModels method   
        if inpSeqMat is None: #If I have no sequence information, I will need to simulate a sequence 
            if model is None: # If no model provided, I will set the q Matrix (the model) to the matrix provided in the Huelsenbeck reading. Jukes-Cantor is an example of another model I could use.
                self.setModels(self.root)
            else: #If a model is provided, then I will use that model
                self.setModels(self.root, Model = model)
        else: #If seq info is provided (in the format of a matrix), I will need to format it into a dictionary first
            seqDict = {}
            for item in inpSeqMat:
                seqDict[item[0].replace(" ", "")]=item[1] #Here I remove the space beteen "Sp" and "A" (and the rest of the letters) and set each species as the dictionary key to its sequence.
            self.assignSeqs(self.root, seqDict)
            
    
    def divideNewick(self, stringNewick, root):
        """
        The point of this method is to take a newick-formatted string of 
        bases+branchlengths and store name and brl info for each node (the brl 
        leading up to that node).
        """
        stringNewick = stringNewick.replace(" ", "")[1:-1] #Remove spaces and outside parentheses from the newick string
        #print "String Newick: " + stringNewick        
        x = 0
        if stringNewick.count(",") != 0: #As long as there are still multiple terminal nodes in the string, this loop will continue
            for pos in range(len(stringNewick)): #Purpose of this loop is to find the comma between sets of parentheses (so I can divide branches)
                if stringNewick[pos] == "(":
                    x += 1 #For every open parenthesis in the newick string I want to add 1 to x
                elif stringNewick[pos] == ")":
                    x -= 1 #For every close parenthesis in the newick string I want to subtract 1 from x
                elif stringNewick[pos] == ",":
                    if x == 0: #This condition will only be met for a complete node (starting from "earlier" nodes and moving towards terminal nodes)
                        tupSplit = (stringNewick[0:pos], stringNewick[pos+1:len(stringNewick)]) #Here I divide the string into two nodes in order to work with each node individually
                        for elem in tupSplit: #Each node gets the following treatment
                            if elem[-1] != ")": #If the last character in the string is not a parenthesis I know there is a brl associated with the node (a given brl leading up to that node). 
                                stringNewick = elem[0:elem.rfind(":")] #newickString includes all data except the brl length
                                storedNode = Node(name=stringNewick, parent=root) #storing a node entry
                                storedNode.brl = float(elem[elem.rfind(":")+1:]) #storing a branchlength entry for the given node (branchlength corresponds to length of branch leading up to that node).
                                root.children.append(storedNode) #here I identify the children for the root ("root" signifies the actual root before recursion, and then means simply "ancestor" once recursion begins.)
                                self.divideNewick(stringNewick, storedNode)
                            else: #This section of code allows for an input of a newick string without branch lengths
                                storedNode = Node(name=stringNewick, parent=root)
                                root.children.append(storedNode) 
                                self.divideNewick(stringNewick, storedNode)
                        break # To prevent endless looping
    
    
    
    
    
    def printNames(self,node):
        """
        A method of a Tree object that will print out the names of its
        terminal nodes. 
        
        We worked out a version of this code on the whiteboard in class.            
        """
        if len(node.children) > 0: #Wasn't sure how to set up this first line. Borrowed from Glaucia. It ensures that all internal nodes run through recursion. Terminal nodes will go to else.
            for child in node.children: #iterating through each descendent of the given node  
                self.printNames(child) #This is the key statement. It causes the method to restart on the children nodes.
        else: 
            print node.name #Print terminal node name      
    
 
    # Write a recursive function to calculate the total tree length (the sum of
    # all the branch lengths). Again, the root node of a tree should be the only 
    # argument the first time this function is called. 

    
    def treeLength(self,node):
        """
        A method to calculate and return total tree length.
        Below is similar to the code that Glaucia/Marco suggested in class,
        but I added an else statement and a return outside the forloop. To me,
        this is more intuitive and it gives the same result (though it takes
        slightly more code).
        """
        
        totbrl = 0
        if node.children is not None: #(If the node is an internal node)
            for child in node.children: 
                totbrl = totbrl + self.treeLength(child) #Recursively add the branch length leading up to each internal node
        else:
            node.brl + totbrl #Add branch length leading up to each terminal node
        return node.brl + totbrl
             
            
    # Write a recursive function that takes the root node as one of its arguments
    # and prints out a parenthetical (Newick) tree string. Due next Tues (3/17).
    
    
    def newick(self,node):
        """
        A method of a Tree object that will print out the Tree as a 
        parenthetical string (Newick format). Based on Subir's code.
        """
        newickString = "(" #This is open parentheses will be the start of all newick strings
        if node.children == []: #If there are no offspring for a given node, then ...
            return node.name + ":" + str(node.brl) #I want to simply get name:branchlength leading up to that terminal node
        else: 
            for c in node.children:
                if node.children[-1] == c:
                    newickString += self.newick(c) #I want the last-in-the-list offspring of a node to have no punctuation associated with it
                else:
                    newickString += self.newick(c) + "," #I want non-last-in-the-list offspring to have a comma after their names
            if node.brl != 0:
                newickString += "):" + str(node.brl) #For branchlengths associated with an internal node I want to print that brl outside that parentheses.
            else:
                newickString += ")" #If no brl associated with that internal node (specifically, the root), then I only want a parenthesis to close the newick string
            return newickString
    
                
    # Now, let's write a recursive function to simulate sequence evolution along a
    # tree. This amounts to simply simulating evolution along each branch 
    # from the root towards the tips. We'll need to use our ctmc class for setting the 
    # conditions of our simulation, which is why we imported it above our tree 
    # class definition. In this case, we've stored the definition of our ctmc 
    # class in a separate file (ctmc.py) to keep our tree code compact.
    # Now, let's add a ctmc object to each internal node in our tree (except the
    # root). Again, it would be best to add the ctmcs as part of the Node
    # constructor, if we know that we'll be simulating data.
    
     
    def setModels(self, node, Model = None, seqLength = None):
        """
        This method of a Tree object defines a ctmc object that is associated
        with each node that has a branch length (all nodes but the root). If I 
        to change models (i.e., Q-matrix values) I can add that new model as an 
        argument to this method. Otherwise, the default model values is the one 
        given in the Huelsenbeck reading.
        """
        
        if Model is None and seqLength is None:
            node.sequence = [ctmc.contMarkov().cmSim()]
        elif Model is None and seqLength is not None:
            node.sequence = [ctmc.contMarkov().cmSim(seqL=seqLength)]
        elif Model is not None and seqLength is None:
            node.sequence = [ctmc.contMarkov(matrix = Model).cmSim()]
        else: #If no model or seqLength is provided by user the default is:
            node.sequence = [ctmc.contMarkov(matrix = Model).cmSim(seqL=seqLength)]
        self.simulate(node) 
    


    
    def simulate(self,node):
        
        """
        This method simulates evolution along the branches of a tree, taking
        the root node as its initial argument.
        """
       
        if node.children == []: #not simulating for the root (which has no associated brl)
            pass #This is a handy key word 
        else:
            for child in node.children:
                child.sequence = [ctmc.contMarkov(arbBrl=child.brl).cmSim(startSeq=node.sequence)]
                self.simulate(child) #The key line that introduces recursion through the whole tree       
       
    
    
    def printSeqs(self,node):
        """
        This method prints out the names of the tips and their associated
        sequences as an alignment (matrix).
        """
        if node.children == []:
            print node.name , node.sequence
        for child in node.children:
            self.printSeqs(child)
    
    
    
    def assignSeqs(self, node, seqDict):
        #The purpose of this method is to store in memory the corresponding sequence for each node 
        if node.name in seqDict:
            node.sequence = seqDict[node.name] #This line stores the value (sequence) for the given node name. Since I iterate through all node names, I will store all corresponding sequences.
            node.likeli = self.probFinSt(node) #This line stores the conditional probabilities at each node
        else: #In case the provided node name is not found as a key in the dict, it should have a child as a key in the dict
            for child in node.children:
                self.assignSeqs(child, seqDict)
    
    def probFinSt(self, node):
        finalProbDict = {"A": [1,0,0,0], "C": [0,1,0,0], "G": [0,0,1,0], "T":[0,0,0,1],
                         "B": [1,1,0,0], "D": [1,0,1,0], "E": [1,0,0,1], "F":[0,1,1,0],
                         "H": [0,1,0,1], "I": [1,1,1,0], "J": [1,1,0,1], "K":[0,1,1,1],
                         "L": [1,0,1,1], "M": [0,0,1,1], "N": [1,1,1,1]}
        storage = []
        for base in range(len(node.sequence)):
            storage.append(finalProbDict[node.sequence[base]])
        return numpy.array(storage)
    
class Likelihood:
    #Goal is to calculate the likelihood of a tree given know species sequences 
    
    def __init__(self, matrix, node, likeli = 0):
        self.matrix = numpy.array(matrix)
        self.P = self.margProbMat()
        self.generator(node) #Finds the conditional probabilities associated with each nucleotide at each node
        self.TreeLike(node) #This calculates the likelihood
        
    def margProbMat(self, branchlength=100):
        #Generates a marginal probability matrix given a specified Q matrix and branchlength
        return (expm(numpy.array(self.matrix) * branchlength))
        	
 
    def generator(self,node): #Finds the conditional probabilities associated with each nucleotide at each node
        conProbs = [] #List with conditional probabilities
        brl = [] #list with the branch lengths
        for child in node.children:
            if child.likeli == []:
                self.generator(child) #Key recursive portion of method. Must go to tip and then work backwards.
            conProbs.append(child.likeli)
            brl.append(child.brl)
        node.likeli = self.calcAncMatrix(conProbs[0], conProbs[1], brl[0], brl[1])
    
    def calcAncMatrix(self, val0, val1, brl0, brl1): #the values in the argument are passed from the generator method
            #Purpose is to calculate the probability matrix of an ancestral node, given all known descendents
        matrixFirst = self.margProbMat(branchlength=brl0).transpose() #Here I calculate a p matrix for the first branch. Transpose formats the matrix for use in matrix multiplication.
        matrixSec = self.margProbMat(branchlength=brl1).transpose() #Here I calculate a p matrix for the second branch. Transpose formats the matrix for use in matrix multiplication.
        multFirst = [y.dot(matrixFirst) for y in val0]
        multSec = [y.dot(matrixSec) for y in val1]
        ancMat = []
        for i in range(len(multFirst)):
            futureCond = []
            for j in range(len(multFirst[i])):
                futureCond.append(multFirst[i][j]* multSec[i][j])
            ancMat.append(futureCond)
        return numpy.array(ancMat)

    def TreeLike(self, node):
        finLike = (self.P[0].dot(node.likeli.transpose())) #Multiply with marginal probabilities and add the terms to get total likelihood for each site
        likeli = 1
        for val in finLike:
            likeli *= val
        return likeli
        
        
#I want to check the code based on the likelihood worksheets we worked on in
#class

stringNewick = "((Sp A:0.1, Sp B:0.13):0.13 , (Sp C: 0.15, (Sp D:0.1, Sp E:0.15):0.3):0.02)" #Tree provided in class
inpSeqMat = 	[["Sp A", "NACA"], #sequences provided with the 5-species tree Jeremy gave us
		["Sp B", "NACC"],
		["Sp C", "NAGG"],
		["Sp D", "NATT"],
		["Sp E", "NATA"]]
matrix = [[-0.96, 0.38,0.39,0.19], #This is the (approximate) Q matrix for the transition prob matrices that were provided by Jeremy in the worksheet. Thanks to Subir for calculating it (he took natural log of transition probability matrix). 
		  [0.29,-0.78,0.39,0.1],
		  [0.58,0.76,-1.44,0.1],
		  [0.58,0.38,0.19,-1.15]]
  
   
Test = Tree(stringNewick, model = matrix, inpSeqMat = inpSeqMat)
b = Likelihood(matrix, Test.root)

#print b.MP

print b.TreeLike(Test.root)

#stringNewick = "((spA:0.6, spB:0.6):0.3, (spC:0.03, spD:0.03):0.05)"     
     
#i=Tree(stringNewick)

#print ("The simulated sequences for each species:")
#i.printSeqs(i.root)

#Intuitive check: Make sure that species with longer branch lengths have 
#more differences between their sequences. However, once branch lengths got 
#longer than ~0.7 I noticed the sequences did not appear more divergent with 
#increasing branchlength. 


#print ("Name of each species in tree:")
#i.printNames(node=i.root)

#print ("The tree length is: ")
#print i.treeLength(node=i.root)

#print ("The newick string is: ") 
#print i.newick(node=i.root)













