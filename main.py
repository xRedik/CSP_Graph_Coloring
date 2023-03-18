import os
import argparse
from gui import GUI
from file import File_to_Graph
from csp import CSP
import subprocess

def main():
    
    # creating the instance for adding the flags and arguments for program
    parser = argparse.ArgumentParser()

    # filename argument. It is required by program
    parser.add_argument("-f", "--filename",dest ="filename", help="name of the input file")
    
    # display GUI argument. Not required. Default value is True. 
    # it means GUI will be displayed in default value
    parser.add_argument("-g", "--gui", dest = "display_gui", 
                        help="display GUI",
                        action=argparse.BooleanOptionalAction, default = True)
    
    # automatic coloring method argument. Not required. Default value is True. 
    # it means GUI will be displayed with the colors of the Vertex that assigned by CSP
    # when this argument is False. Color of the vertexes will be displayed one by one with the left and right keys
    parser.add_argument("-a", "--auto", dest = "auto_coloring_method", 
                        help="automatic Coloring method", 
                        action=argparse.BooleanOptionalAction, default=True)
    
    # executing test scripts argument. Default value is True. It means tests will be executed automatically.
    parser.add_argument("-t", "--run_test", dest = "run_test", 
                        help="flag for running the test", 
                        action=argparse.BooleanOptionalAction, default=True)
    

    # fetching the values
    args = parser.parse_args()
    
    filename = args.filename
    display_gui = args.display_gui
    auto_cm = args.auto_coloring_method
    run_test = args.run_test

    if filename is None:
        raise NameError("Please add the name of the file with f flag")

    print("==========CONFIGURATION==========")

    # printing the name of the file
    print("\tEntered filename is ",filename)
   
    # printing the state of the GUI (activated or deactivated)
    if display_gui:
        print("\tThe GUI is activated (default mode)")
    else:
        print("\tThe GUI is deactivated")

    # printing the state of the automatic coloring method (activated or deactivated)
    if auto_cm:
        print("\tThe automatic coloring method is selected (default mode)")
    else:
        print("\tThe manual key coloring method is selected")

    # printing the state of the test script (activated or deactivated)
    # if activated it will be executed automatically
    if run_test:
        print("\tThe test script is executed (default mode)\n")

        print("==========TEST RESULT==========")
        output_test = subprocess.run(['python', 'test_csp.py'], stdout=subprocess.PIPE)
        print(output_test.stdout.decode('utf-8'))
    else:
        print("\tThe execution of the test script is disabled\n")

    # checking if user added the name of the file or not
    if filename is None:
        raise Exception("Please add the second argument for the name of the file")
    
    # checking the existence of the file
    if not os.path.isfile(filename):
        raise FileExistsError("File do not exist")
    
    # creating object from file_to_graph class
    file = File_to_Graph(filename)

    # calling the method of that object and unpack the tuple 
    class_vertex_list, dict_graph, dict_color = file.construct_graph_from_file()
    
    # creating object from the CSP class and add graph and color dictionaries arguments
    csp = CSP(dict_graph, dict_color)

    # calling the backtracking method to find the solution
    csp.backtracking(csp.domains)

    # print the solution
    csp.print_assignment()

    # if GUI is disabled, then we can terminate the program
    if not display_gui:
        return
    
    # displaying the GUI
    gui = GUI(class_vertex_list,dict_color,csp.assignment,automatic = auto_cm)

    # updating the graph in an infinite loop until user exiting the GUI
    while True:
        gui.update_graph()

if __name__ == "__main__":
    main()