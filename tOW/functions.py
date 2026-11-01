import pygame
import random
import config
from classes import Player, Enemy

def reset_game():
    # hadi fonction katsawb koulchi mn jdid mnin kaymoti l'batal oula kaykhtar RESTART
    config.man = Player(200, 170, 64, 64) # nkhleq l'batal flblasa rwla
    # nkhleq ga3 les ennemis b des positions ashouawiya f y = l'batal
    config.all_enemies = [Enemy(random.randint(0, 2000), config.man.y, 64, 64) for _ in range(10)]
    config.active_enemies = [] # nkhwiw les ennemis li qdam ybanou
    # nbda b 3 (MAX_ACTIVE) dyal les ennemis ybanou
    for _ in range(config.MAX_ACTIVE):
        if config.all_enemies:
            config.active_enemies.append(config.all_enemies.pop())
    config.bullets = [] # nems7o ga3 rses
    config.score = 0
    config.bg_scroll = 0
    config.game_state = "playing" # nrj3ouh laab
    config.restart_animation = 30  # nbdel animation dyal dwiyt fach ki3awed lgame

def redrawGame():
    # blit background joj mrat bach yekhdem scroll bla myban frgha fl 화면
    config.screen.blit(config.bg, (config.bg_scroll % config.bg.get_width(), 0))
    config.screen.blit(config.bg, (config.bg_scroll % config.bg.get_width() - config.bg.get_width(), 0))
    # nktb smyt joueur w l'score foooq l'imniya
    score_text = f'{config.player_name} Score: {config.score}'
    txt = config.font.render(score_text, True, config.BLACK)
    
    # nrsom ga3 les ennemis activés f chacha
    for enemy in config.active_enemies:
        enemy.draw(config.screen)
    # nrsom l'batal
    config.man.draw(config.screen)
    # n7ot l score (n7sbou l width bash maykhrejch mn chacha limen)
    txt_x = config.screenWidth - txt.get_width() - 20
    config.screen.blit(txt, (txt_x, 20))
    
    # nrsom rses
    for bullet in config.bullets:
        bullet.draw(config.screen)
    
    # ila kan restart, khlini nbiyn effet dyal byoudya tndam ou tch3el
    if config.restart_animation > 0:
        alpha = int((config.restart_animation / 30.0) * 255)
        flash_surface = pygame.Surface((config.screenWidth, config.screenHeight))
        flash_surface.set_alpha(alpha) # nfhel tabyod
        flash_surface.fill(config.WHITE)
        config.screen.blit(flash_surface, (0, 0))
    
    # ila kan game over awla rbe7, yeban txt b loun ahmer wl ahder wl boutton RESTART
    if config.game_state in ["game_over", "win"]:
        # 1. Overlay k7el chfaf 3la chacha kamla bash tban mdellma chwia
        s = pygame.Surface((config.screenWidth, config.screenHeight))
        s.set_alpha(150) # mdelma chwia (0=chfaf 255=k7el)
        s.fill(config.BLACK)
        config.screen.blit(s, (0, 0))
        
        # 2. Rsem panel (cadre) d'lgame over/win bohdo 
        text_panel_w, text_panel_h = 320, 80 # Kbernah bach ykfi lktaba mzyan w matkhrejch
        text_panel_x = config.screenWidth // 2 - text_panel_w // 2
        text_panel_y = config.screenHeight // 2 - 80
        
        pygame.draw.rect(config.screen, (30, 30, 30), (text_panel_x, text_panel_y, text_panel_w, text_panel_h)) # loun rmadi mghloq
        pygame.draw.rect(config.screen, config.WHITE, (text_panel_x, text_panel_y, text_panel_w, text_panel_h), 4) # cadre byad r9i9
        
        # 3. Kteb l'titre dyal game over wla win
        font_end = pygame.font.SysFont('comicsans', 60)
        if config.game_state == "game_over":
            text = font_end.render('GAME OVER', 1, config.RED) # loun hmmer kima tbgha
            # Dilla (shadow) dyal lktaba
            shadow = font_end.render('GAME OVER', 1, config.BLACK)
        else:
            text = font_end.render('YOU WIN!', 1, config.GREEN)
            shadow = font_end.render('YOU WIN!', 1, config.BLACK)
            
        # Nsntréw lktaba wst l panel dl ktba blmlimaitre bach djé west l'itar bdbt
        text_rect = text.get_rect(center=(config.screenWidth // 2, text_panel_y + text_panel_h // 2))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        
        config.screen.blit(shadow, shadow_rect)
        config.screen.blit(text, text_rect)
        
        # 4. Ndépclasiw l bouton dyal RESTART l bo7do (houwa rah mrssoum b cadre dyalo f classes.py)
        # config.restart_button dejé fih couleour khader (config.GREEN) mktoba 3adi (config.BLACK font)
        config.restart_button.rect.width = 320 # nqadoh yji qed cadre dyal GAME OVER f l3erdd
        config.restart_button.rect.x = config.screenWidth // 2 - config.restart_button.rect.width // 2
        config.restart_button.rect.y = config.screenHeight // 2 + 10
        config.restart_button.draw(config.screen)
    
    # nbdel chacha kollch mara bach ibano tatbiqat
    pygame.display.update()
