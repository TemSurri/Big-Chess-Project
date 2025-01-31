import pygame
from menu_render import *
import time

#todo: -------------

#put on Git-Hub properly
#make algorithm to play against 


pygame.init()
screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Chess Interface")
running = True

game = MenusAndGame(pygame)
game.passive()

pygame.quit()


