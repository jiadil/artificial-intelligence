import random
import sys

# map store edges and city names
class Map:
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
    
    # fitness function
    def fitness_f(self, map):
        result = 0
        for i in range(64):
            for j in range(64):
                if map.adjacency_matrix[i][j] == 1 and self.state[i] != self.state[j]:
                    result += 1
        return result/(2 * map.num_of_edges)
                    
        

class Population:

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

def tournament(tournamentSize, population):
    
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

# 这个不确定怎么分x和y 她也没细说
def crossover(x, y):
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

def mutate(arr2D, populationSize, n):

    s = set()
    while len(s) < n:
        i = random.randint(0, populationSize - 1)
        j = random.randint(0, 63)

        if (i, j) not in s:
            arr2D[i][j] = random.choice(list({0, 1, 2, 3} - {arr2D[i][j]}))
            s.add((i, j))
            
    
def q4(numberOfGenerations, populationSize, tournamentSize, mutationRate):
    
    # create initial population and map
    map = Map(sys.path[0] + '/state_neighbors.txt')
    print(map.num_of_edges)
    p = Population(populationSize, map)
    
    i = 0
    while i < numberOfGenerations and not p.solution_test():
        
        # print stats
        best, worst, mean = p.get_stat()
        print("Generation #" + str(i))
        print("Best fitness: " + str(best))
        print("Worst fitness: " + str(worst))
        print("Average fitness: " + str(mean) + "\n\n\n")
        
        # step 3: choose the parents
        parents = tournament(tournamentSize, p)
        newChros = []
        
        # step 4: Produce the next generation
        for j in range(populationSize):
            tmp = random.sample(parents, 2)
            chro = crossover(tmp[0].state, tmp[1].state)
            newChros.append(chro)
            
        # step 5: mutation
        mutate(newChros, populationSize, int(populationSize * 64 * mutationRate))
        
        # step 6: replace the old population and repeat
        new_p = []
        for k in range(populationSize):
            new_p.append(Chromosome(map, tuple(newChros[k])))
        p.chromosomes = tuple(new_p)
        i += 1
        
    # TODO:print result
    # if p.solution_test():
    #     print(i)
    # else:
    #     for i in p.chromosomes:
    #         print(i.fitness)



        
            
            
# try different values
numberOfGenerations = 5000
populationSize = 1000
tournamentSize = 10
mutationRate = 0.02

q4(numberOfGenerations, populationSize, tournamentSize, mutationRate)

