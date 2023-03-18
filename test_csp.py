import unittest
from csp import CSP

class TestCSP(unittest.TestCase):
    
    # test output of backtracking if everything is valid
    def test_valid_graph_and_color(self):
        test_graph = {1 : {2,3}, 2 : {1,3}, 3 : {1,2}}
        
        test_dict_colors = {'red': (255,0,0), 'blue': (0,0,255), 
                            'green': (0,255,0), 'default': (0,0,0)}
        
        csp = CSP(test_graph, test_dict_colors)
        assert csp.backtracking(csp.domains) != None

    # test output of backtracking if color dictionary is invalid
    def test_invalid_color_dictionary(self):
        test_graph = {1 : {2,3}, 2 : {1,3}, 3 : {1,2}}
        
        test_dict_colors = {'red': (255,0,0), 'blue': (0,0,255), 'default': (0,0,0)}
        
        csp = CSP(test_graph, test_dict_colors)
        assert csp.backtracking(csp.domains) == None

    # test output of backtracking if we only have one vertex
    def test_graph_one_vertex(self):
        test_graph = {1 : {}}
        
        test_dict_colors = {'red': (255,0,0), 'blue': (0,0,255), 
                            'green': (0,255,0), 'default': (0,0,0)}
        
        csp = CSP(test_graph, test_dict_colors)
        assert csp.backtracking(csp.domains) != None
        
    # test output of backtracking if graph is consist of multiple components
    def test_graph_multi_components(self):
        test_graph = {1 : {2}, 2 : {1}, 3: {}}
        test_dict_colors = {'red': (255,0,0), 'blue': (0,0,255), 
                    'green': (0,255,0), 'default': (0,0,0)}
        
        csp = CSP(test_graph, test_dict_colors)
        assert csp.backtracking(csp.domains) != None

    # test ac3 with consistent values
    def test_ac3_consistent_values(self):
        test_graph = {1 : {2}, 2 : {1,3}, 3 : {2}}
        test_dict_colors = {'red': (255,0,0), 'blue': (0,0,255), 
                            'green': (0,255,0), 'default': (0,0,0)}
        csp = CSP(test_graph, test_dict_colors)
        
        csp.domains[1] = ['red']
        csp.domains[2] = ['green', 'blue']
        csp.domains[3] = ['green']
        assert csp.ac3() == True

    # test ac3 with inconsistent values
    def test_csp_inconsistent_values(self):
        test_graph = {1 : {2}, 2 : {1,3}, 3 : {2}}
        test_dict_colors = {'red': (255,0,0), 'blue': (0,0,255), 
                            'green': (0,255,0), 'default': (0,0,0)}
        csp = CSP(test_graph, test_dict_colors)
        
        csp.domains[1] = ['red']
        csp.domains[2] = ['red','green']
        csp.domains[3] = ['green']

        assert csp.ac3() == False

    # test mrv function
    def test_mrv(self):
        test_graph = {1 : {2}, 2 : {1,3}, 3 : {2}}
        test_dict_colors = {'red': (255,0,0), 'blue': (0,0,255), 
                            'green': (0,255,0), 'default': (0,0,0)}
        csp = CSP(test_graph, test_dict_colors)
        
        csp.domains[1] = ['red', 'green']
        csp.domains[2] = ['red']
        csp.domains[3] = ['green']

        assert csp.min_remaining_values() == 2

    # test lcv function
    def test_lcv(self):
        test_graph = {1 : {2}, 2 : {1,3}, 3 : {2}}
        test_dict_colors = {'red': (255,0,0), 'blue': (0,0,255), 
                            'green': (0,255,0), 'default': (0,0,0)}
        csp = CSP(test_graph, test_dict_colors)
        
        csp.domains[1] = ['red', 'green']
        csp.domains[2] = ['red', 'green']
        csp.domains[3] = ['green', 'blue']

        assert csp.least_constraints_values(2) == ['red', 'green']

def main():
    unittest.main()

main()