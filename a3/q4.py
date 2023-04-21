# constraints class consist of:
# scope: set of variables
# condition: function for evaluating constraint condition
# name
class Constraint():
    def __init__(self, scope, condition, name):
        self.scope = scope
        self.condition = condition
        self.name = name

# CSP class consist of:
# variables: dictionary of {variable name:variable domain}
# constraints: set of constraints
# var_to_const: dictionary of {variable name:involved constraint}
class CSP():
    def __init__(self, domain, constraints):
        self.variables = domain
        self.constraints = constraints
        self.var_to_const = {var:set() for var in self.variables}
        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

# CSP solver: solve a given CSP using AC + DS
class CSPsolvers():
    def __init__(self, csp):
        self.csp = csp
        self.solution = []
    
    # arc consistency
    def AC(self, csp):
        Tda = {(var, const) for const in csp.constraints
                for var in const.scope}
        while Tda:
            var, const = Tda.pop()
            related_var = [v for v in const.scope if v != var]
            new_domain = const.condition(var, related_var, csp.variables)
            if new_domain != csp.variables[var]:
                csp.variables[var] = new_domain
                for c in self.csp.var_to_const[var]:
                    if c != const:
                        for v in c.scope:
                            if v != var:
                                Tda.add((v, c))

    # domain splitting + AC
    def solve(self, csp):
        self.AC(csp)
        if any(len(csp.variables[v]) == 0 for v in csp.variables):
            return False
        elif all(len(csp.variables[v]) == 1 for v in csp.variables):
            self.solution.append({var:csp.variables[var] for var in csp.variables})
            return True
        else:
            selected_v = {v for v in csp.variables if len(csp.variables[v]) > 1}
            selected_v = selected_v.pop()
            split = len(csp.variables[selected_v]) // 2
            
            dom1 = set(list(csp.variables[selected_v])[:split])
            dom2 = csp.variables[selected_v] - dom1
            csp2 = CSP(csp.variables.copy(), csp.constraints.copy())
            csp.variables[selected_v] = dom1
            csp2.variables[selected_v] = dom2
            return self.solve(csp), self.solve(csp2)
    
    # trigger function
    def soln(self, csp):
        return self.solve(csp)

# condition function for constraint: precondition and effect of action Move
def con_move(var, related_var, domain):
    
    loc_before = []
    loc_after = []
    move = []
    new_domain = set()
    if "Move" in var:
        move = var
        v1 = related_var[0]
        v2 = related_var[1]
        if int(v1[-1]) > int(v2[-1]):
            loc_after = v1
            loc_before = v2
        else:
            loc_after = v2
            loc_before = v1
        for val in domain[move]:
            if val == "mc":
                if ("cs" in domain[loc_before] and "off" in domain[loc_after]) or\
                    ("off" in domain[loc_before] and "lab" in domain[loc_after]) or\
                    ("lab" in domain[loc_before] and "mr" in domain[loc_after]) or\
                    ("mr" in domain[loc_before] and "cs" in domain[loc_after]):
                    new_domain.add(val)
            elif val == "mcc":
                if ("off" in domain[loc_before] and "cs" in domain[loc_after]) or\
                    ("lab" in domain[loc_before] and "off" in domain[loc_after]) or\
                    ("mr" in domain[loc_before] and "lab" in domain[loc_after]) or\
                    ("cs" in domain[loc_before] and "mr" in domain[loc_after]):
                    new_domain.add(val)
            else:
                if ("off" in domain[loc_before] and "off" in domain[loc_after]) or\
                    ("lab" in domain[loc_before] and "lab" in domain[loc_after]) or\
                    ("mr" in domain[loc_before] and "mr" in domain[loc_after]) or\
                    ("cs" in domain[loc_before] and "cs" in domain[loc_after]):
                    new_domain.add(val)
    else:
        map = ["cs", "off", "lab", "mr"]
        v1 = var
        if "Move" in related_var[0]:
            move = related_var[0]
            v2 = related_var[1]
        else:
            move = related_var[1]
            v2 = related_var[0]
        if int(v1[-1]) > int(v2[-1]):
            loc_after = v1
            loc_before = v2
        else:
            loc_after = v2
            loc_before = v1
        if var == loc_before:
            for val in domain[loc_before]:
                index = map.index(val)
                if ("mc" in domain[move] and map[(index + 1) % 4] in domain[loc_after]) or\
                    ("mcc" in domain[move] and map[(index - 1) % 4] in domain[loc_after]) or\
                    ("nm" in domain[move] and val in domain[loc_after]):
                    new_domain.add(val)
        else:
            for val in domain[loc_after]:
                index = map.index(val)
                if ("mc" in domain[move] and map[(index - 1) % 4] in domain[loc_before]) or\
                    ("mcc" in domain[move] and map[(index + 1) % 4] in domain[loc_before]) or\
                    ("nm" in domain[move] and val in domain[loc_after]):
                    new_domain.add(val)
    return new_domain

# condition function for constraint: precondition of action PUC
def con_PUC_pre(var, related_var, domain):
    new_domain = set()
    if "RLoc" in var:
        loc = var
        puc = related_var[0]
        for val in domain[loc]:
            if (val == "cs" and True in domain[puc]) or\
                (val == "cs" and False in domain[puc]) or\
                (val != "cs" and False in domain[puc]):
                new_domain.add(val)
    else:
        loc = related_var[0]
        puc = var
        for val in domain[puc]:
            if (val == True and "cs" in domain[loc]) or\
                (val == False and len(domain[loc]) > 0):
                new_domain.add(val)
    
    return new_domain

# condition function for constraint: precondition of action DelC
def con_DelC_pre(var, related_var, domain):
    new_domain = set()
    loc = []
    rhc = []
    delc = []
    l = related_var.copy()
    l.append(var)
    for i in l:
        if "RLoc" in i:
            loc = i
        elif "RHC" in i:
            rhc = i
        else:
            delc = i
    if var == loc:
        for val in domain[loc]:
            if (val == "off" and True in domain[rhc] and len(domain[delc]) > 0) or\
                (val == "off" and False in domain[rhc] and False in domain[delc]) or\
                (val != "off" and len(domain[rhc]) > 0 and False in domain[delc]):
                new_domain.add(val)
    elif var == rhc:
        for val in domain[rhc]:
            if (val == True and "off" in domain[loc] and len(domain[delc]) > 0) or\
                (val == True and "off" not in domain[loc] and False in domain[delc]) or\
                (val == False and len(domain[loc]) > 0 and False in domain[delc]):
                new_domain.add(val)
    else:
        for val in domain[delc]:
            if (val == True and True in domain[rhc] and "off" in domain[loc]) or\
                (val == False and len(domain[rhc]) > 0 and len(domain[loc]) > 0):
                new_domain.add(val)
    return new_domain

# condition function for constraint: precondition of action PUM
def con_PUM_pre(var, related_var, domain):
    new_domain = set()
    pum = []
    loc = []
    mw = []
    l = related_var.copy()
    l.append(var)
    for i in l:
        if "PUM" in i:
            pum = i
        elif "RLoc" in i:
            loc = i
        else:
            mw = i
    if var == pum:
        for val in domain[pum]:
            if (val == True and "mr" in domain[loc] and True in domain[mw]) or\
                (val == False and len(domain[loc]) > 0 and len(domain[mw]) > 0):
                new_domain.add(val)
    elif var == loc:
        for val in domain[loc]:
            if (val == "mr" and True in domain[pum] and True in domain[mw]) or\
                (val == "mr" and False in domain[pum] and True in domain[mw]) or\
                (val == "mr" and False in domain[pum] and False in domain[mw]) or\
                (val != "mr" and False in domain[pum] and len(domain[mw]) > 0):
                new_domain.add(val)
    else:
        for val in domain[mw]:
            if (val == True and "mr" in domain[loc] and True in domain[pum]) or\
                (val == True and "mr" in domain[loc] and False in domain[pum]) or\
                (val == True and "mr" not in domain[loc] and False in domain[pum]) or\
                (val == False and len(domain[loc]) > 0 and False in domain[pum]):
                new_domain.add(val)
    return new_domain

# condition function for constraint: precondition of action DelM
def con_DelM_pre(var, related_var, domain):
    new_domain = set()
    loc = []
    rhm = []
    delm = []
    l = related_var.copy()
    l.append(var)
    for i in l:
        if "RLoc" in i:
            loc = i
        elif "RHM" in i:
            rhm = i
        else:
            delm = i
    if var == loc:
        for val in domain[loc]:
            if (val == "off" and True in domain[rhm] and len(domain[delm]) > 0) or\
                (val == "off" and False in domain[rhm] and False in domain[delm]) or\
                (val != "off" and len(domain[rhm]) > 0 and False in domain[delm]):
                new_domain.add(val)
    elif var == rhm:
        for val in domain[rhm]:
            if (val == True and "off" in domain[loc] and len(domain[delm]) > 0) or\
                (val == True and "off" not in domain[loc] and False in domain[delm]) or\
                (val == False and len(domain[loc]) > 0 and False in domain[delm]):
                new_domain.add(val)
    else:
        for val in domain[delm]:
            if (val == True and True in domain[rhm] and "off" in domain[loc]) or\
                (val == False and len(domain[loc]) > 0 and len(domain[rhm]) > 0):
                new_domain.add(val)
    return new_domain

# condition function for constraint: effct of action PUM
def con_PUM_eff(var, related_var, domain):
    new_domain = set()
    truth_table = {"mw_before":[True, True, False, False],
                   "pum":[True, False, True, False],
                   "mw_after":[False, True, False, False]}
    mw_before = []
    pum = []
    mw_after = []
    v1 = []
    v2 = []
    l = related_var.copy()
    l.append(var)
    for i in l:
        if "PUM" in i:
            pum = i
        elif "MW" in i and len(v1) == 0:
            v1 = i
        else:
            v2 = i
    if int(v1[-1]) > int(v2[-1]):
        mw_after = v1
        mw_before = v2
    else:
        mw_after = v2
        mw_before = v1

    if var == mw_before:
        for val in domain[mw_before]:
            for i in range(4):
                if val == truth_table["mw_before"][i] and\
                    truth_table["pum"][i] in domain[pum] and\
                    truth_table["mw_after"][i] in domain[mw_after]:
                    new_domain.add(val)
    elif var == pum:
        for val in domain[pum]:
            for i in range(4):
                if val == truth_table["pum"][i] and\
                    truth_table["mw_before"][i] in domain[mw_before] and\
                    truth_table["mw_after"][i] in domain[mw_after]:
                    new_domain.add(val)
    else:
        for val in domain[mw_after]:
            for i in range(4):
                if val == truth_table["mw_after"][i] and\
                    truth_table["pum"][i] in domain[pum] and\
                    truth_table["mw_before"][i] in domain[mw_before]:
                    new_domain.add(val)
    return new_domain

# condition function for constraint: effct of action DelM
def con_DelM_eff(var, related_var, domain):
    new_domain = set()
    truth_table = {"rhm_before":[True, True, True, True, False, False, False, False],
                   "delm":[True, True, False, False, True, True, False, False],
                   "pum":[True, False, True, False, True, False, True, False],
                   "rhm_after":[True, False,True, True, False, False, True, False]}
    rhm_before = []
    delm = []
    pum = []
    rhm_after = []
    v1 = []
    v2 = []
    l = related_var.copy()
    l.append(var)
    for i in l:
        if "DelM" in i:
            delm = i
        elif "PUM" in i:
            pum = i
        elif "RHM" in i and len(v1) == 0:
            v1 = i
        else:
            v2 = i
    if int(v1[-1]) > int(v2[-1]):
        rhm_after = v1
        rhm_before = v2
    else:
        rhm_after = v2
        rhm_before = v1
    if var == rhm_before:
        for val in domain[rhm_before]:
            for i in range(8):
                if val == truth_table["rhm_before"][i] and\
                    truth_table["delm"][i] in domain[delm] and\
                    truth_table["pum"][i] in domain[pum] and\
                    truth_table["rhm_after"][i] in domain[rhm_after]:
                    new_domain.add(val)
    elif var == delm:
        for val in domain[delm]:
            for i in range(8):
                if val == truth_table["delm"][i] and\
                    truth_table["rhm_before"][i] in domain[rhm_before] and\
                    truth_table["pum"][i] in domain[pum] and\
                    truth_table["rhm_after"][i] in domain[rhm_after]:
                    new_domain.add(val)
    elif var == pum:
        for val in domain[pum]:
            for i in range(8):
                if val == truth_table["pum"][i] and\
                    truth_table["rhm_before"][i] in domain[rhm_before] and\
                    truth_table["delm"][i] in domain[delm] and\
                    truth_table["rhm_after"][i] in domain[rhm_after]:
                    new_domain.add(val)
    else:
        for val in domain[rhm_after]:
            for i in range(8):
                if val == truth_table["rhm_after"][i] and\
                    truth_table["rhm_before"][i] in domain[rhm_before] and\
                    truth_table["delm"][i] in domain[delm] and\
                    truth_table["pum"][i] in domain[pum]:
                    new_domain.add(val)
    return new_domain

# condition function for constraint: effct of action PUC
def con_PUC_eff(var, related_var, domain):
    truth_table = {"rhc_before":[True, True, True, True, False, False, False, False], 
                   "delc":[True, True, False, False, True, True, False, False], 
                   "puc":[True, False, True, False, True, False, True, False],
                   "rhc_after":[True, False, True, True, False, False, True, False]}
    new_domain = set()
    l = related_var.copy()
    l.append(var)
    rhc_before = []
    delc = []
    puc = []
    rhc_after = []
    v1 = []
    v2 = []
    for i in l:
        if "DelC" in i:
            delc = i
        elif "PUC" in i:
            puc = i
        elif "RHC" in i and len(v1) == 0:
            v1 = i
        else:
            v2 = i
    if int(v1[-1]) > int(v2[-1]):
        rhc_after = v1
        rhc_before = v2
    else:
        rhc_after = v2
        rhc_before = v1
    if var == rhc_before:
        for val in domain[rhc_before]:
            for i in range(8):
                if val == truth_table["rhc_before"][i] and\
                    truth_table["delc"][i] in domain[delc] and\
                    truth_table["puc"][i] in domain[puc] and\
                    truth_table["rhc_after"][i] in domain[rhc_after]:
                    new_domain.add(val)
    elif var == delc:
        for val in domain[delc]:
            for i in range(8):
                if val == truth_table["delc"][i] and\
                    truth_table["rhc_before"][i] in domain[rhc_before] and\
                    truth_table["puc"][i] in domain[puc] and\
                    truth_table["rhc_after"][i] in domain[rhc_after]:
                    new_domain.add(val)
    elif var == puc:
        for val in domain[puc]:
            for i in range(8):
                if val == truth_table["puc"][i] and\
                    truth_table["delc"][i] in domain[delc] and\
                    truth_table["rhc_before"][i] in domain[rhc_before] and\
                    truth_table["rhc_after"][i] in domain[rhc_after]:
                    new_domain.add(val)
    else:
        for val in domain[rhc_after]:
            for i in range(8):
                if val == truth_table["rhc_after"][i] and\
                    truth_table["delc"][i] in domain[delc] and\
                    truth_table["puc"][i] in domain[puc] and\
                    truth_table["rhc_before"][i] in domain[rhc_before]:
                    new_domain.add(val)
    return new_domain

# condition function for constraint: effct of action DelC
def con_DelC_eff(var, related_var, domain):
    truth_table = {"swc_before":[True, True, False, False], 
                   "delc":[True, False, True, False], 
                   "swc_after":[False, True, False, False]}
    new_domain = set()
    l = related_var.copy()
    l.append(var)
    delc = []
    swc_before = []
    swc_after = []
    v1 = []
    v2 = []
    for i in l:
        if "DelC" in i:
            delc = i
        elif "SWC" in i and len(v1) == 0:
            v1 = i
        else:
            v2 = i
    if int(v1[-1]) > int(v2[-1]):
        swc_after = v1
        swc_before = v2
    else:
        swc_after = v2
        swc_before = v1
    if var == swc_before:
        for val in domain[swc_before]:
            for i in range(4):
                if val == truth_table["swc_before"][i] and\
                    truth_table["delc"][i] in domain[delc] and\
                    truth_table["swc_after"][i] in domain[swc_after]:
                    new_domain.add(val)
    elif var == delc:
        for val in domain[delc]:
            for i in range(4):
                if val == truth_table["delc"][i] and\
                    truth_table["swc_before"][i] in domain[swc_before] and\
                    truth_table["swc_after"][i] in domain[swc_after]:
                    new_domain.add(val)
    else:
        for val in domain[swc_after]:
            for i in range(4):
                if val == truth_table["swc_after"][i] and\
                    truth_table["swc_before"][i] in domain[swc_before] and\
                    truth_table["delc"][i] in domain[delc]:
                    new_domain.add(val)
    return new_domain
    
# condition function for constraint: mutex constraint(only 1 action per time step)
def mutex(var, related_var, domain):
    new_domain = set()
    truth_table = {"move":["mc", "mcc", "nm", "nm", "nm", "nm"], 
                   "puc":[False, False, True, False, False, False],
                   "delc":[False, False, False, True, False, False],
                   "pum":[False, False, False, False, True, False],
                   "delm":[False, False, False, False, False, True]}
    l = related_var.copy()
    l.append(var)
    move = []
    puc = []
    delc = []
    pum = []
    delm = []
    for i in l:
        if "Move" in i:
            move = i
        elif "PUC" in i:
            puc = i
        elif "DelC" in i:
            delc = i
        elif "PUM" in i:
            pum = i
        else:
            delm = i
    if var == move:
        for val in domain[move]:
            for i in range(6):
                if val == truth_table["move"][i] and\
                    truth_table["puc"][i] in domain[puc] and\
                    truth_table["delc"][i] in domain[delc] and\
                    truth_table["pum"][i] in domain[pum] and\
                    truth_table["delm"][i] in domain[delm]:
                    new_domain.add(val)
    elif var == puc:
        for val in domain[puc]:
            for i in range(6):
                if val == truth_table["puc"][i] and\
                    truth_table["move"][i] in domain[move] and\
                    truth_table["delc"][i] in domain[delc] and\
                    truth_table["pum"][i] in domain[pum] and\
                    truth_table["delm"][i] in domain[delm]:
                    new_domain.add(val)
    elif var == delc:
        for val in domain[delc]:
            for i in range(6):
                if val == truth_table["delc"][i] and\
                    truth_table["move"][i] in domain[move] and\
                    truth_table["puc"][i] in domain[puc] and\
                    truth_table["pum"][i] in domain[pum] and\
                    truth_table["delm"][i] in domain[delm]:
                    new_domain.add(val)
    elif var == pum:
        for val in domain[pum]:
            for i in range(6):
                if val == truth_table["pum"][i] and\
                    truth_table["move"][i] in domain[move] and\
                    truth_table["puc"][i] in domain[puc] and\
                    truth_table["delc"][i] in domain[delc] and\
                    truth_table["delm"][i] in domain[delm]:
                    new_domain.add(val)
    else:
        for val in domain[delm]:
            for i in range(6):
                if val == truth_table["delm"][i] and\
                    truth_table["move"][i] in domain[move] and\
                    truth_table["puc"][i] in domain[puc] and\
                    truth_table["delc"][i] in domain[delc] and\
                    truth_table["pum"][i] in domain[pum]:
                    new_domain.add(val)
    return new_domain

# solve the STRIPS problem by converting it to CSP and using AC + DS
def solve_STRIPS(initial, goal):
    h = 0
    solve = False
    solution = []
    while not solve:
        if h == 0:
            if all(initial[v].issubset(goal[v]) for v in goal):
                solve = True
                solution.append(initial)
            else:
                h += 1
        else:
            # convert to CSP
            csp = init(initial, goal, h)
            sol = CSPsolvers(csp)

            # solve it by AC + DS
            if sol.soln(csp):
                solve = True
                solution = sol.solution
            else:
                h += 1
    
    # solution
    print("Horizen: " + str(h))
    for i in solution[0]:
        print(i, solution[0][i])
        
# construct the initial CSP
def init(initial, goal, h):
    boolean = {True, False}
    
    # feature variables
    domain1 = {"RLoc":{"cs", "off", "lab", "mr"}, "RHC":boolean, "SWC":boolean, "MW":boolean, "RHM":boolean}
    
    # action variables
    # nm for Not Move
    domain2 = {"Move":{"mc", "mcc", "nm"}, "PUC":boolean, "DelC":boolean, "PUM":boolean, "DelM":boolean}
    domain = {}
    constraints = set()
    
    # define a variable for each feature in every time step from 0 to h
    for i in range(h + 1):
        for v in domain1:
            domain[v + "_" + str(i)] = domain1[v].copy()
            
    # define a variable for each action and add constraints in every time step from 0 to h - 1
    for i in range(h):
        for v in domain2:
            domain[v + "_" + str(i)] = domain2[v].copy()  
        constraints.add(Constraint({"RLoc"+"_"+str(i), "Move"+"_"+str(i), "RLoc"+"_"+str(i + 1)}, con_move, "move_condition"))
        constraints.add(Constraint({"RLoc"+"_"+str(i), "PUC"+"_"+str(i)}, con_PUC_pre, "con_PUC_pre"))
        constraints.add(Constraint({"RLoc"+"_"+str(i), "RHC"+"_"+str(i), "DelC"+"_"+str(i)}, con_DelC_pre, "con_DelC_pre"))
        constraints.add(Constraint({"RLoc"+"_"+str(i), "MW"+"_"+str(i), "PUM"+"_"+str(i)}, con_PUM_pre, "con_PUM_pre"))
        constraints.add(Constraint({"RLoc"+"_"+str(i), "RHM"+"_"+str(i), "DelM"+"_"+str(i)}, con_DelM_pre, "con_DelM_pre"))
        constraints.add(Constraint({"RHC"+"_"+str(i), "PUC"+"_"+str(i), "RHC"+"_"+str(i + 1), "DelC"+"_"+str(i)}, con_PUC_eff, "con_PUC_eff"))
        constraints.add(Constraint({"SWC"+"_"+str(i + 1), "DelC"+"_"+str(i), "SWC"+"_"+str(i)}, con_DelC_eff, "con_DelC_eff"))
        constraints.add(Constraint({"MW"+"_"+str(i), "MW"+"_"+str(i + 1), "PUM"+"_"+str(i)}, con_PUM_eff, "con_PUM_eff"))
        constraints.add(Constraint({"RHM"+"_"+str(i), "PUM"+"_"+str(i), "RHM"+"_"+str(i + 1), "DelM"+"_"+str(i)}, con_DelM_eff, "con_DelM_eff"))
        constraints.add(Constraint({"Move"+"_"+str(i), "PUC"+"_"+str(i), "DelC"+"_"+str(i), "PUM"+"_"+str(i), "DelM"+"_"+str(i)}, mutex, "mutex"))
        
    # add initial constraint
    for v in initial:
        domain[v+"_0"] = initial[v]
        
    # add goal constraint
    for v in goal:
        domain[v+"_"+str(h)] = goal[v]
    return CSP(domain, constraints)


initial = {"RLoc":{"off"}, "RHC":{False}, "SWC":{True}, "MW":{False}, "RHM":{True}}
goal = {"RLoc":{"off"}, "SWC":{False}}
solve_STRIPS(initial, goal)
