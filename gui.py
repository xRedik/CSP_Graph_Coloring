from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import math
import sys

class GUI():
    resolution = (1280,720)
    boundary = (150,50)
    def __init__(self,vertex_list, chosen_dict_colors, assignment = None, 
                 vertex_radius = 20, fps = 60, font_size = 15, automatic = False):
        self.vertex_list = sorted(vertex_list, key = lambda v: v.value)
        self.vertex_radius = vertex_radius
        self.fps = fps
        self.font_size = font_size
        self.lmb_state = False
        self.chosen_dict_colors = chosen_dict_colors
        self.csp_assignment = assignment
        self.index = 0
        self.max_limit = len(self.vertex_list)
        self.auto = automatic
        
        if self.auto:
            for vertex in self.vertex_list:
                vertex.color = self.csp_assignment[vertex.value]
        
        pygame.init()
        self.window = pygame.display.set_mode(GUI.resolution)
        pygame.display.set_caption("CSP Graph Coloring by Farid Guliyev")
        self.clock = pygame.time.Clock()
        self.window.fill((255, 255, 255))

    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == pygame.BUTTON_LEFT:
                     self.lmb_state = True
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == pygame.BUTTON_LEFT:
                     self.lmb_state = False
            
            if e.type == pygame.KEYUP and not self.auto:
                if e.key == pygame.K_LEFT:
                    if self.index == self.max_limit:
                        self.index-=1
                    self.vertex_list[self.index].color = "default"
                    if self.index>0:
                        self.index-=1
                elif e.key == pygame.K_RIGHT:
                    if self.index>=self.max_limit:
                        continue
                    self.vertex_list[self.index].color = self.csp_assignment[self.vertex_list[self.index].value]
                    self.index+=1
    
            elif e.type == pygame.QUIT:
                sys.exit()


    def update_graph(self):
        self.add_edges()
        self.add_vertex()
        self.make_graph_flexible()
    
    def add_edges(self):
        for vertex in self.vertex_list:
            for path in vertex.paths:   
                pygame.draw.line(self.window, (0,0,0), vertex.position, self._get_pos_from_value(path))

    def _get_pos_from_value(self,path):
        for vertex in self.vertex_list:
            if vertex.value == path:
                return vertex.position

    def add_vertex(self):
        new_x, new_y = pygame.mouse.get_pos()
        for vertex in self.vertex_list:
            br = pygame.draw.circle(self.window, self.chosen_dict_colors[vertex.color], vertex.position, self.vertex_radius)
            self._add_name(vertex)
            
            if vertex.pressed:
                vertex.pos_x = new_x
                vertex.pos_y = new_y
            
            if br.collidepoint(new_x, new_y) and self.lmb_state:
                vertex.pressed = True
            elif vertex.pressed and not self.lmb_state:
                vertex.pressed = False

    def _add_name(self,vertex):
        font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        w, h = font.size(str(vertex.value))
        surf = font.render(str(vertex.value), True, (255,255,255))
        self.window.blit(surf, (vertex.pos_x-(w/2), 
                        vertex.pos_y-(h/2)))

    def make_graph_flexible(self):
        for i, vertex_1 in enumerate(self.vertex_list):
            for j, vertex_2 in enumerate(self.vertex_list):
                if i == j:
                    continue
                
                dx, dy = vertex_2.pos_x - vertex_1.pos_x, vertex_2.pos_y - vertex_1.pos_y
                euc_distance = math.hypot(dx, dy) + 1
                
                if euc_distance < self.vertex_radius + 50:
                    vertex_1.pos_x -= int(vertex_1.repelsion_force * (dx / euc_distance))
                    vertex_1.pos_y -= int(vertex_1.repelsion_force * (dy / euc_distance))
        
            vertex_1.position = (vertex_1.pos_x, vertex_1.pos_y)

    def refresh_window(self):
        self.clock.tick(self.fps)
        pygame.display.flip()
        self.window.fill((255, 255, 255))