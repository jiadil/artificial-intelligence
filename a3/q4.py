"""
q4
State:
    RLoc - Rob's location
        Domain: Coffee Shop (cs), Sam's office (off), Mail Room (mr), or Laboratory (lab)
    RHC - Rob has coffee.
        Domain: True or False
    SWC - Sam wants coffee.
        Domain: True or False
    MW - Mail is waiting.
        Domain: True or False
    RHM - Rob has mail.
        Domain: True or False
Actions:
    Move:
        Preconditions: {}
        Effects: {}
    PUC:
        Preconditions: {RLoc: cs; RHC: F}
        Effects: {RHC: T}
    DelC:
        Preconditions: {RLoc: off; RHC: T}
        Effects: {RHC: F; SWC: F}
    PUM:
        Preconditions: {RLoc: mr; MW: T; RHM: F}
        Effects: {RHM: T; MW: F}
    DelM:
        Preconditions: {RLoc: off; RHM: T}
        Effects: {RHM: F}
TODO: 
    reformulate the STRIPS model as CSPs with different horizons, and then solve them by implementing the Arc Consistency + Domain Splitting algorithm.
    The initial state is RLoc: off, RHC: F, SWC: T, MW: F, and RHM: T.
    The goal state is RLoc: off and SWC: F.
"""

class State:
    '''This class defines the 5 states (RLoc, RHC, SWC, MW, RHM)'''
    def __init__(self, RLoc, RHC, SWC, MW, RHM):
        self.RLoc = RLoc
        self.RHC = RHC
        self.SWC = SWC
        self.MW = MW
        self.RHM = RHM
    def Print(self):
        statesPrint = []
        statesPrint.append("RLoc: " + self.RLoc)
        statesPrint.append("RHC: " + self.RHC)
        statesPrint.append("SWC: " + self.SWC)
        statesPrint.append("MW: " + self.MW)
        statesPrint.append("RHM: " + self.RHM)
        return statesPrint

class MoveMcc():
    '''This class defines the action MoveMcc'''
    def __init__(self, currentState):
        self.state = currentState
        self.effects = self.Effects()
    def Effects(self):
        if self.state.RLoc == "cs":
            self.state.RLoc = "mr"
        elif self.state.RLoc == "mr":
            self.state.RLoc = "lab"
        elif self.state.RLoc == "lab":
            self.state.RLoc = "off"
        elif self.state.RLoc == "off":
            self.state.RLoc = "cs"
        return self.state

class PUC():
    '''This class defines the action PUC'''
    def __init__(self, currentState):
        self.state = currentState
        self.preconditions = self.Preconditions()
        self.apply = self.Apply()
        self.effects = self.Effects()
    def Preconditions(self):
        preconditions = []
        preconditions.append("RLoc: cs")
        preconditions.append("RHC: F")
        return preconditions
    def Apply(self):
        for i in self.preconditions:
            if i not in self.state.Print():
                return False
        return True
    def Effects(self):
        if self.apply:
            self.state.RHC = "T"
        return self.state

class DelC():
    '''This class defines the action DelC'''
    def __init__(self, currentState):
        self.state = currentState
        self.preconditions = self.Preconditions()
        self.apply = self.Apply()
        self.effects = self.Effects()
    def Preconditions(self):
        preconditions = []
        preconditions.append("RLoc: off")
        preconditions.append("RHC: T")
        return preconditions
    def Apply(self):
        for i in self.preconditions:
            if i not in self.state.Print():
                return False
        return True
    def Effects(self):
        if self.apply:
            self.state.RHC = "F"
            self.state.SWC = "F"
        return self.state

class PUM():
    '''This class defines the action PUM'''
    def __init__(self, currentState):
        self.state = currentState
        self.preconditions = self.Preconditions()
        self.apply = self.Apply()
        self.effects = self.Effects()
    def Preconditions(self):
        preconditions = []
        preconditions.append("RLoc: mr")
        preconditions.append("MW: T")
        preconditions.append("RHM: F")
        return preconditions
    def Apply(self):
        for i in self.preconditions:
            if i not in self.state.Print():
                return False
        return True
    def Effects(self):
        if self.apply:
            self.state.RHM = "T"
            self.state.MW = "F"
        return self.state

class DelM():
    '''This class defines the action DelM'''
    def __init__(self, currentState):
        self.state = currentState
        self.preconditions = self.Preconditions()
        self.apply = self.Apply()
        self.effects = self.Effects()
    def Preconditions(self):
        preconditions = []
        preconditions.append("RLoc: off")
        preconditions.append("RHM: T")
        return preconditions
    def Apply(self):
        for i in self.preconditions:
            if i not in self.state.Print():
                return False
        return True
    def Effects(self):
        if self.apply:
            self.state.RHM = "F"
        return self.state

def reachGoal(currentState, goal):
    '''This function determines if curret state has reached the goal'''
    for i in goal:
        if i not in currentState.Print():
            return False
    return True

def STRIPS(initial, goal):
    '''This function performs STRIPS'''
    # initialize varaibles and lists
    solved = False
    horizon = 0
    solActions = []
    solPath = []

    # loop
    while solved == False:
        # map STRIPS into CSP with horizon
        if PUC(initial).apply:
            PUC(initial).Effects()
            solActions.append("PUC")
            solPath.append(initial.Print())
        elif DelC(initial).apply:
            DelC(initial).Effects()
            solActions.append("DelC")
            solPath.append(initial.Print())
        ## nothing to do with mail in q4, ignore actions relevant to mail
        # elif PUM(initial).apply:
        #     PUM(initial).Effects()
        #     solActions.append("PUM")
        #     solPath.append(initial.Print())
        # elif DelM(initial).apply:
        #     DelM(initial).Effects()
        #     solActions.append("DelM")
        #     solPath.append(initial.Print())
        else:
            MoveMcc(initial)
            solActions.append("MoveMcc")
            solPath.append(initial.Print())
        
        # if found solution, stop loop
        if reachGoal(initial, goal):
            solved = True
            horizon = horizon + 1  
        # otherwise keeps looping
        else:
            horizon = horizon + 1
    
    # add MoveMc action to the list if it's applicable
    for i in range(horizon-2):
        if (solActions[i] == "MoveMcc"):
            if (solActions[i+1] == "MoveMcc") and (solActions[i+2] == "MoveMcc"):
                solActions[i] = "MoveMc"
                del solActions[i+1:i+3]
                del solPath[i:i+2]
                horizon -= 2

    # print horizon and all variable assignments in the solution
    for i in range(horizon):
        print("\nhorizon " + str(i+1) + ": ")
        print("Action: " + str(solActions[i]))
        print("Path: " + str(solPath[i]))
    print("\nSolution found in a horizon of " + str(i+1))
        
# set initial and goal state
initial = State("off","F","T","F","T")
goal = ["RLoc: off", "SWC: F"]

# print the results
print("initial state: ")
print(initial.Print())
plan = STRIPS(initial, goal)
print("\ngoal state: ")
print(goal)
