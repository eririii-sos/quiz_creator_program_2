# General Instructions: Create the Quiz program that read the output file of the Quiz Creator; 
# The user will answer the randomly selected question and check if the answer is correct.

# Install library to use

# Import library
import pygame
import sys

# Initialyze pygame
pygame.init()
pygame.mixer.init()

# Set up window
WIDTH, HEIGHT = 1067, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Day")

# Load display background(s) 
home_background = pygame.image.load("assets/background.png")
background_1 = pygame.transform.scale(home_background, (WIDTH, HEIGHT))

# Font setup
font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 48)

# Set Menu buttons
start_button = pygame.Rect(100, 100, 100, 100)
exit_button = pygame.Rect(200, 200, 200, 200)
info_button = pygame.Rect(WIDTH - 110, HEIGHT - 50, 100, 50)

# Set menu background
def draw_menu():
    screen.blit(background_1, (0, 0))  # Draw background

    # Draw menu buttons and label
    pygame.draw.rect(screen, (100, 100, 100), start_button)
    pygame.draw.rect(screen, (100, 100, 100), exit_button)
    start_text = font.render("Start", True, (255, 255, 255))
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(start_text, (start_button.x + 70, start_button.y + 15))
    screen.blit(exit_text, (exit_button.x + 70, exit_button.y + 15))

def dev_info_button():
    pygame.draw.rect(screen, (100, 100, 100), info_button)
    info_text = font.render("About", True, (255, 255, 255))
    screen.blit(info_text, (info_button.x + 20, info_button.y + 10))

# Main loop
running = True
while running:

    draw_menu()
    dev_info_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()            