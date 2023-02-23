import pygame
import math
import sys

class GUI():
    def __init__(self,vertex_list,resolution = (1280,720), vertex_radius = 20, 
                 boundary_x = 150, boundary_y = 50, fps = 60, font_size = 15):
        self.vertex_list = vertex_list
        self.resolution = resolution
        self.vertex_radius = vertex_radius
        self.boundary_x, self.boundary_y = boundary_x, boundary_y
        self.fps = fps
        self.font_size = font_size
        self.lmb_state = False
        pygame.init()
        self.window = pygame.display.set_mode(self.resolution)
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
            if e.type == pygame.QUIT:
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
            br = pygame.draw.circle(self.window, (0,0,0), vertex.position, self.vertex_radius)
            self._add_name(vertex)
            
            #DEYIW
            if br.collidepoint(new_x, new_y) and self.lmb_state:
                vertex.clicked = True
            if vertex.clicked and not self.lmb_state:
                vertex.clicked = False

            if vertex.clicked:
                vertex.pos_x = new_x
                vertex.pos_y = new_y

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
                    vertex_1.pos_x -= int(vertex_1.repel * (dx / euc_distance))
                    vertex_1.pos_y -= int(vertex_1.repel * (dy / euc_distance))
        
            vertex_1.position = (vertex_1.pos_x, vertex_1.pos_y)

    def refresh_window(self):
        self.clock.tick(self.fps)
        pygame.display.flip()
        self.window.fill((255, 255, 255))