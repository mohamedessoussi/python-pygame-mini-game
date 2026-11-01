import pygame
import random

import welcomelib
welcomelib.say_welcome()

# initialisation 
pygame.init()
# set up the display part
width = 600
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("testing py game library")

# colors part
WHITE = (255, 255, 255)

# game loop
running = True

# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # change the bg color on clique
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    # update the display 
    pygame.display.flip()

# quit game
pygame.quit()

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
