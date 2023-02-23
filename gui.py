import pygame
import gui_config
import math

def add_edges(node_class_lists):
    for node in node_class_lists:
        for path in node.paths:
            pygame.draw.line(gui_config.window, (0,0,0), node.position, _get_pos_from_value(node_class_lists,path))

def _get_pos_from_value(node_class_lists,path):
    for node in node_class_lists:
        if node.value == path:
            return node.position

def add_vertex(node_class_lists,lmb):
    new_x, new_y = pygame.mouse.get_pos()
    for node in node_class_lists:
        br = pygame.draw.circle(gui_config.window, (0,0,0), node.position, gui_config.vertex_radius)
        _add_name(node, gui_config.window, size=15)
        
        print(new_x,new_y)
        #DEYIW
        if br.collidepoint(new_x, new_y) and lmb:
            node.clicked = True
        if node.clicked and not lmb:
            node.clicked = False

        if node.clicked:
            node.pos_x = new_x
            node.pos_y = new_y


def _add_name(node, window, size=15):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    w, h = font.size(str(node.value))
    surf = font.render(str(node.value), True, (255,255,255))
    window.blit(surf, (node.pos_x-(w/2), 
                       node.pos_y-(h/2)))


def make_graph_flexible(node_class_lists):
    for i, node_1 in enumerate(node_class_lists):
        for j, node_2 in enumerate(node_class_lists):
            if i == j:
                continue
            
            dx, dy = node_2.pos_x - node_1.pos_x, node_2.pos_y - node_1.pos_y
            dist = math.hypot(dx, dy) + 1
            
            if dist < gui_config.vertex_radius + 50:
                # forceX = dx / dist
                # forceY = dy / dist
                node_1.pos_x -= int(node_1.repel * (dx / dist))
                node_1.pos_y -= int(node_1.repel * (dy / dist))
    
        node_1.position = (node_1.pos_x, node_1.pos_y)


def refresh_window():
    gui_config.window.fill((255, 255, 255))
