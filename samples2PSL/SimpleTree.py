import pdb
import re 


unary_operators = ['G', 'F', '!', 'X', '*']
binary_operators = ['&', '|', 'U', '->', '|->', '+', '.']


class SimpleTree:
    def __init__(self, label = "dummy"):
        self.left = None
        self.right = None
        self.label = label
    
    def __hash__(self):
        return hash((self.label, self.left, self.right))
    
    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.label == other.label and self.left == other.left and self.right == other.right
    
    def __ne__(self, other):
        return not self == other
    
    def _isLeaf(self):
        return self.right == None and self.left == None
    
    def _addLeftChild(self, child):
        if child == None:
            return
        if type(child) is str:
            child = SimpleTree(child)
        self.left = child
        
    def _addRightChild(self, child):
        if type(child) is str:
            child = SimpleTree(child)
        self.right = child
    
    def addChildren(self, leftChild = None, rightChild = None): 
        self._addLeftChild(leftChild)
        self._addRightChild(rightChild)
        
        
    def addChild(self, child):
        self._addLeftChild(child)
        
    def getAllNodes(self):
        leftNodes = []
        rightNodes = []
        
        if self.left != None:
            leftNodes = self.left.getAllNodes()
        if self.right != None:
            rightNodes = self.right.getAllNodes()
        return [self] + leftNodes + rightNodes

    def getAllLabels(self):
        if self.left != None:
            leftLabels = self.left.getAllLabels()
        else:
            leftLabels = []
            
        if self.right != None:
            rightLabels = self.right.getAllLabels()
        else:
            rightLabels = []
        return [self.label] + leftLabels + rightLabels

    def __repr__(self):
        if self.left == None and self.right == None:
            return self.label
        
        # the (not enforced assumption) is that if a node has only one child, that is the left one
        elif self.left != None and self.right == None:
            return self.label + '(' + self.left.__repr__() + ')'
        
        elif self.left != None and self.right != None:
            return self.label + '(' + self.left.__repr__() + ',' + self.right.__repr__() + ')'

'''
A class for encoding syntax Trees and syntax DAGs of PSL formulas
'''

class Formula(SimpleTree):
    
    def __init__(self, formulaArg = "dummyF"):
        if not isinstance(formulaArg, str):
            self.label = formulaArg[0]
            self.left = formulaArg[1]
            try:
                self.right = formulaArg[2]
            except:
                self.right = None
        else:
            super().__init__(formulaArg)

    def __lt__(self, other):

        if self.getDepth() < other.getDepth():
            return True
        elif self.getDepth() > other.getDepth():
            return False
        else:
            if self._isLeaf() and other._isLeaf():
                return self.label < other.label

            if self.left != other.left:
                return self.left < other.left

            if self.right is None:
                return False
            if other.right is None:
                return True
            if self.right != other.right:
                return self.right < other.right

            else:
                return self.label < other.label


    def prettyPrint(self, top=False):
        if top is True:
            lb = ""
            rb = ""
        else:
            lb = "("
            rb = ")"
        if self._isLeaf():
            return self.label
        if self.label in unary_operators:
            return lb + self.label +" "+ self.left.prettyPrint() + rb
        if self.label in binary_operators:
            return lb + self.left.prettyPrint() +" "+  self.label +" "+ self.right.prettyPrint() + rb
    
    
    
    def getAllVariables(self):
        allNodes = list(set(self.getAllNodes()))
        return [ node for node in allNodes if node._isLeaf() == True ]
    def getDepth(self):
        if self.left == None and self.right == None:
            return 0
        leftValue = -1
        rightValue = -1
        if self.left != None:
            leftValue = self.left.getDepth()
        if self.right != None:
            rightValue = self.right.getDepth()
        return 1 + max(leftValue, rightValue)
    
    def getNumberOfSubformulas(self):
        return len(self.getSetOfSubformulas())
    
    def getSetOfSubformulas(self):
        if self.left == None and self.right == None:
            return [repr(self)]
        leftValue = []
        rightValue = []
        if self.left != None:
            leftValue = self.left.getSetOfSubformulas()
        if self.right != None:
            rightValue = self.right.getSetOfSubformulas()
        return list(set([repr(self)] + leftValue + rightValue))        