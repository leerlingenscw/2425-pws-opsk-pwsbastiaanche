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
WEAPON_WIDTH = 70
WEAPON_HEIGHT = 120
HEART_WIDTH = 50
HEART_HEIGHT = 50
COIN_WIDTH = 40
COIN_HEIGHT = 40
weapon_angle = 0  # initial angle in degrees
weapon_radius = 100  # distance from player to weapon center
bounce_strength = 200
lives = 3
wave = 1
coins = 1000000
score = 0 
buyteller = 1
wave_delay = 0

# INIT PLAYER
player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT - 100
player_speed_x = 10
player_speed_y = 10

# INIT WEAPON
weapon_x = SCREEN_WIDTH / 2 
weapon_y = SCREEN_HEIGHT - 250
weapon_speed_x = 10
weapon_speed_y = 10

# INIT PYGAME
pygame.init()
font = pygame.font.SysFont('default', 50)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# LAAD SPRITESHEET
spritesheet = pygame.image.load('Player.png').convert_alpha()
spritesheet1 = pygame.image.load("monster.png").convert_alpha()
spritesheet2 = pygame.image.load("weapon2.png").convert_alpha()
spritesheet3 = pygame.image.load('heart.png').convert_alpha()
spritesheet4 = pygame.image.load('coin.png').convert_alpha()
spritesheet5 = pygame.image.load("legendary_sword.png").convert_alpha()
spritesheet6 = pygame.image.load("HAMMER.png").convert_alpha()
# SPELER AFBEELDING
player_img = pygame.Surface((60, 90), pygame.SRCALPHA)
player_img.blit(spritesheet, (0, 0), (0, 0, 1111, 1100))
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# MONSTER AFBEELDING
monster_img = pygame.Surface((70, 70), pygame.SRCALPHA)
monster_img.blit(spritesheet1, (0, 0), (0, 0, 50, 50))
Monster_img = pygame.transform.scale(monster_img, (MONSTER_WIDTH, MONSTER_HEIGHT))

# ZWAARD AFBEELDING
weapon_img = pygame.Surface((70, 130), pygame.SRCALPHA)
weapon_img.blit(spritesheet2, (0, 0), (0, 0, 100, 150))
weapon_img = pygame.transform.scale(weapon_img, (WEAPON_WIDTH, WEAPON_HEIGHT))

# HEART AFBEELDING
heart_img = pygame.Surface((100, 100), pygame.SRCALPHA)
heart_img.blit(spritesheet3, (0, 0), (0, 0, 100, 100))
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

# COINS AFBEELDING
coin_img = pygame.Surface((40, 40), pygame.SRCALPHA)
coin_img.blit(spritesheet4, (0, 0), (0, 0, 40, 40))
coin_img = pygame.transform.scale(coin_img, (COIN_WIDTH, COIN_HEIGHT))

# MEERDERE MONSTERS AANMAKEN
monsters = []
for i in range(MONSTER_COUNT):
    monsters.append({
        "x": random.randint(0, SCREEN_WIDTH - MONSTER_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT - MONSTER_HEIGHT),
        "speed": 4
    })

background_img = pygame.image.load("image.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

print('mygame is running')

start_ticks = pygame.time.get_ticks() 
game_paused = False
game_over = False
countdown_active = True
countdown_start_ticks = pygame.time.get_ticks()

running = True
while running:
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # COUNTDOWN AAN HET BEGIN
    if countdown_active:
        current_ticks = pygame.time.get_ticks()
        elapsed_time = (current_ticks - countdown_start_ticks) // 1000
        
        if elapsed_time < 4:
            if elapsed_time == 0:
                countdown_text = "3"
            elif elapsed_time == 1:
                countdown_text = "2"
            elif elapsed_time == 2:
                countdown_text = "1"
            elif elapsed_time == 3:
                countdown_text = "GO!"

            screen.blit(background_img, (0, 0))
            screen.blit(player_img, (player_x, player_y))
            screen.blit(weapon_img, (weapon_x, weapon_y))
            for monster in monsters:
               screen.blit(Monster_img, (monster["x"], monster["y"]))


            text_surface = font.render(countdown_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(40, 20))
            screen.blit(text_surface, text_rect)

            pygame.display.flip()
            fps_clock.tick(FPS)
            continue  # Skip rest van de game logic tijdens countdown

        else:
            countdown_active = False
            start_ticks = pygame.time.get_ticks()  # Game timer resetten na countdown


    if not game_over:
      elapsed_ms = pygame.time.get_ticks() - start_ticks
      elapsed_sec = elapsed_ms // 1000
      remaining_time = max(0, 10 - elapsed_sec) 

    remaining_time = max(0, 10 - elapsed_sec)
    down_time = max(0, 300000000000000 - elapsed_sec)

    if remaining_time == 0 and not game_paused:
        print("Time's up!")
        game_paused = True
        background_img = pygame.image.load("shop.png").convert()
        background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))



    if down_time == 0 and game_paused:
        print("Down time is over")
        start_ticks = pygame.time.get_ticks()
        game_paused = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q] and game_paused:
        start_ticks = pygame.time.get_ticks()
        game_paused = False
        wave += 1
        background_img = pygame.image.load("image.png").convert()
        background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        countdown_active = True
        countdown_start_ticks = pygame.time.get_ticks()

    if not game_paused and not game_over:
        if keys[pygame.K_a]:
            player_x -= player_speed_x
        if keys[pygame.K_d]:
            player_x += player_speed_x
        if keys[pygame.K_w]:
            player_y -= player_speed_y
        if keys[pygame.K_s]:
            player_y += player_speed_y

        weapon_angle = (weapon_angle + 5) % 360

        weapon_x = player_x + PLAYER_WIDTH / 3.5 + weapon_radius * math.cos(math.radians(weapon_angle)) - WEAPON_WIDTH / 2
        weapon_y = player_y + PLAYER_HEIGHT / 3.5 + weapon_radius * math.sin(math.radians(weapon_angle)) - WEAPON_HEIGHT / 2
        rotated_weapon_img = pygame.transform.rotate(weapon_img, -weapon_angle)
        rotated_rect = rotated_weapon_img.get_rect(center=(weapon_x + WEAPON_WIDTH / 2, weapon_y + WEAPON_HEIGHT / 2))
        weapon_mask = pygame.mask.from_surface(rotated_weapon_img)

        player_x = max(0, min(player_x, SCREEN_WIDTH - PLAYER_WIDTH))
        player_y = max(60, min(player_y, SCREEN_HEIGHT - PLAYER_HEIGHT))
        for monster in monsters:
         monster["x"] = max(0, min(monster["x"], SCREEN_WIDTH - MONSTER_WIDTH))
         monster["y"] = max(60, min(monster["y"], SCREEN_HEIGHT - MONSTER_HEIGHT))

        for i, monster in enumerate(monsters):
            dx = player_x - monster["x"]
            dy = player_y - monster["y"]
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx /= distance
                dy /= distance
                monster["x"] += dx * monster["speed"]
                monster["y"] += dy * monster["speed"]

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

    # Altijd de achtergrond tonen (game of shop)
    screen.blit(background_img, (0, 0))

    if not game_paused:
      screen.blit(player_img, (player_x, player_y))
      screen.blit(rotated_weapon_img, rotated_rect.topleft)

    # Coins-icoon
    screen.blit(coin_img, (960, 10))

    # Monsters tekenen
    if not game_paused:
     for monster in monsters:
        screen.blit(Monster_img, (monster["x"], monster["y"]))

    # HUD
    timer_text = font.render(f'Time left: {remaining_time}s', True, (255, 255, 255))
    screen.blit(timer_text, (270, 10)) 
    wave_text = font.render(f'Wave: {wave}', True, (255, 255, 255))
    screen.blit(wave_text, (550, 10))
    coin_text = font.render(f'Coins: {coins}', True, (255, 255, 255))
    screen.blit(coin_text, (800, 10))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (1080, 10))

    # Hartjes
    for i in range(lives):
        screen.blit(heart_img, (39 + i * (HEART_WIDTH + 10), 5))

    for monster in monsters:
        if not game_paused and not game_over:
            HITBOX_OFFSET = 72
            if (monster["x"] + MONSTER_WIDTH - HITBOX_OFFSET > player_x and
                monster["x"] + HITBOX_OFFSET < player_x + PLAYER_WIDTH and
                monster["y"] + MONSTER_HEIGHT - HITBOX_OFFSET > player_y and
                monster["y"] + HITBOX_OFFSET < player_y + PLAYER_HEIGHT):
                for monster in monsters:
                    monster["x"] += 300
                    monster["y"] += 300
                print(f"Monster pakt speler!")
                if lives > 0:
                    lives -= 1


            # Maak een masker aan van het monsteroppervlak
            monster_surface = pygame.Surface((MONSTER_WIDTH, MONSTER_HEIGHT), pygame.SRCALPHA)
            monster_surface.blit(Monster_img, (0, 0))
            monster_mask = pygame.mask.from_surface(monster_surface)

            # Positieverschil tussen zwaard en monster
            offset_x = int(monster["x"] - rotated_rect.left)
            offset_y = int(monster["y"] - rotated_rect.top)

            if weapon_mask.overlap(monster_mask, (offset_x, offset_y)):
             print("Monster geraakt door zwaard!")
             coins += 1
             score += 10
             dx = monster["x"] - weapon_x
             dy = monster["y"] - weapon_y
             distance = math.hypot(dx, dy)
             if distance != 0:
                 dx /= distance
                 dy /= distance
                 monster["x"] += dx * bounce_strength
                 monster["y"] += dy * bounce_strength

   
    if game_paused:
        big_font = pygame.font.SysFont('default', 140)
        mid_font = pygame.font.SysFont('default', 55)
        pause_text = font.render('Druk op "Q" om naar de volgende wave te gaan!', True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2 ))
        pygame.draw.rect(screen, (0,0,0), text_rect.inflate(20, 20))
        screen.blit(pause_text, text_rect)
        price_text = big_font.render('5', True, (0, 0, 0))
        text_rect = price_text.get_rect(topleft=(295, 450))
        screen.blit(price_text, text_rect)
        price_text1 = big_font.render('10', True, (0, 0, 0))
        text_rect = price_text1.get_rect(topleft=(540, 440))
        screen.blit(price_text1, text_rect)
        price_text2 = big_font.render('20', True, (0, 0, 0))
        text_rect = price_text2.get_rect(topleft=(835, 445))
        screen.blit(price_text2, text_rect)
        press_text = mid_font.render('Press Z', True, (0, 0, 0))
        text_rect = press_text.get_rect(topleft=(258, 50))
        screen.blit(press_text, text_rect)
        press_text1 = mid_font.render('Press X', True, (0, 0, 0))
        text_rect = press_text1.get_rect(topleft=(518, 50))
        screen.blit(press_text1, text_rect)
        press_text2 = mid_font.render('Press C', True, (0, 0, 0))
        text_rect = press_text2.get_rect(topleft=(818, 50))
        screen.blit(press_text2, text_rect)

    if keys[pygame.K_z] and game_paused and coins >= 5 and lives < 3:
        lives += 1
        coins -= 5
    if keys[pygame.K_x] and game_paused and coins >= 10 and buyteller == 1 and wave_delay == 0:
        WEAPON_HEIGHT += 150
        WEAPON_WIDTH += 150
        weapon_img = pygame.Surface((100, 150), pygame.SRCALPHA)
        weapon_img.blit(spritesheet5, (0, 0), (0, 0, 1111, 1100))
        weapon_img = pygame.transform.scale(weapon_img, (WEAPON_WIDTH, WEAPON_HEIGHT))
        coins -= 10
        buyteller -= 1
        if wave +1:
            wave_delay += 1
    if keys[pygame.K_x] and game_paused and coins >= 10 and buyteller == 0 and wave_delay == 1:
        WEAPON_HEIGHT += 150
        WEAPON_WIDTH += 150
        weapon_img = pygame.Surface((100, 150), pygame.SRCALPHA)
        weapon_img.blit(spritesheet6, (0, 0), (0, 0, 1111, 1100))
        weapon_img = pygame.transform.scale(weapon_img, (WEAPON_WIDTH, WEAPON_HEIGHT))
        coins -= 10
        buyteller -= 1


    if lives <= 0:
       game_over = True
    
    if game_over:
        game_text = font.render("GAME OVER - Druk op 'R' om opnieuw te starten", True, (255, 255, 255))
        text_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(20, 20))
        screen.blit(game_text, text_rect)

        if keys[pygame.K_r]:
            # Reset variabelen
            lives = 3
            buyteller = 1
            wave = 1
            coins = 0
            score = 0
            player_x = SCREEN_WIDTH / 2
            player_y = SCREEN_HEIGHT - 100
            weapon_angle = 0
            countdown_active = True
            countdown_start_ticks = pygame.time.get_ticks()
            background_img = pygame.image.load("image.png").convert()
            background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            monsters = []
            for i in range(MONSTER_COUNT):
                monsters.append({
                    "x": random.randint(0, SCREEN_WIDTH - MONSTER_WIDTH),
                    "y": random.randint(0, SCREEN_HEIGHT - MONSTER_HEIGHT),
                    "speed": 5
                })
            game_paused = False
            game_over = False
 
    pygame.display.flip()
    fps_clock.tick(FPS)


print('mygame stopt running')
