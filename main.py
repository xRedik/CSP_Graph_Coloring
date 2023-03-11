import sys
import os
import argparse

from gui import GUI
from file import File_to_Graph
from csp import CSP

#test cases
#comments

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--filename",dest ="filename", help="Name of the input file")
    parser.add_argument("-gui", "--gui", dest = "display_gui", 
                        help="Display GUI",
                        action=argparse.BooleanOptionalAction, default = True)
    parser.add_argument("-a", "--auto", dest = "auto_coloring_method", 
                        help="Automatic Coloring method", 
                        action=argparse.BooleanOptionalAction, default=True)

    args = parser.parse_args()

    filename = args.filename
    display_gui = args.display_gui
    auto_cm = args.auto_coloring_method

    print("==========Configuration==========")
    print("\tEntered filename is ",filename)
   
    if display_gui:
        print("\tThe GUI is activated (default mode)")
    else:
        print("\tThe GUI is deactivated")

    if auto_cm:
        print("\tThe automatic coloring method is selected (default mode)")
    else:
        print("\tThe manual key coloring method is selected\n")

    if filename is None:
        raise Exception("Please add the second argument for the name of the file")
    
    if not os.path.isfile(filename):
        raise FileExistsError("File do not exist")
    
    file = File_to_Graph(filename)

    class_vertex_list, dict_graph, dict_color = file.construct_graph_from_file()

    csp = CSP(dict_graph, dict_color)
    csp.backtracking(csp.domains)
    csp.print_assignment()

    if not display_gui:
        return
    
    gui = GUI(class_vertex_list,dict_color,csp.assignment,automatic = auto_cm)

    while True:
        gui.check_events()
        gui.update_graph()
        gui.refresh_window()

if __name__ == "__main__":
    main()