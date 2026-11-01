import pygame
import random

# hna kanbda l'module dyal pygame
successes, fails = pygame.init()

# hado les dimensions dyal chacha (la fenêtre dyal lgame)
screenWidth = 588
screenHeight = 294
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Essoussi Game") # smya dyal lgame foq l'fenêtre

# les couleurs li ghan7tajohom fl'game (khder, hmer, k7el w bywd)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 100, 0)

# hna kanchargiw les images dyal l'batal mnin kaydir l'mouvement limn w lissr
move_right = [pygame.image.load(f"hero/R{i}.png") for i in range(1, 10)]
move_left = [pygame.image.load(f"hero/L{i}.png") for i in range(1, 10)]

# hna kanchargiw les images dyal les ennemis (lw7ouch)
move_rightE = [pygame.image.load(f"enemy/R{i}E.png") for i in range(1, 12)]
move_leftE = [pygame.image.load(f"enemy/L{i}E.png") for i in range(1, 11)] + [pygame.image.load("enemy/L10E.png")]

# hna kanchargiw les sons dyal l'msseman w derba
bulletsound = pygame.mixer.Sound('sounds/bullet.wav')
hitsound = pygame.mixer.Sound('sounds/hit.wav')

# tswira dyal l'khilfia (background) w tswira dyal lbatal waqf
bg = pygame.image.load("background.jpg")
hero = pygame.image.load("standing.png")

clock = pygame.time.Clock() # l'horloge dyal lgame bach ncontroliw l'vitesse (fps)

# l'khotot dyal l'ktba (fonts) - kaytlbo ikon display m'initialiser 9bl maykhedmo
font = pygame.font.SysFont('comicsans', 30, True, BLACK)

# les variables globals bach ntb3o l'7ala dyal lgame (score, background scroll)
score = 0
bg_scroll = 0
game_state = "menu"  # l'halaa dyal lgame ya: menu, playing (l3ab), game_over (khsek), aw win (rb7ti)
restart_animation = 0

# jdad: bach ysjalo smyt joueur o so3ouba
player_name = ""
difficulty = "normal" # t9der tkon "easy", "normal", "hard"

# les variables dyal lblayk li ghaykouno flgame, ghay3emro b'données men be3d f'reset_game
active_enemies = [] # les ennemis li baynin daba
all_enemies = [] # ga3 les ennemis
bullets = [] # l'qrtas li motlo9
man = None # l'batal dyalna (le joueur)
restart_button = None # zrir dyal restart (i3iyad tl3eb)
MAX_ACTIVE = 3 # ch7al mn wa7ch yban f d9a whda
