import sys

class CSP:
    def __init__(self,dict_graph = None, color_list = None):
        self.graph = dict_graph
        self.color_list = color_list

        self.variables = self.graph.keys()
        self.domains = {v: color_list for v in self.variables}
        self.constraints = {(v1, v2): lambda x, y: x != y for v1, neighbors in self.graph.items() for v2 in neighbors}
        self.assignment = {}

    def ac3(self):
        queue = list(self.constraints.keys())
        while queue:
            v1, v2 = queue.pop()
            if self.remove_inconsistent_values(v1,v2):
                if len(self.domains[v1]) == 0:
                    return False
                for n in self.graph[v1]:
                    if n != v2:
                        queue.append((n, v1))
        return True

    def remove_inconsistent_values(self,v1,v2):
        removed = False
        for x in self.domains[v1]:
            if not any(self.constraints[v1, v2](x, y) for y in self.domains[v2]):
                self.domains[v1].remove(x)
                removed = True
        return removed

    def min_remaining_values(self):
        return min([v for v in self.domains if v not in self.assignment], 
                   key = lambda v: len(self.domains[v]))

    def least_constraints_values(self,variable):
        value_conf = {color: 0 for color in self.domains[variable]}

        for v1, v2 in self.constraints:
            main_var = v2
            if v1 == variable:
                main_var = v1
            
            for value in self.domains[main_var]:
                    value_conf[value]+=1
           
            # if v1 == variable:# and v2 not in self.domains[variable]:
            #     for value in self.domains[v2]:
            #         value_conf[value]+=1
            
            # elif v2 == variable:# and v1 not in self.domains[variable]:
            #     for value in self.domains[v1]:
            #         value_conf[value]+=1
        
        return sorted(self.domains[variable], key = lambda v: value_conf[v])

    def backtracking(self,domains):
        if len(self.assignment) == len(self.domains):
            return self.assignment
        
        v = self.min_remaining_values()

        #DEYIWILMELIDI
        for value in self.least_constraints_values(v):
            if all(self.constraints[v, neighbor](value, self.assignment[neighbor]) for neighbor in self.graph[v] if neighbor in self.assignment):
                self.assignment[v] = value
                temp_domains = domains.copy()
                temp_domains[v] = [value]
                
                if self.ac3():
                    result = self.backtracking(temp_domains)
                    if result is not None:
                        return result
                
                del self.assignment[v]

        return None