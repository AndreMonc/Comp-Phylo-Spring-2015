from __future__ import division
import ctmc

"""
Exercise 6 - Creating and Using Node and Tree Classes
@author: jembrown

# ---> Defining Node and Tree classes <---
"""

'''
Written with help from Subir.
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
        


class Tree(Node):
    """
    Defines a class of phylogenetic tree, consisting of linked Node objects.
    """
    
    def __init__(self, stringNewick):
        self.root = Node("root")
        self.divideNewick(stringNewick, self.root) #Divides newickString in order to create a tree with name+branchlength info associated with each node
        self.setModels(self.root) #I've set the default starting sequence length to 10 (each of the 10 sites undergoes a Markov chain simulation. Default qMatrix is that in the Huelsenbeck reading.)
        #Also, I've set the root to always be "node" in the setModels method   
    
    
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
            node.sequence = [ctmc.contMarkov(Qmatrix = Model).cmSim()]
        else: #If no model or seqLength is provided by user the default is:
            node.sequence = [ctmc.contMarkov(Qmatrix = Model).cmSim(seqL=seqLength)]
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
    
    
    
    
stringNewick = "((spA:0.9, spB:0.5):0.3, (spC:0.03, spD:0.03):0.05)"     
     
i=Tree(stringNewick)

print ("The simulated sequences for each species:")
i.printSeqs(i.root)

print ("Name of each species in tree:")
i.printNames(node=i.root)

print ("The tree length is: ")
print i.treeLength(node=i.root)

print ("The newick string is: ") 
print i.newick(node=i.root)













