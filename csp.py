class CSP:
    def __init__(self, dict_graph, dict_color):

        # assigning the entered arguments to the object variable
        self.graph = dict_graph
        self.color_list = list(dict_color.keys())[:-1]

        # initializing the variables, domains, and constraints
        self.variables = self.graph.keys()
        self.domains = {v: self.color_list for v in self.variables}
        self.constraints = {(v1, v2): lambda x, y: x != y for v1, neighbors in self.graph.items() for v2 in neighbors}
        
        # initializing the variables
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

    # The MRV heuristic for finding the vertex 
    # that has smallest number of remaining values 
    # in its domain and not assigned yet by csp
    def min_remaining_values(self):
        return min([v for v in self.domains if v not in self.assignment], 
                   key = lambda v: len(self.domains[v]))

    # The LCV heuristic that takes a vertex as an input 
    # and return sorted list of its domain values
    def least_constraints_values(self,variable):
        # initializing the dictionary with zeros
        value_conf = {color: 0 for color in self.domains[variable]}

        # iterating over key of constraints 
        # and counting the number of conflicting 
        # values for each possible value of the given variable
        for v1, v2 in self.constraints:
            eq_var = v2
            if v1 == variable:
                eq_var = v1
            for value in self.domains[eq_var]:
                    value_conf[value]+=1
        
        # sorting the domains of that variable based on that ditionary
        return sorted(self.domains[variable], key = lambda v: value_conf[v])

    def backtracking(self,domains):
        # if length is equal it means we already have a solution
        if len(self.assignment) == len(self.domains):
            return self.assignment
        
        # calculate the mrv and lcv and assign them to the variable
        mrv_v = self.min_remaining_values()
        lcv_c = self.least_constraints_values(mrv_v)

        for value in lcv_c:
            if all(self.constraints[mrv_v, n](value, self.assignment[n]) 
                   for n in self.graph[mrv_v] if n in self.assignment):
                
                temp_domains = domains.copy()
                
                temp_domains[mrv_v] = [value]
                self.assignment[mrv_v] = value

                if self.ac3():
                    rec_res = self.backtracking(temp_domains)
                    if rec_res is not None:
                        return rec_res
                
                self.assignment.pop(mrv_v)

        return None
    
    # The method for printing the assigned colors of vertices
    def print_assignment(self):
        print("==========RESULT==========")

        # checking if coloring was possible or not
        if self.assignment is None:
            print("It is impossible to color the graph with {} number of color".format(len(self.color_list)))
            return
        
        # iterating over assignment dictionary and priting the vertex value and its color
        for vertex, color in self.assignment.items():
            print("\tThe color of vertex {} is {}".format(vertex,color))