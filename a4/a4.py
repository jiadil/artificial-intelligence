# Class Factor
class Factor:
    def __init__(self, vars, table):
        self.vars = vars
        self.table = table

    # Operation: assign a variable
    def assign(self, vname, val):
        index = self.vars.index(vname)
        self.table = [x for x in self.table if x[index] == val]
        for row in self.table:
            del row[index]
        self.vars.remove(vname)
    
    # Operation: Sum out a variable
    def SumOut(self, vaname):
        index = self.vars.index(vaname)
        self.vars.remove(vaname)
        for row in self.table:
            del row[index]
        for r1 in self.table:
            tmp = self.table.copy()
            tmp.remove(r1)
            for r2 in tmp:
                if r1[:-1] == r2[:-1]:
                    r1[-1] = round(r1[-1] + r2[-1], 10)
                    del self.table[self.table.index(r2)]

# Bayesian Network
class BN:
    def __init__(self, factors):
        self.factors = factors
    
    # Variable Elimination
    def VE(self, query_var, evd_var, query_var_val, evd_var_val):
        
        # Elimination Ordering
        elim_order = ["E", "D", "HD", "Hb", "BP", "CP"]
        const = []
        tmp = set()
        for i in query_var:
            elim_order.remove(i)

        # Assign all evidence variables
        if len(evd_var) > 0:
            for i in range(len(evd_var)):
                for t in self.factors:
                    if evd_var[i] in t.vars:
                        t.assign(evd_var[i], evd_var_val[i])
                        if len(t.vars) == 0:
                            const.append(t.table[0][0])
                            tmp.add(t)
            for i in evd_var:
                elim_order.remove(i)
        self.factors -= tmp
        
        # summation         
        for v in elim_order:
            fs = set()
            for f in self.factors:
                if v in f.vars:
                    fs.add(f)
            self.factors -= fs
            
            # multiplication
            while len(fs) > 1:
                f1 = fs.pop()
                f2 = fs.pop()
                f3 = mult(f1, f2)
                fs.add(f3)
            f = fs.pop()
            f.SumOut(v)
            self.factors.add(f)
        
        # final factor
        final_f = self.factors.pop()
        if len(const) > 0:
            for row in final_f.table:
                for num in const:
                    row[-1] = round(row[-1] * num, 10)
        sum = 0
        
        # normalize
        for row in final_f.table:
            sum += row[-1]
        if sum != 1:
            for row in final_f.table:
                row[-1] = round(row[-1] / sum, 10)
                
        # result row
        print("Result: ")
        for row in final_f.table:
            equal = True
            for v in query_var:
                if row[final_f.vars.index(v)] != query_var_val[query_var.index(v)]:
                    equal = False
            if equal:
                print(row[-1])

# Operation: mult 2 factors
def mult(f1, f2):
    
    # get common variables
    common = []
    for i in f1.vars:
        if i in f2.vars:
            common.append(i)

    # get new variables
    new_vars = f1.vars.copy()
    for i in f2.vars:
        if i not in common:
            new_vars.append(i)
            
    # get new table
    new_table = []
    for r1 in f1.table:
        for r2 in f2.table:
            equal = True
            for v in common:
                if r1[f1.vars.index(v)] != r2[f2.vars.index(v)]:
                    equal = False
            if equal:
                new_row = r1[:-1]
                for i in range(len(r2) - 1):
                    if f2.vars[i] not in common:
                        new_row.append(r2[i])
                new_row.append(round(r1[-1] * r2[-1], 10))
                new_table.append(new_row)
    
    # return new factor
    return Factor(new_vars, new_table)

# Truth Table: P(E)     
var_E = ["E"]
table_E = [["Yes", 0.7],
           ["No", 0.3]]

# Truth Table: P(D)   
var_D = ["D"]
table_D = [["Healthy", 0.25],
           ["Unhealthy", 0.75]]

# Truth Table: P(HD| E, D)   
var_HD = ["E", "D", "HD"]                    
table_HD = [["Yes", "Healthy", "Yes", 0.25],
         ["Yes", "Healthy", "No", 0.75],
         ["Yes", "Unhealthy", "Yes", 0.45],
         ["Yes", "Unhealthy", "No", 0.55],
         ["No", "Healthy", "Yes", 0.55],
         ["No", "Healthy", "No", 0.45], 
         ["No", "Unhealthy", "Yes", 0.75], 
         ["No", "Unhealthy", "No", 0.25]]

# Truth Table: P(Hb| D)   
var_Hb = ["D", "Hb"]
table_Hb = [["Healthy", "Yes", 0.2],
            ["Healthy", "No", 0.8],
            ["Unhealthy", "Yes", 0.85], 
            ["Unhealthy", "No", 0.15]]

# Truth Table: P(BP| HD)   
var_BP = ["HD", "BP"]
table_BP = [["Yes", "High", 0.85],
      ["Yes", "Low", 0.15],
      ["No", "High", 0.2],
      ["No", "Low", 0.8]]

# Truth Table: P(CP| HD, Hb)   
var_CP = ["HD", "Hb", "CP"]
table_CP = [["Yes", "Yes", "Yes", 0.8],
            ["Yes", "Yes", "No", 0.2],
            ["Yes", "No", "Yes", 0.6],
            ["Yes", "No", "No", 0.4],
            ["No", "Yes", "Yes", 0.4],
            ["No", "Yes", "No", 0.6],
            ["No", "No", "Yes", 0.1],
            ["No", "No", "No", 0.9]]

# all tables
tables = {Factor(var_E, table_E), Factor(var_D, table_D), Factor(var_HD, table_HD),
          Factor(var_Hb, table_Hb), Factor(var_BP, table_BP), Factor(var_CP, table_CP)}

# create Bayesian Network
bn = BN(tables)

# ask for input
query_var = input("Query Variable: ")
evd_var = input("Evidence Variable: ")
query_var_val = input("Query Variable Value: ")
evd_var_val = input("Evidence Variable Value: ")
query_var = query_var.split(", ")
if query_var[0] == '':
    query_var = []
evd_var = evd_var.split(", ")
if evd_var[0] == '':
    evd_var = []
query_var_val = query_var_val.split(", ")
if query_var_val[0] == '':
    query_var_val = []
evd_var_val = evd_var_val.split(", ")
if evd_var_val[0] == '':
    evd_var_val = []
    
# do VE
bn.VE(query_var, evd_var, query_var_val, evd_var_val)

