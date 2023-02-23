from read_initialize import *
from gui_config import *
import gui
import sys

def main():
    num_colors, node_class_lists = read_file("input_text.txt")
    color_list = choose_colors(num_colors)
    left_click = False
    while True:
        gui.refresh_window()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == pygame.BUTTON_LEFT:
                    left_click = True
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == pygame.BUTTON_LEFT:
                    left_click = False
            if e.type == pygame.QUIT:
                sys.exit()
        
        gui.make_graph_flexible(node_class_lists)
        gui.add_edges(node_class_lists)
        gui.add_vertex(node_class_lists,left_click)
  
        clock.tick(fps)
        pygame.display.flip()

    #csp(num_colors,dict_graph)


if __name__ == "__main__":
    main()
