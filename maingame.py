import pygame

# Initialize pygame
pygame.init()

# Screen settings
screen_width, screen_height = 588, 294
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Movement Game")

# Colors
BLACK = (0, 0, 0)

# Load assets
hero_img = pygame.image.load("hero/standing.png")  # Single player image
bg = pygame.image.load("background.jpg")
bg_width = bg.get_width()

class Player:
    def _init_(self, x, y):
        self.x, self.y = x, y
        self.speed = 5
        self.jump_power = 11
        self.gravity = 0.3
        self.jump_speed = self.jump_power
        self.is_jumping = False
        
    def draw(self):
        screen.blit(hero_img, (self.x, self.y))

def redraw(scroll):
    # Draw parallax background
    screen.blit(bg, (scroll % bg_width, 0))
    screen.blit(bg, (scroll % bg_width - bg_width, 0))
    
    # Draw player
    man.draw()
    pygame.display.update()

# Game setup
man = Player(200, 170)
scroll = 0

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    # Movement
    if keys[pygame.K_LEFT]:
        scroll += man.speed
    elif keys[pygame.K_RIGHT]:
        scroll -= man.speed
    
    # Jumping
    if not man.is_jumping and keys[pygame.K_SPACE]:
        man.is_jumping = True
        man.jump_speed = man.jump_power
    
    if man.is_jumping:
        man.y -= (man.jump_speed**2) * man.gravity * (1 if man.jump_speed >= 0 else -1)
        man.jump_speed -= 1
        if man.jump_speed < -man.jump_power:
            man.is_jumping = False
            man.jump_speed = man.jump_power
    
    redraw(scroll)

pygame.quit()