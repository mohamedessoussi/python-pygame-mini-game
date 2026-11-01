import pygame
import config
from classes import Button, Player, Enemy, Bullet
from functions import reset_game, redrawGame
from menu import draw_menu, handle_menu_events

# khle9na e-zer d "RESTART" f'wset dyal e-chacha, ma ymqdrnach na3mlo hadshi f config hitach l'ktba/font ba9a mat'initializatsh
config.restart_button = Button(config.screenWidth // 2 - 60, config.screenHeight // 2 + 80, 120, 50, "RESTART", config.GREEN, config.BLACK)

# nebda2o l'game la mrra lowla bash tkhleq l'motaghayirat ga3 (b7al lw7ouch)
reset_game()

# Nrz3oh l'menu  bash maybdach l3eb direct
config.game_state = "menu"

# l'boucle principale dyal lgame li kaykhelliha dima khdama
running = True
while running:
    # 30 fps, maximum sor3a dyal lgame
    config.clock.tick(30)
    
    # njib blasset souris fine kayna daba
    mouse_pos = pygame.mouse.get_pos()
    # n-update state d RESTART bouton, wach souris fo9 mno awla la
    config.restart_button.update(mouse_pos)
    
    # ntchecki 3la l'ahdath (events) b7al souris w clavier
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # ila seddit l'fenêtre, wqaf kolchi m   
            
        if config.game_state == "menu":
            handle_menu_events(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if config.game_state != "playing": # ila kan match mssali (rkhti awla rb7ti)
                    # w kliciti 3la bouton d RESTART
                    if config.restart_button.is_clicked(event.pos):
                        # restart ga3 lvariablates l zero
                        reset_game()
            if event.type == pygame.KEYDOWN:
                # ila wrk 3la "S" -> tire qertassa m3a itijah dyal joueur
                if event.key == pygame.K_s and len(config.bullets) < 5 and config.game_state == "playing":
                    config.bulletsound.play()
                    direction = 1 if config.man.right else -1
                    config.bullets.append(Bullet(round(config.man.x + config.man.width // 2), round(config.man.y + config.man.height // 2), 5, config.RED, direction, 10))
                # ila wrk 3la "F" -> dima kaytire 9ertasa gha qddamo flimn
                elif event.key == pygame.K_f and len(config.bullets) < 5 and config.game_state == "playing":
                    config.bulletsound.play()
                    config.bullets.append(Bullet(round(config.man.x + config.man.width // 2), round(config.man.y + config.man.height // 2), 5, config.RED, 1, 10))

    # ila kano f lista dyal l'menu
    if config.game_state == "menu":
        draw_menu()
        continue

    # ila mamkhdmch lgame, dir redraw ou khrej (madirch l'mouvements wl collisions)
    if config.game_state != "playing":
        redrawGame()
        continue
    
    # nqess men compteur dl'animation mn mora l'restart
    if config.restart_animation > 0:
        config.restart_animation -= 1

    keys = pygame.key.get_pressed()

    # nchouf wach kayn darba m3a l'we7ch
    for enemy in config.active_enemies:
        if enemy.visible:
            # hasb blasa dyal lwe7ch wzid 3liha mouvement d background
            enemy_hitbox_x = enemy.hitbox[0] + config.bg_scroll
            enemy_hitbox = (enemy_hitbox_x, enemy.hitbox[1], enemy.hitbox[2], enemy.hitbox[3])
            
            # wach rectangl dyal l'batal tdkhl f rectangl dyal we7ch?
            if (config.man.hitbox[0] < enemy_hitbox_x + enemy_hitbox[2] and 
                config.man.hitbox[0] + config.man.hitbox[2] > enemy_hitbox_x and 
                config.man.hitbox[1] < enemy_hitbox[1] + enemy_hitbox[3] and 
                config.man.hitbox[1] + config.man.hitbox[3] > enemy_hitbox[1]):
                config.man.hit() # tdarb hbatal!

    # logica dyal rsesaat
    for bullet in config.bullets[:]:
        bullet_hit = False
        for enemy in config.active_enemies:
            if enemy.visible:
                enemy_hitbox_x = enemy.hitbox[0] + config.bg_scroll
                # wach qertasa dkhlat f w7ch?
                if (enemy_hitbox_x < bullet.x < enemy_hitbox_x + enemy.hitbox[2] and 
                    enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3]):
                    config.bullets.remove(bullet) # mse7 rqetasa
                    enemy.hit() # qass lw7ch dm dyalou
                    bullet_hit = True
                    if not enemy.visible: # ila mtt lw7ch
                        config.score += 1 # zid naqta
                        if config.all_enemies: # jbid w7ch jdid mn lqantra li khzanin fihom (all_enemies)
                            config.active_enemies.append(config.all_enemies.pop())
                        elif not any(e.visible for e in config.active_enemies): # mato ga3 lw7ouch!
                            config.game_state = "win" # rbbtii!!
                    break
        
        # ila makynch hsab w9ertasa mazel wsta chacha: hrk qertassa lkdam 
        if not bullet_hit and 0 < bullet.x < config.screenWidth:
            bullet.x += bullet.step
        else: # raha khrjat mn chacha wla darbna lw7ch
            if bullet in config.bullets:
                config.bullets.remove(bullet)

    # mouvement dyal l'batal bl clavier wl souris (khroj b list flimn / lissr)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        config.bg_scroll += config.man.step # scroll f chacha lilimen (bach tzid lisar)
        config.man.left = True
        config.man.right = False
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        config.bg_scroll -= config.man.step # scroll chacha listar (bach yzid limn)
        config.man.right = True
        config.man.left = False
    else: # ila muharkch
        config.man.left = False
        config.man.right = False
        config.man.moves = 0  # rja ltaswiera louwla wqf

    # logica dyal nqzato hliya f sma
    if not config.man.isJumping:
        if keys[pygame.K_UP]: 
            config.man.isJumping = True
            config.man.current_speed = config.man.jump_speed
    else: # ila kynqz
        if config.man.current_speed >= -config.man.jump_speed:
            neg = 1 if config.man.current_speed >= 0 else -1
            # hasb mn position y ljdida b formul dyal physics
            config.man.y -= (config.man.current_speed ** 2) * config.man.gravity * neg
            config.man.current_speed -= 1 # hbt chouia sor3a
        else: # wsel lared
            config.man.isJumping = False
            config.man.current_speed = config.man.jump_speed

    # rsem ga3 chachi kima jat jdida (moura ma tbdlat les positions w variables)
    redrawGame()

pygame.quit() # khrjet mn game kamel!