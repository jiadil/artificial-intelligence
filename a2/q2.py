"""
q2
A, B, C, D have the domain of {1, 2, 3, 4, 5, 6}, while E and F are in {1,2,3,4} domain. 
Constraints are: 
    A>1, 
    A-B=1, 
    B odd, 
    A≠C, 
    B+C=4, 
    B+D%3=0, 
    D even, 
    C≥E, 
    D-E odd, 
    E<F, 
    E+F even.
TODO: 
    Draw the search tree generated
    Print all solutions (models) found
    Print the number of failing consistency checks (i.e. failing branches) in the tree
"""

def consistency_check(state):
    '''This function determines whether the cpnstraints are met'''
    # A>1
    if state[0] and not (state[0] > 1):
        return False
    # A-B=1
    if state[1] and not (abs(state[0] - state[1]) == 1):
        return False
    # B odd
    if state[1] and not (state[1] % 2 == 1):
        return False
    # A≠C
    if state[2] and not (state[0] != state[2]):
        return False
    # B+C=4
    if state[2] and not (state[1] + state[2] == 4):
        return False
    # B+D%3=0
    if state[3] and not ((state[1] + state[3]) % 3 == 0):
        return False
    # D even
    if state[3] and not (state[3] % 2 == 0):
        return False
    # C≥E
    if state[4] and not ((state[2] >= state[4])):
        return False
    # D-E odd
    if state[4] and not ((state[3] - state[4]) % 2 == 1):
        return False
    # E<F
    if state[5] and not (state[4] < state[5]):
        return False
    # E+F even
    if state[5] and not ((state[4] + state[5]) % 2 == 0):
        return False
    return True

def assigned(state):
    '''This function returns the number of assigned variables of input state'''
    i = 0
    while i < 6 and state[i]:
        i += 1
    return i
 
def expand(state):
    '''This function returns all possible next states based on the input state'''
    n = assigned(state)
    # A, B, C, D have the domain of {1, 2, 3, 4, 5, 6}
    if n < 4:
        l1 = list(state)
        l2 = list(state)
        l3 = list(state)
        l4 = list(state)
        l5 = list(state)
        l6 = list(state)
        l1[n] = 6
        l2[n] = 5
        l3[n] = 4
        l4[n] = 3
        l5[n] = 2
        l6[n] = 1
        return (tuple(l1), tuple(l2), tuple(l3),
                tuple(l4), tuple(l5), tuple(l6))
    # E and F have the domain of {1,2,3,4}
    else:
        l1 = list(state)
        l2 = list(state)
        l3 = list(state)
        l4 = list(state)
        l1[n] = 4
        l2[n] = 3
        l3[n] = 2
        l4[n] = 1
        return (tuple(l1), tuple(l2),
                tuple(l3), tuple(l4))

def dfs(initial):
    '''This function performs dfs search for the given issue'''
    # init problem
    v = ["A", "B", "C", "D", "E", "F"]
    frontier = []
    frontier.extend(expand(initial))
    sol = []
    fail = []
    print_flag = False
    
    # dfs
    while frontier:
        cur_state = frontier.pop()
        n = assigned(cur_state)
        
        # format the search tree
        if print_flag:
            print_flag = False
            for i in range(n - 1):
                print("      ", sep = "", end = "", flush = True)
        # print the state status (X=t, y=t, etc.)
        print(v[n - 1] + " = " + str(cur_state[n - 1]), sep = "", end = "", flush = True)
        check = consistency_check(cur_state)
        
        # print Solution! if find a solution to the issue
        if check and n == 6:
            sol.append(cur_state)
            print(" Solution!")
            print_flag = True
        # check next state  
        elif check:
            print(" ", sep = "", end = "", flush = True)
            frontier.extend(expand(cur_state))
        # print Failure! if the current solution doesn't satisfy the constraints   
        else:
            fail.append(cur_state)
            print(" Failure!")
            print_flag = True
            
    return sol, fail

s, f = dfs((None, None, None, None, None, None))
print("\n\nSolutions in form of (A, B, C, D, E, F):")
for i in range(len(s)):
    print(s[i])
print("\n\nNumber of failed Branch: " + str(len(f)))
