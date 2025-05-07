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
screen.fill((255, 255, 255))  # Initial background fill
pygame.display.set_caption("Quiz Day")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()            