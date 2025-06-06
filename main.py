#
# BREAKOUT GAME 
#

import pygame, time


FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_WIDTH = 144
PLAYER_HEIGHT = 32

player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT - 100
player_speed_x = 10
player_speed_y = 10

#
# init game
#

pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

player_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
player_img.blit(spritesheet, (0, 0), (1158, 462, 243, 64))   
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

#
# game loop
#



print('mygame is running')
running = True
while running:
    #
    # read events
    # 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            running = False 
    keys = pygame.key.get_pressed() 
   
    if keys[pygame.K_a] :
      player_x = player_x - player_speed_x

    if keys[pygame.K_s] :
      player_y = player_y + player_speed_y
    if keys[pygame.K_w] :
      player_y = player_y - player_speed_y
    if keys[pygame.K_d] :
      player_x = player_x + player_speed_x
    
    if player_x + PLAYER_WIDTH > SCREEN_WIDTH:
       player_x = SCREEN_WIDTH - PLAYER_WIDTH
    if player_x < 1:
       player_x = 1    
    if player_y + PLAYER_HEIGHT > SCREEN_HEIGHT:
       player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
    if player_y < 1:
       player_y = 1     
    screen.fill('black') 

    screen.blit(player_img, (player_x, player_y))
   
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) 

print('mygame stopt running')
