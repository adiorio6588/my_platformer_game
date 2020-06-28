####################### Imports ###########################

import pygame, sys

from pygame.locals import * # (part 1)importing all pygame modules
pygame.init() 

################# Varibiles for the game ##################

clock = pygame.time.Clock()

pygame.display.set_caption('My Pygame Window')

WINDOW_SIZE = (400, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # (part 1)initiate window

player_image = pygame.image.load('player.png') # player image (PART 2)

moving_right = False # player movements variables (PART 2)
moving_left = False

player_location = [50, 50] # player starting location (PART 2)
player_y_momentum = 0 # Y coordinate variable for jumping 

player_rect = pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())# Collison Rect for player (PART 2)
test_rect = pygame.Rect(100, 100, 100, 50) # first two ints is the location of the react (PART 2)


while True: # (part 1)game loop
    screen.fill((146,244,255)) # fills the screen with a rgb color to prevent trails (PART 2)

    screen.blit(player_image, player_location) # player image surface on top of screen, player location variable being used (PART 2)

    if player_location[1] > WINDOW_SIZE[1] - player_image.get_height(): # Player bouncing once hitting the bottom (PART 2)
        player_y_momentum =- player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if moving_right == True: # moves the player once right or left is pressed (PART 2)
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    player_rect.x = player_location[0] # update rect to player's position (PART 2)
    player_rect.y = player_location[1] 

    # test rect for Collisions
    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255,0,0), test_rect)
    else:
        pygame.draw.rect(screen, (0,0,0), test_rect)
    
    for event in pygame.event.get(): # event loop (PART1 1)
        if event.type == QUIT: # check for window quit (KEY_X) (PART 1) 
            pygame.quit() # stop pygame (PART 1)
            sys.exit() # stop script (PART 1)
        if event.type == KEYDOWN: # checking when keys are pressed down (PART 2)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT: 
                moving_left = False

    pygame.display.update()
    clock.tick(60) # (part 1)frames per second 