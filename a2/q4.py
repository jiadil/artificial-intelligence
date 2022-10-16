"""
q4
color the map of US and Canada with 4 colors, such that no adjacent states, provinces or territories have the same color.
"""


import random
import sys
import matplotlib.pyplot as plt
import numpy as np

'''
Step 1: Generate the initial population
populationSize is one of the configurable parameters of the algorithm. Each member of the population is called a stateName. Initially, all nodes of each stateName are colored randomly.
Hint: You can use a simple array to represent the state of a stateName.
'''
class Map:
    '''This class stores edges and city names'''
    def __init__(self, fname):
        f = open(fname, 'r')
        lines1 = f.readlines()
        f.seek(0)
        lines2 = f.readlines()
        f.close()
        self.regions = []
        self.adjacency_matrix = []
        self.num_of_edges = 0

        # city names
        for line in lines1:
            line = line.strip("\n\t").split(" ")
            self.regions.append(line[0])

        # edges
        for line in lines2:
            line = line.strip("\n\t").split(" ")
            tmp = [0] * 64
            for s in line[1:]:
                tmp[self.regions.index(s)] = 1
                self.num_of_edges += 1
            self.adjacency_matrix.append(tuple(tmp))
        self.num_of_edges /= 2

        self.regions = tuple(self.regions)
        self.adjacency_matrix = tuple(self.adjacency_matrix)

        # for i in range(64):
        #     print(self.regions[i], end = '', sep = '')
        #     print(self.adjacency_matrix[i])


class Chromosome:
    '''This class creates chromosome and define fitness given a state'''
    def __init__(self, map, state = None):
        # if state is given, create a chromosome basd on the state
        if state:
            self.state = state
        
        # if no state given, create a random state chromosome
        else:
            self.state = []
            for i in range(64):
                self.state.append(random.randint(0,3))
            self.state = tuple(self.state)

        # calculate the fitness
        self.fitness = self.fitness_f(map)
    
    def printState(self):
        return list(self.state)

    '''
    Step 2: Determine the fitness of each stateName
    The fitness function describes how good an answer is, and is used for choosing the parents.
    ''' 
    # fitness function
    def fitness_f(self, map):
        result = 0
        for i in range(64):
            for j in range(64):
                if map.adjacency_matrix[i][j] == 1 and self.state[i] != self.state[j]:
                    result += 1
        return result/(2 * map.num_of_edges)
                    
        
class Population:
    '''This class stores chromosomes and gets their stat data'''
    def __init__(self, populationSize, map):
        self.populationSize = populationSize
        self.chromosomes = []
        self.solution = None
        for i in range(populationSize):
            self.chromosomes.append(Chromosome(map))
        self.chromosomes = tuple(self.chromosomes)
    
    def solution_test(self):
        for c in self.chromosomes:
            if c.fitness == 1:
                self.solution = c
                return True
        return False
    
    def get_stat(self):
        
        max_fit = self.chromosomes[0].fitness
        min_fit = self.chromosomes[0].fitness
        mean = 0
        for i in range(self.populationSize):
            x = self.chromosomes[i].fitness
            
            if x > max_fit:
                max_fit = x
            
            if x < min_fit:
                min_fit = x
            
            mean += x
            
        return max_fit, min_fit, mean/self.populationSize 


'''
Step 3: Choose the parents
In this step, you use the tournament selection method. This method first randomly chooses k members of the population and then chooses the best of them. 
'''
def tournament(tournamentSize, population):
    '''This function generates tournament selection'''
    result = []
    tmp = list(population.chromosomes)
    random.shuffle(tmp)
    n = int(population.populationSize / tournamentSize)
    for i in range(n):
        random_ones = []
        for j in range(tournamentSize):
            random_ones.append(tmp[i * tournamentSize + j])
        index = 0
        best_fit = random_ones[0].fitness
        for k in range(1, tournamentSize):
            if random_ones[k].fitness > best_fit:
                index = k
                best_fit = random_ones[k].fitness
        result.append(random_ones[index])
    return tuple(result)


'''
Step 4: Produce the next generation
'''
def crossover(x, y):
    '''This function crossovers the chosen parents'''
    # l = []
    # for i in range(64):
    #     j = random.randint(0, 1)
    #     if j == 1:
    #         l.append(x[i])
    #     else:
    #         l.append(y[i])
    # return l
    lx = list(x[:32])
    ly = list(y[32:])
    return lx + ly


'''
step 5: mutation
'''
def mutate(arr2D, populationSize, n):
    '''This function randomly mutates a certain number of genes in the whole new population'''
    s = set()
    while len(s) < n:
        i = random.randint(0, populationSize - 1)
        j = random.randint(0, 63)

        if (i, j) not in s:
            arr2D[i][j] = random.choice(list({0, 1, 2, 3} - {arr2D[i][j]}))
            s.add((i, j))
            
    
def q4(numberOfGenerations, populationSize, tournamentSize, mutationRate):
    '''This function gets and prints result'''
    # create initial population and map
    map = Map(sys.path[0] + '/state_neighbors.txt')
    p = Population(populationSize, map)
    # create y-list to store stat data
    yBests = []
    yWorsts = []
    yAverages = []
    i = 0
    while i < numberOfGenerations and not p.solution_test():
        # print stats
        best, worst, mean = p.get_stat()
        print("Generation #" + str(i))
        print("Best fitness: " + str(best))
        print("Worst fitness: " + str(worst))
        print("Average fitness: " + str(mean) + "\n\n\n")

        # store data
        yBests.append(str(best))
        yWorsts.append(str(worst))
        yAverages.append(str(mean))
        
        # choose parents (from step 3)
        parents = tournament(tournamentSize, p)
        newChros = []
        
        # produce next generation (from step 4)
        for j in range(populationSize):
            tmp = random.sample(parents, 2)
            chro = crossover(tmp[0].state, tmp[1].state)
            newChros.append(chro)
            
        # mutation (from step 5)
        mutate(newChros, populationSize, int(populationSize * 64 * mutationRate))
        
        '''
        step 6: replace the old population and repeat
        '''
        new_p = []
        for k in range(populationSize):
            new_p.append(Chromosome(map, tuple(newChros[k])))
        p.chromosomes = tuple(new_p)
        i += 1
        
    # print result
    if p.solution_test():
        print("Solution is found in generation #" + str(i) + ":")
        stateColor = p.chromosomes[-1].printState()
        stateName = map.regions
        for m in range(len(stateName)): 
            print(stateName[m] + ": " + str(stateColor[m]))

        # plot the graph
        x = []
        for n in range(i):
            x.append(n)
        yBest = [float(y) for y in yBests]
        yWorst = [float(y) for y in yWorsts]
        yAverage = [float(y) for y in yAverages]
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.yticks(np.arange(0.50,1.05,0.05))
        plt.plot(x, yBest, label = "Best")
        plt.plot(x, yWorst, label = "Worst")
        plt.plot(x, yAverage, label = "Average")
        plt.legend()
        plt.show()
        plt.close()
    else:
        print("Didn't find a folution")
        for m in p.chromosomes:
            print(m.fitness)

# try different values
numberOfGenerations = 5000
populationSize = 100
tournamentSize = 2
mutationRate = 0.02

q4(numberOfGenerations, populationSize, tournamentSize, mutationRate)
