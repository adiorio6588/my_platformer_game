import pygame, sys, os, random
import data.engine as e
from pygame.locals import * # importing all pygame modules (PART 1)

pygame.mixer.pre_init(44100, -16, 2, 512)  # changes sound playtime(PART 6)
pygame.init() 
pygame.mixer.set_num_channels(64) # setting how many sounds play at once (PART 6)

clock = pygame.time.Clock()

pygame.display.set_caption('Pixel Pug')

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initiate window (PART 1)

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled (PART 3)

moving_right = False # (PART 3)
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0, 0] # (PART 4)

############## SCORE TEST #########################################################################################
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32) # Font size is 32

score_x = 10
score_y = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
############## SCORE TEST #########################################################################################

CHUNK_SIZE = 8

def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            if target_y > 10:
                tile_type = 2 # dirt
            elif target_y == 10:
                tile_type = 1 # grass
            elif target_y == 9:
                if random.randint(1,5) == 1:
                    tile_type = 3 # plant
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data

class jumper_obj():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(jumper_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 8, 9)

    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)

#################### ANIMATIONS ###############################################################################
e.load_animations('data/images/entities/') # FROM GAME ENGINE (PART 8)
game_map = {}

grass_img = pygame.image.load('data/images/grass.png')
dirt_img = pygame.image.load('data/images/dirt.png')
plant_img = pygame.image.load('data/images/plant.png').convert()
plant_img.set_colorkey((255, 255, 255))

jumper_img = pygame.image.load('data/images/jumper.png').convert()
jumper_img.set_colorkey((255,255,255))

tile_index = {1:grass_img, 
              2:dirt_img, 
              3:plant_img
              }



################## ENEMY TEST CODE #######################

enemies = []

for i in range(5):
    enemies.append([0,e.entity(random.randint(0,600)-300,80,13,13,'enemy')])

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # enemy_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        

animation_database = {}

animation_database['fly'] = load_animation('data/entities/enemy/fly',[7,7,7,7,7])
animation_database['idle'] = load_animation('data/entities/enemy/idle',[7,7])

enemy_action = 'idle'
enemy_frame = 0
enemy_flip = False

enemy_rect = pygame.Rect(100,100,5,13)

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
################## ENEMY TEST CODE #######################


#################### ANIMATIONS ###############################################################################


############## SOUNDS #########################################################################################
jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
grass_sounds = [pygame.mixer.Sound('data/audio/grass_0.wav'), pygame.mixer.Sound('data/audio/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('data/audio/music.wav')
pygame.mixer.music.play(-1)

grass_sound_timer = 0
############## SOUNDS #########################################################################################

player = e.entity(100, 100, 30, 23, 'player') # FROM GAME ENGINE (PART 8)

enemies = []

for i in range(5):
    enemies.append([0,e.entity(random.randint(0,600) -300, 80, 32, 32,'enemy')])

jumper_objects = []

for i in range(5):
    jumper_objects.append(jumper_obj((random.randint(0,600)-300,80)))


background_objects = [[0.25,[120,10,70,400]], [0.25,[280,30,40,400]], [0.5,[30,40,40,400]], [0.5,[130,90,100,400]], [0.5,[300,80,120,400]]]



##################### GAME LOOP ################################################################################
while True: 
    display.fill((146,244,255)) # fills the screen with a rgb color to prevent trails (PART 2)

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player.x-true_scroll[0]-152)/20
    true_scroll[1] += (player.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75), pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)


    tile_rects = [] # (PART 3)
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))    

    player_movement = [0,0] # (PART 3)
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_flip(False)
        player.set_action('run')
    if player_movement[0] < 0:
        player.set_flip(True)
        player.set_action('run')
    if player_movement[1] < 0:
        player.set_action('jump')

    collision_types = player.move(player_movement,tile_rects)

    if collision_types['bottom'] == True: # (PART 3)
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer == 30
                random.choice(grass_sounds).play() # function that picks a random sound (PART 6)
    else:
        air_timer += 1

    player.change_frame(1)
    player.display(display, scroll)


    for jumper in jumper_objects:
        jumper.render(display, scroll)
        if jumper.collision_test(player.obj.rect):
            vertical_momentum = -3

    display_r = pygame.Rect(scroll[0],scroll[1],300,200)

 
##################### TEST CODE #########################

    for enemy in enemies:
        if display_r.colliderect(enemy[1].obj.rect):
            enemy[0] += 0.2
            if enemy[0] > 3:
                enemy[0] = 3
            enemy_movement = [0,enemy[0]]
            if player.x > enemy[1].x + 5:
                enemy_movement[0] = 1
            if player.x < enemy[1].x - 5:
                enemy_movement[0] = -1
            collision_types = enemy[1].move(enemy_movement,tile_rects)
            if collision_types['bottom'] == True:
                enemy[0] = 0

            enemy[1].display(display,scroll)

            if player.obj.rect.colliderect(enemy[1].obj.rect):
                vertical_momentum = -4

    enemy_movement = [0,0]
    if moving_right == True:
        enemy_movement[0] += 2
    if moving_left == True:
        enemy_movement[0] -= 2
    enemy_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if enemy_movement[0] == 0:
        enemy_action,enemy_frame = change_action(enemy_action,enemy_frame,'idle')
    if enemy_movement[0] > 0:
        enemy_flip = False
        enemy_action,enemy_frame = change_action(enemy_action,enemy_frame,'run')
    if enemy_movement[0] < 0:
        enemy_flip = True
        enemy_action,enemy_frame = change_action(enemy_action,enemy_frame,'run')

    enemy_rect,collisions = move(enemy_rect,enemy_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    enemy_frame += 1
    if enemy_frame >= len(animation_database[enemy_action]):
        enemy_frame = 0
    enemy_img_id = animation_database[enemy_action][enemy_frame]
    enemy_img = animation_frames[enemy_img_id]
    display.blit(pygame.transform.flip(enemy_img,enemy_flip,False),(enemy_rect.x-scroll[0],enemy_rect.y-scroll[1]))



##################### TEST CODE #########################



    for event in pygame.event.get(): # event loop (PART1 1)
        if event.type == QUIT: # check for window quit (KEY_X) (PART 1) 
            pygame.quit() # stop pygame (PART 1)
            sys.exit() # stop script (PART 1)
        if event.type == KEYDOWN: # checking when keys are pressed down (PART 2)
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.music.play(-1)    
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    show_score(score_x, score_y)
    pygame.display.update()
    clock.tick(60) # frames per second (PART 1)
