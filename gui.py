# it is just helper variable for hiding the default output text from pygame module
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import math
import sys

# The GUI class for displaying the vertices and interacting with them
class GUI():
    # the resolution and boundary assigned like that 
    # because other file class is using that two variable
    # to calculate the random position
    resolution = (1280,720)
    boundary = (150,50)
    def __init__(self,vertex_list, chosen_dict_colors, assignment = None, 
                 vertex_radius = 20, fps = 60, font_size = 15, automatic = False):
        # initializing the variables
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
        
        # checking the user desired coloring method in GUI
        # if automatic selected, we are assigning the colors to the vertex
        # from the assignment of the csp
        if self.auto:
            for vertex in self.vertex_list:
                vertex.color = self.csp_assignment[vertex.value]
        
        # initializing the window of GUI
        pygame.init()
        self.window = pygame.display.set_mode(GUI.resolution)
        pygame.display.set_caption("CSP Graph Coloring by Farid Guliyev")
        self.clock = pygame.time.Clock()
        self.window.fill((255, 255, 255))

    # The method for checking the events
    def check_events(self):
        for e in pygame.event.get():

            # if left click is pressed it means 
            # user wants to move the vertex
            # that is why we are changing the state of the lmb_state
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == pygame.BUTTON_LEFT:
                     self.lmb_state = True
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == pygame.BUTTON_LEFT:
                     self.lmb_state = False
            
            # checking the condition that if user selected 
            # manual coloring mode and pressed the key
            if e.type == pygame.KEYUP and not self.auto:

                # if left key is pressed then 
                # then we are changing the color of vertex 
                # to the default color for GUI
                if e.key == pygame.K_LEFT:
                    if self.index == self.max_limit:
                        self.index-=1
                    self.vertex_list[self.index].color = "default"
                    if self.index>0:
                        self.index-=1
                
                # if right key is selected then
                # we are assigning the color that csp has assigned to the vertex
                elif e.key == pygame.K_RIGHT:
                    if self.index>=self.max_limit:
                        continue
                    self.vertex_list[self.index].color = self.csp_assignment[self.vertex_list[self.index].value]
                    self.index+=1
    
            # if events is quit, it means user want to terminate the program
            elif e.type == pygame.QUIT:
                sys.exit()


    # it is just the helper method for calling the other methods in order
    # instead of writing them in main function one by one
    def update_graph(self):
        self.check_events()
        self.add_edges()
        self.add_vertex()
        self.make_graph_flexible()
        self.refresh_window()

    # The method for adding or updating the edges in the GUI
    def add_edges(self):
        for vertex in self.vertex_list:
            for n in vertex.paths:   
                pygame.draw.line(self.window, (0,0,0), vertex.position, self._get_pos_from_value(n))

    # The helper method for getting the position of neighbor
    def _get_pos_from_value(self,neighbour):
        for vertex in self.vertex_list:
            if vertex.value == neighbour:
                return vertex.position

    # The method for adding or updating the vertex in the GUI
    def add_vertex(self):
        new_x, new_y = pygame.mouse.get_pos()
        for vertex in self.vertex_list:
            # drawing the circle and displaying the vertex name
            br = pygame.draw.circle(self.window, self.chosen_dict_colors[vertex.color], vertex.position, self.vertex_radius)
            self._add_name(vertex)
            
            # checking the node clicked state and 
            # assigning the new position if it is true
            if vertex.pressed:
                vertex.pos_x = new_x
                vertex.pos_y = new_y
            
            # checking the state of the mouse and colliding of the points
            # and assigning the pressed state of the vertex based on that
            if br.collidepoint(new_x, new_y) and self.lmb_state:
                vertex.pressed = True
            elif vertex.pressed and not self.lmb_state:
                vertex.pressed = False

    # The method for writing the value of the vertex on circle object
    def _add_name(self,vertex):
        font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        w, h = font.size(str(vertex.value))
        surf = font.render(str(vertex.value), True, (255,255,255))
        self.window.blit(surf, (vertex.pos_x-(w/2), 
                        vertex.pos_y-(h/2)))

    # The method for making the graph flexible
    # this method is helping is to moving around the vertices 
    # while considering the relationship between other vertices
    def make_graph_flexible(self):
        for i, vertex_1 in enumerate(self.vertex_list):
            for j, vertex_2 in enumerate(self.vertex_list):
                # if same vertices just continue
                if i == j:
                    continue
                
                # calculating the difference between the vertices
                # and calculating the euclidean distance
                dx, dy = vertex_2.pos_x - vertex_1.pos_x, vertex_2.pos_y - vertex_1.pos_y
                euc_distance = math.hypot(dx, dy) + 1
                
                # calculating the new position based on the repelsion force and distance
                if euc_distance < self.vertex_radius + 50:
                    vertex_1.pos_x -= int(vertex_1.repelsion_force * (dx / euc_distance))
                    vertex_1.pos_y -= int(vertex_1.repelsion_force * (dy / euc_distance))
        
            vertex_1.position = (vertex_1.pos_x, vertex_1.pos_y)

    # The method for refreshing the window
    def refresh_window(self):
        self.clock.tick(self.fps)
        pygame.display.flip()
        self.window.fill((255, 255, 255))