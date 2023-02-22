import pygame

resolution = (1024, 768)
vertex_radius = 20
X_boundary = 150
Y_boundary = 50
fps = 60

pygame.init()
window = pygame.display.set_mode(resolution)
pygame.display.set_caption("CSP Graph Coloring by Farid Guliyev")
clock = pygame.time.Clock()
window.fill((255, 255, 255))

