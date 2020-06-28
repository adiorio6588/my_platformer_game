####################### Imports ###########################

import pygame, sys

from pygame.locals import * #importing all pygame modules
pygame.init() 

################# Varibiles for the game ##################

clock = pygame.time.Clock()

pygame.display.set_caption('My Pygame Window')

WINDOW_SIZE = (400, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initiate window

while True: # game loop

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    clock.tick(60) # frames per second 