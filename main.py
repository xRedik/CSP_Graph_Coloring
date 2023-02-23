from read_initialize import *
from gui import GUI

def main():
    num_colors, node_class_lists = read_file("input_text.txt")
    color_list = choose_colors(num_colors)
    gui = GUI(node_class_lists)
    while True:        
        gui.check_events()
        gui.update_graph()
        gui.refresh_window()

        #csp(num_colors,dict_graph)


if __name__ == "__main__":
    main()
