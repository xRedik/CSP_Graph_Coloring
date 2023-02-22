import pygame
import gui_config

def add_edges(node_class_lists):
    for node in node_class_lists:
        for path in node.paths:
            pygame.draw.line(gui_config.window, (0,0,0), node.position, _get_pos_from_value(node_class_lists,path))

def _get_pos_from_value(node_class_lists,path):
    for node in node_class_lists:
        if node.value == path:
            return node.position

def add_vertex(node_class_lists):
    for node in node_class_lists:
        br = pygame.draw.circle(gui_config.window, (0,0,0), node.position, gui_config.vertex_radius)
        _add_name(node, gui_config.window, size=15)

def _add_name(node, window, size=15):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    w, h = font.size(str(node.value))
    surf = font.render(str(node.value), True, (255,255,255))
    window.blit(surf, (node.pos_x-(w/2), 
                       node.pos_y-(h/2)))

