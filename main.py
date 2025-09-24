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
MONSTER_COUNT = 0
WEAPON_WIDTH = 80
WEAPON_HEIGHT = 140
EXTRA_WEAPON_HEIGHT = 140
EXTRA_WEAPON_WIDTH = 80
HEART_WIDTH = 50
HEART_HEIGHT = 50
COIN_WIDTH = 40
COIN_HEIGHT = 40
weapon_angle = 0  # initial angle in degrees
weapon_radius = 100  # distance from player to weapon center
bounce_strength = 200
lives = 3
wave = 1
coins = 0
score = 0
buyteller = 1
wave_delay = 0
last_purchase_time = 0
purchase_cooldown = 800
in_menu = True
extra_weapon_unlocked = False  
extra_weapon_angle = 180       

# --- Functie om monsters te maken ---
def spawn_monsters(count):
    monsters = []
    for i in range(count):
        monsters.append({
            "x": random.randint(0, 100),
            "y": random.randint(0, 100),
            "speed": 4
        })
    return monsters

#Cooldown functie
def can_purchase():
    global last_purchase_time
    current_time = pygame.time.get_ticks()
    if current_time - last_purchase_time >= purchase_cooldown:
        last_purchase_time = current_time
        return True
    return False

#Tussenscherm
def show_between_wave_screen():
    """Tekent het tussenscherm en retourneert de yes/no rects."""
    # achtergrond
    screen.blit(between_wave_bg, (0, 0))

    # Titel (boven midden)
    font_big = pygame.font.SysFont("default", 48)
    title_text = font_big.render("Congratulations! You have made it to the next wave!", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
    screen.blit(title_text, title_rect)

    # Vraag onder de titel
    font_small = pygame.font.SysFont("default", 36)
    question = font_small.render("Would you like to go to the shop?", True, (255, 255, 255))
    question_rect = question.get_rect(center=(SCREEN_WIDTH // 2, 180))
    screen.blit(question, question_rect)

    # Ja / Nee knoppen (onder de vraag)
    yes_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, 260, 100, 50)
    no_rect  = pygame.Rect(SCREEN_WIDTH//2 + 20, 260, 100, 50)

    pygame.draw.rect(screen, (0, 200, 0), yes_rect)  # groen
    pygame.draw.rect(screen, (200, 0, 0), no_rect)   # rood

    yes_text = font_small.render("Yes", True, (0, 0, 0))
    no_text  = font_small.render("No", True, (0, 0, 0))

    screen.blit(yes_text, (yes_rect.centerx - yes_text.get_width()//2,
                           yes_rect.centery - yes_text.get_height()//2))
    screen.blit(no_text, (no_rect.centerx - no_text.get_width()//2,
                          no_rect.centery - no_text.get_height()//2))

    # Karakter naast de tekst: gebruik geselecteerde character of standaard speler
    char_img = selected_character_img if selected_character_img else player_img
    # teken links van de tekst (center Y met question)
    char_x = SCREEN_WIDTH//2 - 350
    char_y = 180
    screen.blit(char_img, (char_x, char_y))

    return yes_rect, no_rect

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
extra_rect = pygame.Rect(0, 0, WEAPON_WIDTH, WEAPON_HEIGHT)
rotated_extra_weapon_img = pygame.Surface((EXTRA_WEAPON_WIDTH, EXTRA_WEAPON_HEIGHT), pygame.SRCALPHA)

# INIT PYGAME
pygame.init()
font = pygame.font.SysFont('default', 50)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# ---- INTRO SCHERM VARIABELEN ----
in_intro = True
intro_background = pygame.image.load("beginscherm1.png").convert()
intro_background = pygame.transform.scale(intro_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

intro_title_font = pygame.font.SysFont("default", 80)
intro_text_font = pygame.font.SysFont("default", 40)

intro_title = "Wanted in Greece!"

intro_texts = [
    "Welcome brave warrior!\nYou have been chosen by us, the Greek gods, to elimenate a great threat.\nThere are dangerous monsters in these woods\nand you may be greeces final hope.\n\n\n\n\nPress Enter to continue ",
    "Now great warrior you have to learn to control yourself.\nYou can use W, to move up, A to go left,\nS to go down and D to go right.\nYou will have 3 hearts, everytime you touch a\nmonster you shall lose a heart.\nThis might prove harder than it seems.\n\n\nPress Enter to continue",
    "You also have a weapon that cirkels around you.\nThat might help you get rid of those foul creatures.\nIf you manage to hit a creature i will bless you with some\nPrecisely Ordered Indicators Nudging Toward Scores.\nBut you may call them points.\nIf you have 500 points you win!\n\n\nPress Enter to continue",
    "Monsters naturaly spawn coins when you hit them.\nSo save up and you may be able to buy some interesting stuff in the shop.\n\n\n\n\n\n\nPress Enter to continue ",
    "We have selected multiple challenges for you to complete.\nYou need to prove your worthy by completing the easier raids\nto be able to do the harder ones.\n\n\n\n\n\nPress Enter to continue"
]

current_text_index = 0
displayed_text = ""
char_index = 0
typing_speed = 50  # ms per letter
last_update = pygame.time.get_ticks()
waiting_for_enter = False
enter_cooldown = 0
ENTER_COOLDOWN_TIME = 300  # milliseconden (0.3s), pas aan naar smaak


# KARAKTER KEUZE
in_character_select = False   # Staat voor karakterkeuze scherm
selected_character_img = None
character_images = [
    pygame.image.load("Player.png").convert_alpha(),
    pygame.image.load("player2.png").convert_alpha(),
    pygame.image.load("player3.png").convert_alpha(),
    pygame.image.load("player4.png").convert_alpha(),
    pygame.image.load("sanic.png").convert_alpha()
]
# Schaal alle characters naar dezelfde grootte als de speler
for i in range(len(character_images)):
    character_images[i] = pygame.transform.scale(character_images[i], (PLAYER_WIDTH, PLAYER_HEIGHT))

character_rects = []  # hier komen de klikgebieden van de characters

# LAAD SPRITESHEET
spritesheet = pygame.image.load('Player.png').convert_alpha()
spritesheet1 = pygame.image.load("monster.png").convert_alpha()
spritesheet2 = pygame.image.load("weapon2.png").convert_alpha()
spritesheet3 = pygame.image.load('heart.png').convert_alpha()
spritesheet4 = pygame.image.load('coin.png').convert_alpha()
spritesheet5 = pygame.image.load("legendary_sword.png").convert_alpha()
spritesheet6 = pygame.image.load("HAMMER.png").convert_alpha()
extrasword_spritesheet = pygame.image.load("extrasword.png").convert_alpha()
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

#keuze menu achtergrond
menu_background = pygame.image.load("keuzemenu.png").convert()
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
difficulty = pygame.image.load("difficulty.png").convert()
difficulty = pygame.transform.scale(difficulty, (SCREEN_WIDTH, SCREEN_HEIGHT))

# HEART AFBEELDING
heart_img = pygame.Surface((100, 100), pygame.SRCALPHA)
heart_img.blit(spritesheet3, (0, 0), (0, 0, 100, 100))
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

# COINS AFBEELDING
coin_img = pygame.Surface((40, 40), pygame.SRCALPHA)
coin_img.blit(spritesheet4, (0, 0), (0, 0, 40, 40))
coin_img = pygame.transform.scale(coin_img, (COIN_WIDTH, COIN_HEIGHT))
# lock afbeelding
lock_img = pygame.image.load("Lock.png").convert_alpha()
lock_img = pygame.transform.scale(lock_img, (100, 100))  # adjust size to fit nicely

#Extra sword
extra_weapon_img = pygame.Surface((EXTRA_WEAPON_WIDTH, EXTRA_WEAPON_HEIGHT), pygame.SRCALPHA)
extra_weapon_img.blit(extrasword_spritesheet, (0, 0), (0, 0, 100, 150))
extra_weapon_img = pygame.transform.scale(extra_weapon_img, (EXTRA_WEAPON_WIDTH, EXTRA_WEAPON_HEIGHT))
rotated_extra_weapon_img = extra_weapon_img.copy()

# (na) background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
between_wave_bg = pygame.image.load("tussenscherm.png").convert()
between_wave_bg = pygame.transform.scale(between_wave_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))



# MEERDERE MONSTERS AANMAKEN
monsters = []
for i in range(MONSTER_COUNT):
    monsters.append({
        "x": random.randint(0, 100),
        "y": random.randint(0, 100),
        "speed": 4
    })

background_img = pygame.image.load("image.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

print('mygame is running')

start_ticks = pygame.time.get_ticks() 
game_paused = False
game_over = False
game_won = False
in_between_wave = False
easy_unlocked = True
medium_unlocked = False
hard_unlocked = False
countdown_active = True
countdown_start_ticks = pygame.time.get_ticks()

running = True
enter_cooldown = 200  # cooldown in ms voor Enter

while running:
    # --- Tussenscherm afhandelen (voorkomt dat rest van game doorloopt) ---
    if in_between_wave:
        # teken scherm + krijg knop rects terug
        yes_rect, no_rect = show_between_wave_screen()
        pygame.display.flip()

        # events alleen voor tussenscherm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if yes_rect.collidepoint(mouse_pos):
                    # ga naar shop
                    in_between_wave = False
                    game_paused = True
                    background_img = pygame.image.load("shop.png").convert()
                    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    # (optioneel) reset last_purchase_time zodat shop direct werkt
                    last_purchase_time = pygame.time.get_ticks()
                elif no_rect.collidepoint(mouse_pos):
                    # ga direct verder met de volgende wave
                    in_between_wave = False
                    # volg dezelfde flow als bij Q: start countdown naar next wave
                    wave += 1
                    countdown_active = True
                    countdown_start_ticks = pygame.time.get_ticks()
                    background_img = pygame.image.load("image.png").convert()
                    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        fps_clock.tick(FPS)
        continue   # heel belangrijk: skip rest van de loop zolang tussenscherm actief
    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_character_select and event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(character_rects):
                if rect.collidepoint(event.pos):
                    selected_character_img = character_images[i]
                    player_img = selected_character_img
                    in_character_select = False
                    in_menu = True

    keys = pygame.key.get_pressed()

    # ---------------- ENTER COOLDOWN ----------------
    if enter_cooldown > 0:
        enter_cooldown -= fps_clock.get_time()

    # ---------------- INTRO ----------------
    if in_intro:
        screen.blit(intro_background, (0, 0))

        # Titel tekenen
        title_surface = intro_title_font.render(intro_title, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Typewriter effect
        if not waiting_for_enter:
            now = pygame.time.get_ticks()
            if now - last_update > typing_speed:
                if char_index < len(intro_texts[current_text_index]):
                    displayed_text += intro_texts[current_text_index][char_index]
                    char_index += 1
                    last_update = now
                else:
                    waiting_for_enter = True

        # Tekst tekenen (meerdere regels mogelijk)
        lines = displayed_text.split("\n")
        y_offset = 0
        for line in lines:
            text_surface = intro_text_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset - 190))
            screen.blit(text_surface, text_rect)
            y_offset += 50

        # ENTER → alles tonen of naar volgende tekst
        if keys[pygame.K_RETURN] and enter_cooldown <= 0:
            enter_cooldown = 200  # reset cooldown
            if not waiting_for_enter:
                # toon direct alle tekst
                displayed_text = intro_texts[current_text_index]
                waiting_for_enter = True
            else:
                # ga naar volgende tekst
                current_text_index += 1
                if current_text_index >= len(intro_texts):
                    in_intro = False
                    in_character_select = True
                else:
                    displayed_text = ""
                    char_index = 0
                    waiting_for_enter = False

        pygame.display.flip()
        fps_clock.tick(FPS)
        continue  # stop hier, ga niet verder naar menu/game

  # ---------------- KARAKTER SELECTIE ----------------
    if in_character_select:
        if in_menu:
         screen.blit(menu_background, (0, 0))
         title_text = font.render("Choose a Character by clicking on it!", True, (255, 255, 255))
         title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
         screen.blit(title_text, title_rect)

        # Plaats characters horizontaal
        character_rects = []
        spacing = 50
        start_x = (SCREEN_WIDTH - (PLAYER_WIDTH * len(character_images) + spacing * (len(character_images)-1))) // 2
        y_pos = SCREEN_HEIGHT // 2
        for i, img in enumerate(character_images):
            x_pos = start_x + i * (PLAYER_WIDTH + spacing)
            rect = pygame.Rect(x_pos, y_pos, PLAYER_WIDTH, PLAYER_HEIGHT)
            character_rects.append(rect)
            screen.blit(img, (x_pos, y_pos))

        # Hover effect: gele rand
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(character_rects):
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 0), rect, 4)

        pygame.display.flip()
        fps_clock.tick(FPS)
        continue  # stop hier, ga niet verder naar menu/game

    # ---------------- MENU SCHERM ----------------
    if in_menu:
        screen.blit(difficulty, (0,0))
        title_text = font.render("Choose a Level by clicking on it!", True, (255, 255, 255))
        easy_text = font.render("Easy (3 monsters)", True, (255, 255, 255))
        medium_text = font.render("Medium (5 monsters)", True, (255, 255, 255))
        hard_text = font.render("Hard (7 monsters)", True, (255, 255, 255))

        # Rectangles (klikgebieden)
        easy_rect = easy_text.get_rect(center=(SCREEN_WIDTH//5, 400))
        medium_rect = medium_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        hard_rect = hard_text.get_rect(center=(SCREEN_WIDTH//1.29, 400))

        mouse_pos = pygame.mouse.get_pos()

        # Easy is always available
        if easy_rect.collidepoint(mouse_pos):
            easy_text = font.render("Easy (3 monsters)", True, (0, 255, 0))

        # Medium only if unlocked
        if medium_unlocked:
            if medium_rect.collidepoint(mouse_pos):
                medium_text = font.render("Medium (5 monsters)", True, (255, 255, 0))
        else:
            medium_text = font.render("Medium (LOCKED)", True, (128, 128, 128))
            lock_pos = medium_rect.center
            lock_rect = lock_img.get_rect(center=lock_pos)
            screen.blit(lock_img, lock_rect)

        # Hard only if unlocked
        if hard_unlocked:
            if hard_rect.collidepoint(mouse_pos):
                hard_text = font.render("Hard (7 monsters)", True, (255, 0, 0))
        else:
            hard_text = font.render("Hard (LOCKED)", True, (128, 128, 128))
            lock_pos = hard_rect.center
            lock_rect = lock_img.get_rect(center=lock_pos)
            screen.blit(lock_img, lock_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if easy_rect.collidepoint(mouse_pos):
                MONSTER_COUNT = 3
                monsters = spawn_monsters(MONSTER_COUNT)
                in_menu = False
                countdown_active = True
                countdown_start_ticks = pygame.time.get_ticks()

            elif medium_rect.collidepoint(mouse_pos) and medium_unlocked:
                MONSTER_COUNT = 5
                monsters = spawn_monsters(MONSTER_COUNT)
                in_menu = False
                countdown_active = True
                countdown_start_ticks = pygame.time.get_ticks()

            elif hard_rect.collidepoint(mouse_pos) and hard_unlocked:
                 MONSTER_COUNT = 7
                 monsters = spawn_monsters(MONSTER_COUNT)

                 # Laad hele monster2.png
                 Monster_img = pygame.image.load("monster2.png").convert_alpha()
                 Monster_img = pygame.transform.scale(Monster_img, (MONSTER_WIDTH, MONSTER_HEIGHT))

                 # Geef monsters extra snelheid
                 for monster in monsters:
                      monster["speed"] += 1.5

                 in_menu = False
                 countdown_active = True
                 countdown_start_ticks = pygame.time.get_ticks()

        # Teksten tekenen
        screen.blit(title_text, (400, 25))
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)

        mouse_pos = pygame.mouse.get_pos()

        if easy_rect.collidepoint(mouse_pos):
          easy_text = font.render("Easy (3 monsters)", True, (0, 255, 0))  # Groen hover
        if medium_rect.collidepoint(mouse_pos):
          medium_text = font.render("Medium (5 monsters)", True, (255, 255, 0))  # Geel hover
        if hard_rect.collidepoint(mouse_pos):
          hard_text = font.render("Hard (7 monsters)", True, (255, 0, 0))  # Rood hover

        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)

        pygame.display.flip()
        continue  # << stop de loop hier, ga NIET door naar game

    # ---------------- COUNTDOWN ----------------
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

            # Tekst in het midden
            text_surface = font.render(countdown_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(40, 20))
            screen.blit(text_surface, text_rect)

            pygame.display.flip()
            fps_clock.tick(FPS)
            continue  # << stop hier, wacht tot countdown voorbij is
        else:
            countdown_active = False
            start_ticks = pygame.time.get_ticks()  # Game timer resetten na countdown


    if not game_over:
      elapsed_ms = pygame.time.get_ticks() - start_ticks
      elapsed_sec = elapsed_ms // 1000
      remaining_time = max(0, 15 - elapsed_sec) 

    remaining_time = max(0, 15 - elapsed_sec)
    down_time = max(0, 300000000000000 - elapsed_sec)

    if remaining_time == 0 and not game_paused:
        in_between_wave = True


    if down_time == 0 and game_paused:
        print("Down time is over")
        start_ticks = pygame.time.get_ticks()
        game_paused = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q] and game_paused and not game_won:
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
    pygame.display.flip()
    if extra_weapon_unlocked and not game_paused and not game_over and not game_won:
     extra_weapon_angle = (extra_weapon_angle + 5) % 360  # draait rond speler
     extra_weapon_x = player_x + PLAYER_WIDTH / 3.5 + weapon_radius * math.cos(math.radians(extra_weapon_angle)) - EXTRA_WEAPON_WIDTH / 2
     extra_weapon_y = player_y + PLAYER_HEIGHT / 3.5 + weapon_radius * math.sin(math.radians(extra_weapon_angle)) - EXTRA_WEAPON_HEIGHT / 2
     rotated_extra_weapon_img = pygame.transform.rotate(extra_weapon_img, -extra_weapon_angle)
     extra_rect = rotated_extra_weapon_img.get_rect(center=(extra_weapon_x + EXTRA_WEAPON_WIDTH / 2, extra_weapon_y + EXTRA_WEAPON_HEIGHT / 2))
     screen.blit(rotated_extra_weapon_img, extra_rect.topleft)
    
    
    # Altijd de achtergrond tonen (game of shop)
    screen.blit(background_img, (0, 0))

    if not game_paused:
      screen.blit(player_img, (player_x, player_y))
      screen.blit(rotated_weapon_img, rotated_rect.topleft)
      if extra_weapon_unlocked:
        screen.blit(rotated_extra_weapon_img, extra_rect.topleft)

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
    # ------------------------
    # Kleiner hitbox voor speler en monster
    # ------------------------
     player_rect = pygame.Rect(
        player_x + PLAYER_WIDTH * 0.1,
        player_y + PLAYER_HEIGHT * 0.1,
        PLAYER_WIDTH * 0.7,
        PLAYER_HEIGHT * 0.7
    )

     monster_rect = pygame.Rect(
        monster["x"] + MONSTER_WIDTH * 0.15,
        monster["y"] + MONSTER_HEIGHT * 0.15,
        MONSTER_WIDTH * 0.7,
        MONSTER_HEIGHT * 0.7
    )

    # ------------------------
    # Weapon rect en mask
    # ------------------------
     weapon_rect = rotated_weapon_img.get_rect(center=(weapon_x + WEAPON_WIDTH / 2,
                                                      weapon_y + WEAPON_HEIGHT / 2))

    # Maskers
     weapon_mask = pygame.mask.from_surface(rotated_weapon_img)

     monster_surface = pygame.Surface((MONSTER_WIDTH, MONSTER_HEIGHT), pygame.SRCALPHA)
     monster_surface.blit(Monster_img, (0, 0))
     monster_mask = pygame.mask.from_surface(monster_surface)

    # ------------------------
    # Collision: speler ↔ monster
    # ------------------------
     if player_rect.colliderect(monster_rect):
        # Duw monsters weg
        for m in monsters:
            m["x"] += 300
            m["y"] += 300

        print("Monster pakt speler!")
        if lives > 0:
            lives -= 1

    # ------------------------
    # Collision: weapon ↔ monster
    # ------------------------
    # Bereken offset voor mask overlap
     offset_x = monster_rect.left - weapon_rect.left
     offset_y = monster_rect.top - weapon_rect.top

     if weapon_mask.overlap(monster_mask, (offset_x, offset_y)):
        print("Monster geraakt door zwaard!")
        coins += 1
        score += 10

        # Bounce effect
        dx = monster["x"] - weapon_x
        dy = monster["y"] - weapon_y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance
            monster["x"] += dx * bounce_strength
            monster["y"] += dy * bounce_strength
    
     if extra_weapon_unlocked:
         # Gebruik het extra wapen mask en rect die net hierboven zijn aangemaakt
         offset_x = monster_rect.left - extra_rect.left
         offset_y = monster_rect.top - extra_rect.top
         extra_weapon_mask = pygame.mask.from_surface(rotated_extra_weapon_img)
         if extra_weapon_mask.overlap(monster_mask, (offset_x, offset_y)):
          coins += 1
          score += 10
          dx = monster["x"] - extra_weapon_x
          dy = monster["y"] - extra_weapon_y
          distance = math.hypot(dx, dy)
          if distance != 0:
            dx /= distance
            dy /= distance
            monster["x"] += dx * bounce_strength
            monster["y"] += dy * bounce_strength


    # ------------------------
    # Winconditie
    # ------------------------
     if score >= 500 and not game_won:
        game_won = True
        game_paused = True

        # Maak een masker aan van het monsteroppervlak
        monster_surface = pygame.Surface((MONSTER_WIDTH, MONSTER_HEIGHT), pygame.SRCALPHA)
        monster_surface.blit(Monster_img, (0, 0))
        monster_mask = pygame.mask.from_surface(monster_surface)

        # Positieverschil tussen wapen en monster
        offset_x = int(monster["x"] - rotated_rect.left)
        offset_y = int(monster["y"] - rotated_rect.top)

        if weapon_mask.overlap(monster_mask, (offset_x, offset_y)):
            print("Monster geraakt door zwaard!")
            coins += 1
            score += 10

            # Bounce effect
            dx = monster["x"] - weapon_x
            dy = monster["y"] - weapon_y
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx /= distance
                dy /= distance
                monster["x"] += dx * bounce_strength
                monster["y"] += dy * bounce_strength

        if score >= 500 and not game_won:
            game_won = True
            game_paused = True

   
    # ------------------------ SHOP ------------------------
    if game_paused and not game_won:
        big_font = pygame.font.SysFont('default', 140)
        mid_font = pygame.font.SysFont('default', 55)

        # Titel
        pause_text = font.render('Press Q to go to the next wave!', True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
        screen.blit(pause_text, text_rect)

        pause_text = font.render('Click the text below to buy.', True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 110))
        screen.blit(pause_text, text_rect)

        #Sanji text
        pause_text = font.render('Welcome to Sanji\'s shop hero!', True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(pause_text, text_rect)

        # Items Click Here
        item1_text = mid_font.render("extra heart", True, (255, 255, 255))
        item1_rect = item1_text.get_rect(topleft=(170, 600))
        screen.blit(item1_text, item1_rect)

        item2_text = mid_font.render("new weapon", True, (255, 255, 255))
        item2_rect = item2_text.get_rect(topleft=(518, 600))
        screen.blit(item2_text, item2_rect)

        item3_text = mid_font.render("extra weapon", True, (255, 255, 255))
        item3_rect = item3_text.get_rect(topleft=(898, 600))
        screen.blit(item3_text, item3_rect)

        # Hover effect
        mouse_pos = pygame.mouse.get_pos()

        # Item 1
        if item1_rect.collidepoint(mouse_pos):
            if coins >= 5 and lives < 3:
                hover_text = mid_font.render("Buy", True, (0, 200, 0))
            elif coins >= 5 and lives == 3:
                hover_text = mid_font.render("Already 3 hearts!", True, (0, 200, 0))
            else:
                hover_text = mid_font.render("Not enough coins", True, (200, 0, 0))
            hover_rect = hover_text.get_rect(center=(item1_rect.centerx, item1_rect.bottom + 30))
            screen.blit(hover_text, hover_rect)

        # Item 2 hover
        if item2_rect.collidepoint(mouse_pos):
                if buyteller == 1 and wave_delay == 0 and coins >= 10:
                    hover_text = mid_font.render("Buy Legendary Sword", True, (0, 200, 0))
                elif buyteller == 0 and wave_delay == 1 and coins >= 10:
                    hover_text = mid_font.render("Buy Hammer", True, (0, 200, 0))
                elif buyteller == -1 and wave_delay == 1 and coins >= 10:
                    hover_text = mid_font.render("Sold out!", True, (200, 0, 0))
                else:
                        hover_text = mid_font.render("Not enough coins", True, (200, 0, 0))
                hover_rect = hover_text.get_rect(center=(item2_rect.centerx, item2_rect.bottom + 30))
                screen.blit(hover_text, hover_rect)

        # Item 3
        if item3_rect.collidepoint(mouse_pos):
            if coins >= 20 and not extra_weapon_unlocked:
                hover_text = mid_font.render("Buy", True, (0, 200, 0))
            elif coins >= 20 and  extra_weapon_unlocked:
                hover_text = mid_font.render("Already bought!", True, (200, 0, 0))
            else:
                hover_text = mid_font.render("Not enough coins", True, (200, 0, 0))
            hover_rect = hover_text.get_rect(center=(item3_rect.centerx, item3_rect.bottom + 30))
            screen.blit(hover_text, hover_rect)

        # Klik detectie
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Item 1: extra hart
            if item1_rect.collidepoint(mouse_pos) and coins >= 5 and lives < 3:
                if can_purchase():
                    lives += 1
                    coins -= 5
                    last_purchase_time = pygame.time.get_ticks()

            # Item 2: Legendary Sword of Hammer
            elif item2_rect.collidepoint(mouse_pos) and coins >= 10:
                if buyteller == 1 and wave_delay == 0:
                    #Legandarysword kopen
                    if can_purchase():
                        WEAPON_HEIGHT += 190
                        WEAPON_WIDTH += 190
                        weapon_img = pygame.Surface((100, 150), pygame.SRCALPHA)
                        weapon_img.blit(spritesheet5, (0, 0), (0, 0, 1111, 1100))
                        weapon_img = pygame.transform.scale(weapon_img, (WEAPON_WIDTH, WEAPON_HEIGHT))
                        coins -= 10
                        buyteller -= 1
                        wave_delay += 1
                        last_purchase_time = pygame.time.get_ticks()
                elif buyteller == 0 and wave_delay == 1:
                    # Koop Hammer
                    if can_purchase():
                        WEAPON_WIDTH -= 180
                        WEAPON_HEIGHT -= 180
                        weapon_img = pygame.Surface((100, 150), pygame.SRCALPHA)
                        weapon_img.blit(spritesheet6, (0, 0), (0, 0, 1111, 1100))
                        weapon_img = pygame.transform.scale(weapon_img, (WEAPON_WIDTH, WEAPON_HEIGHT))
                        coins -= 10
                        buyteller -= 1
                        last_purchase_time = pygame.time.get_ticks()

            # Item 3: Extra wapen
            elif item3_rect.collidepoint(mouse_pos) and coins >= 20 and not extra_weapon_unlocked:
                if can_purchase(): 
                    coins -= 20
                    extra_weapon_unlocked = True


    current_time = pygame.time.get_ticks()

    if lives <= 0:
       game_over = True
    
    if game_over:
        game_text = font.render("GAME OVER - Press 'R' to restart!", True, (255, 255, 255))
        text_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(20, 20))
        screen.blit(game_text, text_rect)

        if keys[pygame.K_r]:
            # Reset variabelen
            lives = 3
            buyteller = 1
            wave_delay = 0
            wave = 1
            coins = 0
            score = 0
            player_x = SCREEN_WIDTH / 2
            player_y = SCREEN_HEIGHT - 100
            weapon_angle = 0
            WEAPON_WIDTH = 100
            WEAPON_HEIGHT = 150
            weapon_img = pygame.Surface((100, 150), pygame.SRCALPHA)
            weapon_img.blit(spritesheet2, (0, 0), (0, 0, 100, 150))
            weapon_img = pygame.transform.scale(weapon_img, (WEAPON_WIDTH, WEAPON_HEIGHT))
            countdown_active = True
            countdown_start_ticks = pygame.time.get_ticks()
            background_img = pygame.image.load("image.png").convert()
            background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            monsters = []
            for i in range(MONSTER_COUNT):
                monsters.append({
                    "x": random.randint(0, 100),
                    "y": random.randint(0, 100),
                    "speed": 5
                })
            game_paused = False
            game_over = False
            in_menu = True
            extra_weapon_unlocked = False
            extra_weapon_angle = 180

    if game_won:
    # Unlock next difficulty only on win
        if MONSTER_COUNT == 3:   # Easy beaten
            medium_unlocked = True
        elif MONSTER_COUNT == 5: # Medium beaten
            hard_unlocked = True

        win_text = font.render("YOU WIN! - Press 'R' to restart", True, (255, 255, 0))
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(20, 20))
        screen.blit(win_text, text_rect)

        if keys[pygame.K_r]:
        # Reset variables (same as game over reset)
            lives = 3
            buyteller = 1
            wave_delay = 0
            wave = 1
            coins = 0
            score = 0
            player_x = SCREEN_WIDTH / 2
            player_y = SCREEN_HEIGHT - 100
            weapon_angle = 0
            WEAPON_WIDTH = 100
            WEAPON_HEIGHT = 150
            weapon_img = pygame.Surface((100, 150), pygame.SRCALPHA)
            weapon_img.blit(spritesheet2, (0, 0), (0, 0, 100, 150))
            weapon_img = pygame.transform.scale(weapon_img, (WEAPON_WIDTH, WEAPON_HEIGHT))
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
            game_won = False
            in_menu = True
            extra_weapon_unlocked = False
            

    pygame.display.flip()
    fps_clock.tick(FPS)


print('mygame stopt running')