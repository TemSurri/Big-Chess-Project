
from menu_render import *

#todo: -------------

#make minimax algorithm to play against
#make ai, neural network to play against

pygame.init()
screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Chess Interface")
running = True


game = MenusAndGame(pygame)
game.passive()

pygame.quit()


