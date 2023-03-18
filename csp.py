class CSP:
    def __init__(self, dict_graph, dict_color):

        # assigning the entered arguments to the object variable
        self.graph = dict_graph
        self.color_list = list(dict_color.keys())[:-1]

        # initializing the variables, domains, and constraints
        self.variables = self.graph.keys()
        self.domains = {v: self.color_list for v in self.variables}
        self.constraints = {(v1, v2): lambda x, y: x != y for v1, 
                            neighbors in self.graph.items() for v2 in neighbors}
        
        # initializing the variables
        self.assignment = {}
        
    # the function to implement the ac-3 algorithm to enforce arc consistency
    def ac3(self):

        # create a queue of all the constraints between variables
        queue = list(self.constraints.keys())
        
        # while the queue is not empty
        while queue:

            # get the next constraint from the queue
            v1, v2 = queue.pop()

            # remove any inconsistent values between the two variables
            if self.remove_inconsistent_values(v1,v2):

                # if there is no value in v1 domain,
                # return false because we have a conflict
                if len(self.domains[v1]) == 0:
                    return False
                
                # append all constraints involving v1 to the queue
                for n in self.graph[v1]:
                    if n != v2:
                        queue.append((n, v1))

        # return true if we have make it through the queue without any conflicts
        return True

    # the method for removing the inconsistent values
    def remove_inconsistent_values(self,v1,v2):
        # initialize the flag with false boolean value
        removed = False
        
        # iterate over domains of v1
        for x in self.domains[v1]:
            # if there is no consistent value, removes the inconsistent value
            # and make the flag true
            
            if not any(self.constraints[v1, v2](x, y) for y in self.domains[v2]):
                self.domains[v1].remove(x)
                removed = True
        
        # return the flag
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

    # the backtracking algorithm for solving a csp
    def backtracking(self,domains):
        # if length is equal it means we already have a solution
        if len(self.assignment) == len(self.domains):
            return self.assignment
        
        # calculate the mrv and lcv and assign them to the variables
        mrv_v = self.min_remaining_values()
        lcv_c = self.least_constraints_values(mrv_v)

        # iterate over each value in lcv_v
        for value in lcv_c:
            
            # check if the value is consistent with current assignments
            if all(self.constraints[mrv_v, n](value, self.assignment[n]) 
                   for n in self.graph[mrv_v] if n in self.assignment):
                
                # copy the domains dictionary to avoid inplace changes
                temp_domains = domains.copy()
                
                # assign the value to the temporary domain and assignment dictionary
                temp_domains[mrv_v] = [value]
                self.assignment[mrv_v] = value

                # apply ac3 constraint propagation and recursive backtracking
                if self.ac3():
                    rec_res = self.backtracking(temp_domains)
                    if rec_res is not None:
                        return rec_res
                
                # delete the vertex value from the assignment
                self.assignment.pop(mrv_v)

        # return none if there is no solution
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