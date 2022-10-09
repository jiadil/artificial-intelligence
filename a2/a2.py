import random

"""
Step 1: Generate the initial population
populationSize is one of the configurable parameters of the algorithm. Each member of the population is called a stateName. Initially, all nodes of each stateName are colored randomly.
Hint: You can use a simple array to represent the state of a stateName.
"""
class Node(object):
    '''This class define a node with the name and a random color assigned from four colors'''
    def __init__(self, stateName):
        self.stateName = stateName
        self.color = random.choice(['green', 'red', 'blue', 'yellow'])
    def __repr__(self):
        return self.stateName + "(" + self.color + ")"

class Edge(object):
    '''This class define an edge that represents the link between the first node and second node''' 
    def __init__(self, firstNode, secondNode):
        self.firstNode = firstNode
        self.secondNode = secondNode
    def __repr__(self):
        return "(" + self.firstNode + ", " + self.secondNode + ")"

class Graph(object):
    '''This class define a graph with two lists: edges and nodes'''
    def __init__(self):
        self.nodes = []
        self.edges = []     
    def add_node(self, stateName):
        node = Node(stateName)
        self.nodes.append(node)
    def add_edge(self, firstNode, secondNode):
        add = True
        for state in self.nodes:
            if secondNode == state.stateName:
                add = False
        if add:
            edge = Edge(firstNode, secondNode)
            self.edges.append(edge)

def createGraph(filename):
    '''This function aims to produce node and edge list from the given file'''
    # read the input file
    f = open(filename,"r")
    lines = f.readlines()
    # initialize the graph object
    graph = Graph()
    # store the file elements to the graph object
    for line in lines:
        stateList = line.strip().split()
        graph.add_node(stateList[0])
        for state in stateList[1:]:
            graph.add_edge(stateList[0], state)
    return graph

graph = createGraph('state_neighbors.txt')
States = graph.nodes
AdjacentRel = graph.edges

print("\nAll States: node in total " + str(len(States)) + ":")
print(States)

print("\nAll Adjacent Relationships: edges in total " + str(len(AdjacentRel)) + ":")
print(AdjacentRel)

print("\n\n")


'''
Step 2: Determine the fitness of each stateName
The fitness function describes how good an answer is, and is used for choosing the parents.
'''
def fitness(States, AdjacentRel):
    '''This function aims to calculate the fitness for current "chromosome"'''
    # set initial fitness equal to 0
    # δ(i,j)=1 if c(ni)c(nj) and δ(i,j)=0 if c(ni)=c(nj)
    delta = 0
    # read through all adjacent relationship to find the fitness
    for edge in AdjacentRel:  
        for state in States:
            if edge.firstNode == state.stateName:
                firstNodeColor = state.color
            if edge.secondNode == state.stateName:
                SecondNodeColor = state.color
        if firstNodeColor == SecondNodeColor:
            delta += 0
        else:
            delta += 1
    return delta/len(AdjacentRel)

print("fitness of current chromosome: ")
print(fitness(States, AdjacentRel))