import pygame
import config
from classes import Button, TextInputBox
from functions import reset_game

# ----------------- UI Elements dl Menu -----------------
# Khalfia k7la ou 3 itarat (Frames) mtstaqllin (Kblna l'3rd bach ykfi kolchi)
frame_w = 460
frame_x = config.screenWidth // 2 - frame_w // 2

# 1. NAME FRAME (y=65, h=45)
name_frame_y = 65
name_frame_h = 45
name_input = TextInputBox(config.screenWidth // 2 - 20, name_frame_y + 8, 180, 28)

# 2. DIFFICULTY FRAME (y=120, h=45)
diff_frame_y = 120
diff_frame_h = 45
btn_w = 100
btn_h = 28
easy_btn = Button(config.screenWidth // 2 - 140, diff_frame_y + 8, btn_w, btn_h, "EASY", config.GREEN, config.BLACK)
normal_btn = Button(config.screenWidth // 2 - 20, diff_frame_y + 8, btn_w, btn_h, "NORMAL", config.WHITE, config.BLACK)
hard_btn = Button(config.screenWidth // 2 + 100, diff_frame_y + 8, btn_w, btn_h, "HARD", config.RED, config.BLACK)

# 3. CHARACTER FRAME (y=175, h=45)
char_frame_y = 175
char_frame_h = 45
default_char_btn = Button(config.screenWidth // 2 - 20, char_frame_y + 8, 180, 28, "DEFAULT", (150, 150, 150), config.BLACK)

# 4. START BUTTON (y=235, h=40)
start_btn = Button(config.screenWidth // 2 - 100, 235, 200, 40, "START GAME", config.GREEN, config.BLACK)

label_font = pygame.font.SysFont('comicsans', 25, True) # segherna kht chwia

def draw_menu():
    # Rsem lkhalfia (Black)
    config.screen.fill(config.BLACK)
    
    # --- TITLE ---
    title_font = pygame.font.SysFont('comicsans', 48, True) # sgheer chwia 
    title_text = title_font.render("ESSOUSSI GAME", True, config.WHITE)
    title_shadow = title_font.render("ESSOUSSI GAME", True, config.GREEN)
    config.screen.blit(title_shadow, (config.screenWidth // 2 - title_text.get_width() // 2 + 2, 12))
    config.screen.blit(title_text, (config.screenWidth // 2 - title_text.get_width() // 2, 10))
    
    # --- FRAME 1: NAME ---
    pygame.draw.rect(config.screen, (30, 30, 30), (frame_x, name_frame_y, frame_w, name_frame_h))
    pygame.draw.rect(config.screen, config.WHITE, (frame_x, name_frame_y, frame_w, name_frame_h), 2)
    name_label = label_font.render("NAME:", True, config.WHITE)
    config.screen.blit(name_label, (frame_x + 20, name_frame_y + 12))
    name_input.update()
    name_input.draw(config.screen)
    
    # --- FRAME 2: DIFFICULTY ---
    pygame.draw.rect(config.screen, (30, 30, 30), (frame_x, diff_frame_y, frame_w, diff_frame_h))
    pygame.draw.rect(config.screen, config.WHITE, (frame_x, diff_frame_y, frame_w, diff_frame_h), 2)
    diff_label = label_font.render("MODE:", True, config.WHITE)
    config.screen.blit(diff_label, (frame_x + 20, diff_frame_y + 12))
    
    easy_btn.color = (0, 200, 0) if config.difficulty == "easy" else (0, 100, 0)
    normal_btn.color = (200, 200, 200) if config.difficulty == "normal" else (100, 100, 100)
    hard_btn.color = (255, 100, 100) if config.difficulty == "hard" else (150, 0, 0)
    easy_btn.draw(config.screen)
    normal_btn.draw(config.screen)
    hard_btn.draw(config.screen)
    
    # --- FRAME 3: CHARACTER ---
    pygame.draw.rect(config.screen, (30, 30, 30), (frame_x, char_frame_y, frame_w, char_frame_h))
    pygame.draw.rect(config.screen, config.WHITE, (frame_x, char_frame_y, frame_w, char_frame_h), 2)
    char_label = label_font.render("HERO:", True, config.WHITE)
    config.screen.blit(char_label, (frame_x + 20, char_frame_y + 12))
    
    default_char_btn.color = (200, 200, 0) # Selected color (Yellowish)
    default_char_btn.draw(config.screen)
    
    # --- START BUTTON ---
    start_btn.draw(config.screen)
    
    # Mettre à jour l'alwan dl hover
    mouse_pos = pygame.mouse.get_pos()
    easy_btn.update(mouse_pos)
    normal_btn.update(mouse_pos)
    hard_btn.update(mouse_pos)
    start_btn.update(mouse_pos)
    
    pygame.display.update()

def handle_menu_events(event):
    name_input.handle_event(event)
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if easy_btn.is_clicked(event.pos):
            config.difficulty = "easy"
        elif normal_btn.is_clicked(event.pos):
            config.difficulty = "normal"
        elif hard_btn.is_clicked(event.pos):
            config.difficulty = "hard"
        elif start_btn.is_clicked(event.pos):
            config.player_name = name_input.text if name_input.text != "" else "Player 1"
            reset_game()
            config.game_state = "playing"
