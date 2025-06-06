#
# BREAKOUT GAME 
#

import pygame, time


FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32

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
player_img = pygame.transform.scale(player_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

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
      player_y = player_y + paddle_speed_y
    if keys[pygame.K_w] :
      paddle_y = paddle_y - paddle_speed_y
    if keys[pygame.K_d] :
      paddle_x = paddle_x + paddle_speed_x
    
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 1:
       paddle_x = 1    
    if paddle_y + PADDLE_HEIGHT > SCREEN_HEIGHT:
       paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT
    if paddle_y < 1:
       paddle_y = 1     
    screen.fill('black') 

    screen.blit(paddle_img, (paddle_x, paddle_y))
   
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) 

print('mygame stopt running')
