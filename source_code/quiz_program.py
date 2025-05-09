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
school_hall_background = pygame.image.load("assets/school_hall_background.jpg")
background_2 = pygame.transform.scale(school_hall_background, (WIDTH, HEIGHT))

# Load character facial expression set
char_expression_1 = pygame.transform.scale(pygame.image.load("assets/neutral2.png"), (300, 400))
char_expression_2 = pygame.transform.scale(pygame.image.load("assets/shocked.png"), (300, 400))
char_expression_3 = pygame.transform.scale(pygame.image.load("assets/disbelief.png"), (300, 400))
char_expression_4 = pygame.transform.scale(pygame.image.load("assets/wondering.png"), (300, 400))
char_expression_5 = pygame.transform.scale(pygame.image.load("assets/thinking2.png"), (300, 400))
char_expression_6 = pygame.transform.scale(pygame.image.load("assets/AHEM.png"), (300, 400))
char_expression_7 = pygame.transform.scale(pygame.image.load("assets/begging.png"), (300, 400))
char_expression_8 = pygame.transform.scale(pygame.image.load("assets/begging2.png"), (300, 400))
char_expression_9 = pygame.transform.scale(pygame.image.load("assets/thinking.png"), (300, 400))

# Monologue text data for the hallway scene
scene_1_monologue = [
    "(Press SPACE to proceed)",  # First message
    "Oh",  # Start of Monologue
    "GOOOOOOOOOOSH!",  
    "I completely forgot about our quiz today!",  
    "I wasn't able to study! What am I going to do?",  
    "...",  
    "...",  
    "...",  
    "hey, uh...", 
    "...will you help me?",  
    "PLEASEEEEEEEE :3",  # End of Monologue
]

# Monologue typing logic
current_line = 0
typed_text = ""
char_index = 0
text_timer = 0  # Initialized text_timer 
TEXT_SPEED = 30

# Clock for frame rate
clock = pygame.time.Clock()

# Game state
game_state = "menu"

# Font setup
font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 48)

# Set Menu buttons
start_button = pygame.Rect(395, 270, 280, 60)
exit_button = pygame.Rect(395, 360, 280, 60)
info_button = pygame.Rect(WIDTH - 60, HEIGHT - 60, 40, 40)

# UI settings
text_box_rect = pygame.Rect(200, 500, 700, 250)
text_color = (255, 255, 255)
box_color = (0, 0, 0)
box_alpha = 180

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

# Text box for character monologue in 1st scene
def draw_text_box():
    box = pygame.Surface((text_box_rect.width, text_box_rect.height))
    box.set_alpha(box_alpha)
    box.fill(box_color)
    screen.blit(box, text_box_rect.topleft)
    character_name_display = font.render("Eri", True, (255, 255, 255))
    screen.blit(character_name_display, (start_button.x + -190, start_button.y + 210))

# 1st scene transitioning with fade in effect
def Hallway_scene(character_image, duration=1000):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    fade_clock = pygame.time.Clock()
    alpha = 255
    fade_speed = 255 / (duration / 10)
    
    while alpha > 0:
        fade_surface.set_alpha(int(alpha))
        screen.blit(background_2, (0, 0))  # Background stays static
        screen.blit(character_image, (WIDTH//2 - 150, HEIGHT - 400))
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        alpha -= fade_speed
        fade_clock.tick(60)

Hallway_scene_done = False # Variable to track if the fade-in has occurred

# Main loop
running = True
while running:
    
    dt = clock.tick(60)

    if game_state == "menu":
        draw_menu()
        dev_info_button()
    
    elif game_state == "play":
        screen.blit(background_2, (0, 0))

        if not Hallway_scene_done:
            Hallway_scene(char_expression_1)  # Character fades in
            Hallway_scene_done = True  

        draw_text_box()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if game_state == "menu":
                if start_button.collidepoint(mouse_pos):
                    game_state = "play"               
                elif exit_button.collidepoint(mouse_pos):
                    running = False

    # Update the display
    pygame.display.flip()            