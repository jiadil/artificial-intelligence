import time
from search import *

###########################################################
######
# q3a
#
def make_rand_StagePuzzle():
    
    stop = False
    init_state = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    
    # shuffle initialized state until find a solvable puzzle instance
    while not stop:
        state = shuffled(init_state)
        puzzle = StagePuzzle(state)
        stop = puzzle.check_solvability(state)

    puzzle.initial = tuple(puzzle.initial)
    return puzzle

###########################################################
######
# q3b
#
def display(state):
    
    # return null when the puzzle is not correctly generated
    if len(state) != 10:
        print("wrong number of states")
        return
    i = 0

    # first line
    print("   ", sep = '', end = '')
    while i < 2:
        if state[i] == 0:
            print("*  ", sep = '', end = '')
        else:
            print(str(state[i]) + "  ", sep = '', end = '')
        i = i + 1

    # second line
    print("\n", sep = '', end = '')
    while i < 6:
        if state[i] == 0:
            print("*  ", sep = '', end = '')
        else:
            print(str(state[i]) + "  ", sep = '', end = '')
        i = i + 1
    
    # third line
    print("\n", sep = '', end = '')
    while i < 10:
        if state[i] == 0:
            print("*  ", sep = '', end = '')
        else:
            print(str(state[i]) + "  ", sep = '', end = '')
        i = i + 1

    print("\n", sep = '', end = '')


###########################################################
######
# q3c
#
# h_type: 0 for misplaced, 1 for Manhattan Distance, 2 for max of them
#
def print_stat(puzzle, h_type):
    
    if h_type not in (0, 1, 2):
        print("Invalid h_type")
        return
    
    start_time = time.time()
    node, num_of_expanded = astar_search(puzzle, h_type)
    elapsed_time = time.time() - start_time
    
    # 5 digits for running time
    print("Running Time: " + str(round(elapsed_time, 5)) + "s   Solution Length: " + str(len(node.solution())) + "   Nodes Expanded: " + str(num_of_expanded))
    return elapsed_time, len(node.solution()), num_of_expanded

def q3_c(num_of_puzzles):
    
    # for calculating the means
    md_time = []
    md_len = []
    md_node = []
    
    mp_time = []
    mp_len = []
    mp_node = []
    
    mx_time = []
    mx_len = []
    mx_node = []
    print()
    
    # repeate num_of_puzzles times
    for i in range(num_of_puzzles):
        print("Instance " + str(i + 1) + ": ")
        puzzle = make_rand_StagePuzzle()
        print(puzzle.initial)

        print("Manhattan Distance:")
        time, len, node = print_stat(puzzle, 1)
        md_time.append(time)
        md_len.append(len)
        md_node.append(node)
        
        print("Misplaced:")
        time, len, node = print_stat(puzzle, 0)
        mp_time.append(time)
        mp_len.append(len)
        mp_node.append(node)

        print("Combined:")
        time, len, node =  print_stat(puzzle,2)
        mx_time.append(time)
        mx_len.append(len)
        mx_node.append(node)

        print("\n\n")

    # summary for mean values
    print("\nSummary on average:\n")
    print("Manhattan Distance:\n" + "Time: " + str(round(sum(md_time) / num_of_puzzles, 5))
          + "  Solution Length: " + str(sum(md_len) / num_of_puzzles) 
          + "  Nodes Expanded: " + str(sum(md_node) / num_of_puzzles))
    
    print("Misplaced:\n" + "Time: " + str(round(sum(mp_time) / num_of_puzzles, 5)) 
          + "  Solution Length: " + str(sum(mp_len) / num_of_puzzles) 
          + "  Nodes Expanded: " + str(sum(mp_node) / num_of_puzzles))
    
    print("Combined:\n" + "Time: " + str(round(sum(mx_time) / num_of_puzzles, 5)) 
          + "  Solution Length: " + str(sum(mx_len) / num_of_puzzles) 
          + "  Nodes Expanded: " + str(sum(mx_node) / num_of_puzzles))
    return



###########################################################
###########################################################
######
# q4a
#
# class for 2x2 cube problem
class Cube(Problem):
    
    # constructor
    def __init__(self, initial): 
        # for calculate h fast
        self.h_value = {4:4, 3:2, 2:1, 1:0}
        super().__init__(initial)
    
    # all actions
    def actions(self, state):
        return ["F1_CLOCKWISE", 
                "F1_COUNTERCLOCKWISE",
                "F2_CLOCKWISE", 
                "F2_COUNTERCLOCKWISE",
                "F3_CLOCKWISE", 
                "F3_COUNTERCLOCKWISE"]
                # "F4_CLOCKWISE",
                # "F4_COUNTERCLOCKWISE",
                # "F5_CLOCKWISE",
                # "F5_COUNTERCLOCKWISE",
                # "F6_CLOCKWISE", 
                # "F6_COUNTERCLOCKWISE"]
    
    ## fi_c for turn facet i clockwise and return the result state
    ## fi_cc for turn facet i counterclockwise and return the result state
    ## 1 <= i <= 6
    # facet 1 clockwise
    def f1_c(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        
        # update f1
        new_state[0][0] = state[0][2]
        new_state[0][1] = state[0][0]
        new_state[0][2] = state[0][3]
        new_state[0][3] = state[0][1]
        
        # update f2
        new_state[1][0] = state[2][0]
        new_state[1][1] = state[2][1]
        
        #update f3
        new_state[2][0] = state[3][0]
        new_state[2][1] = state[3][1]
        
        #update f4
        new_state[3][0] = state[5][3]
        new_state[3][1] = state[5][2]
        
        #update f6
        new_state[5][2] = state[1][1]
        new_state[5][3] = state[1][0]
        
        return new_state

    # facet 1 anticlockwise
    def f1_cc(self,state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
    
        # update f1
        new_state[0][0] = state[0][1]
        new_state[0][1] = state[0][3]
        new_state[0][2] = state[0][0]
        new_state[0][3] = state[0][2]
        
        # update f2
        new_state[1][0] = state[5][3]
        new_state[1][1] = state[5][2]
        
        # update f3
        new_state[2][0] = state[1][0]
        new_state[2][1] = state[1][1]
        
        # update f4
        new_state[3][0] = state[2][0]
        new_state[3][1] = state[2][1]
        
        # update f6
        new_state[5][2] = state[3][1]
        new_state[5][3] = state[3][0]
        
        return new_state

    # facet 2 clockwise
    def f2_c(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        
        # update f2
        new_state[1][0] = state[1][2]
        new_state[1][1] = state[1][0]
        new_state[1][2] = state[1][3]
        new_state[1][3] = state[1][1]
        
        # update f1
        new_state[0][0] = state[5][0]
        new_state[0][2] = state[5][2]
        
        #update f3
        new_state[2][0] = state[0][0]
        new_state[2][2] = state[0][2]
        
        #update f5
        new_state[4][0] = state[2][0]
        new_state[4][2] = state[2][2]
        
        #update f6
        new_state[5][0] = state[4][0]
        new_state[5][2] = state[4][2]
        
        return new_state

    # facet 2 anticlockwise
    def f2_cc(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        # update f2
        new_state[1][0] = state[1][1]
        new_state[1][1] = state[1][3]
        new_state[1][2] = state[1][0]
        new_state[1][3] = state[1][2]
        
        # update f1
        new_state[0][0] = state[2][0]
        new_state[0][2] = state[2][2]
        
        #update f3
        new_state[2][0] = state[4][0]
        new_state[2][2] = state[4][2]
        
        #update f5
        new_state[4][0] = state[5][0]
        new_state[4][2] = state[5][2]
        
        #update f6
        new_state[5][0] = state[0][0]
        new_state[5][2] = state[0][2]
        
        return new_state
    
    # facet 3 clockwise
    def f3_c(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]

        # update f3
        new_state[2][0] = state[2][2]
        new_state[2][1] = state[2][0]
        new_state[2][2] = state[2][3]
        new_state[2][3] = state[2][1]
        
        # update f1
        new_state[0][2] = state[1][3]
        new_state[0][3] = state[1][1]
        
        # update f2
        new_state[1][1] = state[4][0]
        new_state[1][3] = state[4][1]
        
        # update f4
        new_state[3][0] = state[0][2]
        new_state[3][2] = state[0][3]
        
        # update f5
        new_state[4][0] = state[3][2]
        new_state[4][1] = state[3][0]
        
        return new_state

    # facet 3 anticlockwise
    def f3_cc(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        # update f3
        new_state[2][0] = state[2][1]
        new_state[2][1] = state[2][3]
        new_state[2][2] = state[2][0]
        new_state[2][3] = state[2][2]
        
        # update f1
        new_state[0][2] = state[3][0]
        new_state[0][3] = state[3][2]
        
        # update f2
        new_state[1][1] = state[0][3]
        new_state[1][3] = state[0][2]
        
        # update f4
        new_state[3][0] = state[4][1]
        new_state[3][2] = state[4][0]
        
        # update f5
        new_state[4][0] = state[1][1]
        new_state[4][1] = state[1][3]
        return new_state
    
    # facet 4 clockwise
    def f4_c(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        
        # update f4
        new_state[3][0] = state[3][2]
        new_state[3][1] = state[3][0]
        new_state[3][2] = state[3][3]
        new_state[3][3] = state[3][1]
        
        # update f1
        new_state[0][1] = state[2][1]
        new_state[0][3] = state[2][3]
        
        #update f3
        new_state[2][1] = state[4][1]
        new_state[2][3] = state[4][3]
        
        #update f5
        new_state[4][1] = state[5][1]
        new_state[4][3] = state[5][3]
        
        #update f6
        new_state[5][1] = state[0][1]
        new_state[5][3] = state[0][3]

        return new_state

    # facet 4 anticlockwise
    def f4_cc(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        # update f4
        new_state[3][0] = state[3][1]
        new_state[3][1] = state[3][3]
        new_state[3][2] = state[3][0]
        new_state[3][3] = state[3][2]
        
        # update f1
        new_state[0][1] = state[5][1]
        new_state[0][3] = state[5][3]
        
        #update f3
        new_state[2][1] = state[0][1]
        new_state[2][3] = state[0][3]
        
        #update f5
        new_state[4][1] = state[2][1]
        new_state[4][3] = state[2][3]
        
        #update f6
        new_state[5][1] = state[4][1]
        new_state[5][3] = state[4][3]
        return new_state 
    
    # facet 5 clockwise
    def f5_c(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        
        # update f5
        new_state[4][0] = state[4][2]
        new_state[4][1] = state[4][0]
        new_state[4][2] = state[4][3]
        new_state[4][3] = state[4][1]
        
        # update f2
        new_state[1][2] = state[5][1]
        new_state[1][3] = state[5][0]
        
        #update f3
        new_state[2][2] = state[1][2]
        new_state[2][3] = state[1][3]
        
        #update f4
        new_state[3][2] = state[2][2]
        new_state[3][3] = state[2][3]
        
        #update f6
        new_state[5][0] = state[3][3]
        new_state[5][1] = state[3][2]
            
        return new_state

    # facet 5 anticlockwise
    def f5_cc(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        # update f5
        new_state[4][0] = state[4][1]
        new_state[4][1] = state[4][3]
        new_state[4][2] = state[4][0]
        new_state[4][3] = state[4][2]
        
        # update f2
        new_state[1][2] = state[2][2]
        new_state[1][3] = state[2][3]
        
        #update f3
        new_state[2][2] = state[3][2]
        new_state[2][3] = state[3][3]
        
        #update f4
        new_state[3][2] = state[5][1]
        new_state[3][3] = state[5][0]
        
        #update f6
        new_state[5][0] = state[1][3]
        new_state[5][1] = state[1][2]
        return new_state 
    
    # facet 6 clockwise
    def f6_c(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]

        # update f6
        new_state[5][0] = state[5][2]
        new_state[5][1] = state[5][0]
        new_state[5][2] = state[5][3]
        new_state[5][3] = state[5][1]
        
        # update f1
        new_state[0][0] = state[3][1]
        new_state[0][1] = state[3][3]
        
        #update f2
        new_state[1][0] = state[0][1]
        new_state[1][2] = state[0][0]
        
        #update f4
        new_state[3][1] = state[4][3]
        new_state[3][3] = state[4][2]
        
        #update f5
        new_state[4][2] = state[1][0]
        new_state[4][3] = state[1][2]

        return new_state

    # facet 6 anticlockwise
    def f6_cc(self, state):
        new_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4]), list(state[5])]
        # update f5
        new_state[5][0] = state[5][1]
        new_state[5][1] = state[5][3]
        new_state[5][2] = state[5][0]
        new_state[5][3] = state[5][2]
        
        # update f1
        new_state[0][0] = state[1][2]
        new_state[0][1] = state[1][0]
        
        #update f2
        new_state[1][0] = state[4][2]
        new_state[1][2] = state[4][3]
        
        #update f4
        new_state[3][1] = state[0][0]
        new_state[3][3] = state[0][1]
        
        #update f5
        new_state[4][2] = state[3][3]
        new_state[4][3] = state[3][1]
        return new_state 
    
    # return the result state based on input action
    def result(self, state, action):
        new_state = []
        
        if action == "F1_CLOCKWISE":
            
            new_state = self.f1_c(state)
        
        elif action == "F1_COUNTERCLOCKWISE":
            
            new_state = self.f1_cc(state)
            
        elif action == "F2_CLOCKWISE":
            
            new_state = self.f2_c(state)
            
        elif action == "F2_COUNTERCLOCKWISE":
            
            new_state = self.f2_cc(state)
            
        elif action == "F3_CLOCKWISE":
            
            new_state = self.f3_c(state)
        
        elif action == "F3_COUNTERCLOCKWISE":
            
            new_state = self.f3_cc(state)
            
        elif action == "F4_CLOCKWISE":
            
            new_state = self.f4_c(state)
        
        elif action == "F4_COUNTERCLOCKWISE":
            
            new_state = self.f4_cc(state)
            
        elif action == "F5_CLOCKWISE":
            
            new_state = self.f5_c(state)
        
        elif action == "F5_COUNTERCLOCKWISE":
            
            new_state = self.f5_cc(state)
        
        elif action == "F6_CLOCKWISE":

            new_state = self.f6_c(state)
        
        elif action == "F6_COUNTERCLOCKWISE":
            
            new_state = self.f6_cc(state)
        
        # for i in range(len(new_state)):
        #     new_state[i] = tuple(new_state[i])
        # return tuple(new_state)
        return tuple(tuple(sub) for sub in new_state)
    
    # check if the state is a goal state
    def goal_test(self, state):

        for i in state:
            if (len(set(i))) != 1:
                return False
        
        return True
    
    # h function
    def h(self,node):
        sum = 0
        for i in node.state:
            sum += self.h_value[len(set(i))]
        return sum

        
def q4(initial_state):
    
    if len(initial_state) != 6:
        print("Invalid number of facets")
        return
    
    for i in range(len(initial_state)):
        if len(initial_state[i]) != 4:
            print("Invalid number of colors for facet " + str(i + 1))
            return
    
    print("Cube colors:")
    for i in range(6):
        for j in range(4):
            print(initial_state[i][j], end = " ", sep = "")
        print()
    
    cube = Cube(initial_state)
    node, num_of_expanded = astar_search(cube, 3)
    print("\nResult colors:\n", node.state)
    print("Nodes explored: ", num_of_expanded)
    print("Answer depth: ", len(node.solution()))
    print("\nSolution:")
    for i in range(len(node.solution())):
        print(node.solution()[i])

    return

###########################################################
## Test q3a
print("q3_a:")
print("Random solvable initial state")
puzzle = make_rand_StagePuzzle()
print(puzzle.initial)
print("\n")


## Test q3b
print("q3_b:")
print("display (0, 3, 2, 1, 8, 7, 4, 6, 5, 9)")
display((0, 3, 2, 1, 8, 7, 4, 6, 5, 9))
print("\n")


## Test q3c
print("q3_c:")
# q3_c(8)
print("Please remove the commented-out q3_c(8) to test 8 random StagePuzzle instances and their statistics")
print("Below is just a test of one of professor's examples")
state = (1, 6, 2, 4, 8, 9, 0, 3, 7, 5)
puzzle = StagePuzzle(state)
print(puzzle.initial)
print_stat(puzzle, 1)
print_stat(puzzle, 0)
print_stat(puzzle, 2)
print("\n")


## Test q4a
print("q4_a:")
print("Tested with professor's example")
initial_state = ((4, 4, 2, 2), (1, 3, 5, 6), (1, 1, 5, 5), (6, 3, 6, 3), (4, 2, 2, 4), (3, 1, 6, 5))
q4(initial_state)
