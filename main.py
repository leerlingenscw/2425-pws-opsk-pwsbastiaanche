#
# GAME BASTIAAN EN CHÉ
#

import pygame, random, math

# CONSTANTEN
FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_WIDTH = 120
PLAYER_HEIGHT = 150
MONSTER_WIDTH = 100
MONSTER_HEIGHT = 100
MONSTER_COUNT = 5

# INIT PLAYER
player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT - 100
player_speed_x = 10
player_speed_y = 10

# INIT PYGAME
pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# LAAD SPRITESHEET
spritesheet = pygame.image.load('Player.png').convert_alpha()
spritesheet1 = pygame.image.load("monster.png").convert_alpha()

# SPELER AFBEELDING
player_img = pygame.Surface((60, 90), pygame.SRCALPHA)
player_img.blit(spritesheet, (0, 0), (0, 0, 1111, 1100))
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# MONSTER AFBEELDING
monster_img = pygame.Surface((70, 70), pygame.SRCALPHA)
monster_img.blit(spritesheet1, (0, 0), (0, 0, 50, 50))
Monster_img = pygame.transform.scale(monster_img, (MONSTER_WIDTH, MONSTER_HEIGHT))

# MEERDERE MONSTERS AANMAKEN
monsters = []
for i in range(MONSTER_COUNT):
    monsters.append({
        "x": random.randint(0, SCREEN_WIDTH - MONSTER_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT - MONSTER_HEIGHT),
        "speed": 3
    })

background_img = pygame.image.load("pixilart-drawing (1).png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

print('mygame is running')
running = True
while running:
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed_x
    if keys[pygame.K_d]:
        player_x += player_speed_x
    if keys[pygame.K_w]:
        player_y -= player_speed_y
    if keys[pygame.K_s]:
        player_y += player_speed_y

    # SPELER BINNEN SCHERM HOUDEN
    player_x = max(0, min(player_x, SCREEN_WIDTH - PLAYER_WIDTH))
    player_y = max(42, min(player_y, SCREEN_HEIGHT - PLAYER_HEIGHT))
    

    # SCHERM VERVERSEN
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, (player_x, player_y))
    # BEWEEG EN TEKEN MONSTERS
    for i, monster in enumerate(monsters):
        dx = player_x - monster["x"]
        dy = player_y - monster["y"]
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance
            monster["x"] += dx * monster["speed"]
            monster["y"] += dy * monster["speed"]

        screen.blit(Monster_img, (monster["x"], monster["y"]))

        # BOTST MET SPELER?
        HITBOX_OFFSET = 50

        if (monster["x"] + MONSTER_WIDTH - HITBOX_OFFSET > player_x and
            monster["x"] + HITBOX_OFFSET < player_x + PLAYER_WIDTH and
            monster["y"] + MONSTER_HEIGHT - HITBOX_OFFSET > player_y and
            monster["y"] + HITBOX_OFFSET < player_y + PLAYER_HEIGHT):
            print(f"Monster {i} pakt speler!")
    # BOTST MONSTERS MET ELKAAR?
    for i, monster in enumerate(monsters):
        for j, other in enumerate(monsters):
            if i == j:
                continue

            if (monster["x"] + MONSTER_WIDTH > other["x"] and
                monster["x"] < other["x"] + MONSTER_WIDTH and
                monster["y"] + MONSTER_HEIGHT > other["y"] and
                monster["y"] < other["y"] + MONSTER_HEIGHT):

                dx = other["x"] - monster["x"]
                dy = other["y"] - monster["y"]
                distance = math.hypot(dx, dy)
                if distance != 0:
                    dx /= distance
                    dy /= distance
                    monster["x"] -= dx * monster["speed"]
                    monster["y"] -= dy * monster["speed"]

    # VERVERS SCHERM
    pygame.display.flip()
    fps_clock.tick(FPS)

print('mygame stopt running')
            
