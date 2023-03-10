from gui import GUI
from file import File_handler
from csp import CSP

def main():
    file = File_handler("input_files/input_text.txt")
    class_vertex_list, dict_graph, color_list = file.construct_graph_from_file()
    gui = GUI(class_vertex_list)
    csp = CSP(dict_graph, color_list)
    #print(dict_graph)
    #print(color_list)
    csp.backtracking()

    print(csp.assignment)
    # while True:
    #     gui.check_events()
    #     gui.update_graph()
    #     gui.refresh_window()

    #     #csp(num_colors,dict_graph)


if __name__ == "__main__":
    main()