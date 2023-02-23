from gui import GUI
from file import File_handler

def main():
    file = File_handler("input_files/input_text.txt")
    _, vertex_list = file.construct_graph_from_file()
    color_list = file.choose_colors()
    gui = GUI(vertex_list)
    while True:
        gui.check_events()
        gui.update_graph()
        gui.refresh_window()

        #csp(num_colors,dict_graph)


if __name__ == "__main__":
    main()