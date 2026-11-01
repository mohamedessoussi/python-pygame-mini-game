import pygame
import random
import config

# classe dyal les boutons (b7al zrir RESTART)
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height) # lmstatal dyal lbouton
        self.text = text # lktba li fih
        self.color = color 
        self.text_color = text_color
        self.original_color = color
        self.hover_color = (0, 150, 0)  # loun mghloq mnin kaydoz souris foh l'bouton
        self.font = pygame.font.SysFont('comicsans', 25, True) # Sgherna lkht chwia
        self.is_hovered = False # wach souris fqha wla la

    def update(self, mouse_pos):
        # hadi katcheck wach souris m7tot foha
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        # rsom lbouton f chacha hssab wach souris foh wla la
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, config.BLACK, self.rect, 3) # cadre k7al l'bouton
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        # katcheck wach tqerbat l'bouton
        return self.rect.collidepoint(pos)

# classe dyal lblayk li katkteb fihom (b7al smyat l'joueur)
class TextInputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.base_width = width # N7tafdo bl 3red lowl
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.SysFont('comicsans', 25, True) # Sgherna lkht dyal input box
        # Nreddo l'loun d lktaba BYAD
        self.text_color = config.WHITE
        self.txt_surface = self.font.render(text, True, self.text_color)
        self.active = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check wach clicka west l box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False # sedha mnine yekhbet entré
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Render bl'byad dima
                self.txt_surface = self.font.render(self.text, True, self.text_color)
                
    def update(self):
        # 7besna likhroj mn l'itar ila tktab bzaf w 7afedna 3la l3rd l assli
        width = max(self.base_width, min(self.txt_surface.get_width() + 20, 380))
        self.rect.w = width
        # njiboh dima lwst ila tzadd 3rdo
        self.rect.centerx = config.screenWidth // 2
        
    def draw(self, screen):
        # Nsttéw l'ktba fl wssat dl cadre dyalha dl Box
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

# classe dyal l'batal dyal lgame
class Player():
    def __init__(self, x, y, width, height):
        self.x = x # position x
        self.y = y # position y
        self.x_start = x # position wqfha lowla (bach yrg3 f game over wla dorba)
        self.y_start = y 
        self.width = width # l'3erd
        self.height = height # twl
        self.step = 5 # sor3a dyal lmchi
        self.left = False # wach kymchi chmal
        self.right = False # wach kymchi yamn
        self.moves = 0 # l'wjah dyal l'mvt
        self.jump_speed = 11 # sor3a dyal tengiza
        self.gravity = 0.3 # ljalbiya bash yti7
        self.current_speed = self.jump_speed 
        self.isJumping = False # wach kaynjez wla la
        self.hp = 5 # dm dyal l'batal
        self.hitbox = (self.x+20, self.y+10, self.width-40, self.height-10) # lmstatal dyal dorbya (fin kytdrb)
        self.last_hit_time = 0

    def draw(self, screen):
        # khrrej l'animation dyal l'batal hlach mnin mcha limn wla lissr
        if self.left:
            screen.blit(config.move_left[self.moves // 2], (self.x, self.y))
            self.moves = (self.moves + 1) % 18
        elif self.right:
            screen.blit(config.move_right[self.moves // 2], (self.x, self.y))
            self.moves = (self.moves + 1) % 18
        else:
            screen.blit(config.hero, (self.x, self.y))
        
        # update l'hitbox f blastha l'jadida
        self.hitbox = (self.x+20, self.y+10, self.width-40, self.height-10)

        # rsom ddam dyal l'batal foooq
        for i in range(self.hp):
            pygame.draw.rect(screen, config.RED, (20 + i * 30, 10, 20, 20))

    def hit(self):
        # mnin kytdreb l'batal
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > 1000: # khasso mnin yedreb yertah shwia
            self.hp -= 1
            self.last_hit_time = current_time
            if self.hp <= 0: # ila sal lhdhd dm (0 dm)
                config.game_state = "game_over" # game over
            else: # ghyrg3 l blastha lowla w ytnegs
                self.current_speed = self.jump_speed
                self.isJumping = False
                self.x = self.x_start
                self.y = self.y_start
                self.moves = 0
                font1 = pygame.font.SysFont('comicsans', 70)
                text = font1.render('-1 HP', 1, config.RED)
                config.screen.blit(text, (config.screenWidth // 2 - 100, 140))
                pygame.display.update()
                pygame.time.delay(800)

# classe dyal rsesstati (9ertasat)
class Bullet:
    def __init__(self, x, y, radius, color, direction, step):
        self.x = x # position
        self.y = y
        self.radius = radius # l3red dyal rassasa
        self.color = color 
        self.direction = direction # tijah (-1 = lissr, 1 = limn)
        self.step = step * direction # sor3a m3a ttijah

    def draw(self, screen):
        # rsom da2era tmetl rsesa
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# classe dyal les ennemis / w7ouch
class Enemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # dbert fih 7ssab so3oba (difficulty) li mkhtara fl menu
        if config.difficulty == "easy":
            self.health = 10
            self.speeds = [-2, -1, 1, 2]
        elif config.difficulty == "hard":
            self.health = 30
            self.speeds = [-4, -3, 3, 4]
        else: # normal
            self.health = 20 # dm dyal lwe7ch
            self.speeds = [-3, -2, 2, 3] # sor3a w tijah ashouayi
            
        self.step = random.choice(self.speeds)
        self.moves = 0
        self.visible = True # wach bayn wla met
        self.hitbox = (self.x + 20, self.y, self.width - 35, self.height)
        self.direction_change_time = pygame.time.get_ticks()
        self.direction_change_interval = random.randint(1000, 3000)

    def draw(self, screen):
        if self.visible:
            # hrko ghi ila kant lgama mkhdma (machi game over wla rbe7)
            if config.game_state == "playing":
                self.move() # hrek lwe7ch
                self.moves = (self.moves + 1) % 22
                
            # blit l'animation hsab ttijah dyalna (bg_scroll hiya l حركة ديال l background bach yban kit7arrak hd l camera)
            if self.step < 0:
                screen.blit(config.move_leftE[self.moves // 2], (self.x + config.bg_scroll, self.y))
            else:
                screen.blit(config.move_rightE[self.moves // 2], (self.x + config.bg_scroll, self.y))

            # rseom dm dyal lwe7ch (khder foooq hmer kiwre wch dm naqs wla kamel)
            pygame.draw.rect(screen, config.RED, (self.hitbox[0] + config.bg_scroll - 3, self.hitbox[1] - 15, 50, 7))
            pygame.draw.rect(screen, config.GREEN, (self.hitbox[0] + config.bg_scroll - 3, self.hitbox[1] - 15, self.health * 5 // 2, 7))
            self.hitbox = (self.x + 20, self.y, self.width - 35, self.height)

    def move(self):
        # hdchi khlihom yghyro l itijah mrra mrra ashouaya
        current_time = pygame.time.get_ticks()
        if current_time - self.direction_change_time > self.direction_change_interval:
            if random.random() < 0.3:
                self.step = random.choice(self.speeds) # tdir 3la hsab so3oba l'jedida
            self.direction_change_time = current_time
            self.direction_change_interval = random.randint(1000, 3000)
        
        self.x += self.step
        
        # ila mchaw b3id m l camera, ghykhrjou mn choufa w y3awdou ydehlou mn jiha khura
        if self.x + config.bg_scroll < -100:
            self.x = -config.bg_scroll + config.screenWidth + 100
        elif self.x + config.bg_scroll > config.screenWidth + 100:
            self.x = -config.bg_scroll - 100

    def hit(self):
        # lwe7ch tedreb
        config.hitsound.play()
        self.health -= 1
        if self.health <= 0: # ila mtt
            self.visible = False # khalih ma ybnch
            self.hitbox = (0, 0, 0, 0) # ms7 lmstatal dyalou bach maytmchich 3liha rbhtih
