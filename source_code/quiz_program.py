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
quiz_background = pygame.image.load("assets/quiz_background.png")
background_3 = pygame.transform.scale(quiz_background, (WIDTH, HEIGHT))

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
    "OH",  # Start of Monologue
    "MY",
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

# Character expressions mapped to each dialogue line
expression_map = {
    0: char_expression_1,  
    1: char_expression_2,  
    2: char_expression_2,  
    3: char_expression_3, 
    4: char_expression_3,  
    5: char_expression_4,  
    6: char_expression_4,  
    7: char_expression_5,  
    8: char_expression_6,  
    9: char_expression_7,  
    10: char_expression_8,  
    11: char_expression_9,  
}

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

# State variables
Hallway_scene_done = False # Variable to track if the fade-in has occurred
show_yes_no = False

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
    
    # Wrap text
    words = typed_text.split(' ')
    lines = []
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < text_box_rect.width - 20:
            line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (text_box_rect.left + 10, text_box_rect.top + 10 + i * 28))

# Monologue Processing
def process_monologue(current_line, char_index, dt):
    global typed_text, text_timer 
    if current_line < len(scene_1_monologue):
        line_text = scene_1_monologue[current_line]
        if char_index < len(line_text):
            text_timer += dt
            if text_timer >= TEXT_SPEED:
                typed_text += line_text[char_index]
                char_index += 1
                text_timer = 0
        return typed_text, char_index
    else:
        return None, char_index  # End of monologue sequence
    
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

# Yes/No buttons at end of monologue
yes_button = pygame.Rect(300, 500, 200, 50)
no_button = pygame.Rect(550, 500, 200, 50)

def draw_yes_no_buttons():
    pygame.draw.rect(screen, (0, 120, 0), yes_button)
    pygame.draw.rect(screen, (120, 0, 0), no_button)
    yes_text = font.render("Yes", True, (255, 255, 255))
    no_text = font.render("No", True, (255, 255, 255))
    screen.blit(yes_text, (yes_button.x + 75, yes_button.y + 15))
    screen.blit(no_text, (no_button.x + 75, no_button.y + 15))

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

        if current_line < len(scene_1_monologue): # Update character expressions as monologue progresses
            typed_text, char_index = process_monologue(current_line, char_index, dt)
            expression_to_use = expression_map.get(current_line, expression_map[11])
            screen.blit(expression_to_use, (WIDTH // 2 - 150, HEIGHT - 400))
            draw_text_box()

        if current_line >= len(scene_1_monologue):  # Have Yes and No buttons appear after monologue
            show_yes_no = True
            screen.blit(char_expression_9, (WIDTH // 2 - 150, HEIGHT - 400))
            draw_yes_no_buttons()

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
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_line < len(scene_1_monologue):
                    if char_index == len(scene_1_monologue[current_line]):
                        current_line += 1
                        typed_text = ""
                        char_index = 0

    # Update the display
    pygame.display.flip()            