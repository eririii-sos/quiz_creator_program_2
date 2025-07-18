# General Instructions: Create the Quiz program that read the output file of the Quiz Creator; 
# The user will answer the randomly selected question and check if the answer is correct.

# Install library to use

# Import library
import pygame
import sys
import random

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

# Load quiz's grade display for result portion (Failed, Poor, Passed, Perfect + character expression)
failed_mark = pygame.transform.scale(pygame.image.load("assets/failed_mark.png"),(300, 150))
poor_mark = pygame.transform.scale(pygame.image.load("assets/poor_mark.png"),(300, 150))
passed_mark = pygame.transform.scale(pygame.image.load("assets/passed_mark.png"),(300, 150))
perfect_mark = pygame.transform.scale(pygame.image.load("assets/perfect_mark.png"),(300, 150))
failed_expression = pygame.transform.scale(pygame.image.load("assets/failed.png"),(300, 300))
poor_expression = pygame.transform.scale(pygame.image.load("assets/average.png"),(300, 300))
passed_expression = pygame.transform.scale(pygame.image.load("assets/passed.png"),(300, 300))
happy_expression = pygame.transform.scale(pygame.image.load("assets/happy.png"),(300, 300))

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

# Load music set
def music_1():
    pygame.mixer.music.load("home_bg_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop forever

def music_2():
    pygame.mixer.music.load("hallway_bg_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop forever

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
developer_info_active = False

# Font setup
font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 40)

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
hallway_scene_done = False # Variable to track if the fade-in has occurred
show_yes_no = False
quiz_transition_done = False
quiz_started = False
quiz_active = False
quiz_finished = False
questions_answered = 0

# Set menu background
def draw_menu():
    screen.blit(background_1, (0, 0))  # Draw background

    # Comment proceeding parts so they are invisible
    # pygame.draw.rect(screen, (100, 100, 100), start_button)
    # pygame.draw.rect(screen, (100, 100, 100), exit_button)
    # screen.blit(start_button.x + 70, start_button.y + 15)
    # screen.blit(exit_button.x + 70, exit_button.y + 15)

    # pygame.draw.rect(screen, (100, 100, 100), info_button)
    # screen.blit(info_text, (info_button.x + 20, info_button.y + 10))

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

# Pop up message if user proceeds with quiz game
def show_popup_message():
    screen.blit(background_3, (0, 0))
    instruction_box = pygame.Surface((600, 200))
    instruction_box.fill((0, 0, 0))
    instruction_box.set_alpha(200)
    screen.blit(instruction_box, (WIDTH // 2 - 300, HEIGHT // 2 - 100))

    instruction_text_1 = font.render("Click the correct answer from the choices.", True, (255, 255, 255))
    instruction_text_2 = font.render("Press SPACE to start.", True, (255, 255, 255))
    screen.blit(instruction_text_1, (WIDTH // 2 - 210, HEIGHT // 2 - 30))
    screen.blit(instruction_text_2, (WIDTH // 2 - 120, HEIGHT // 2))

# Load and set necessities for quiz part
quiz_file = 'quiz_creator_questions.txt'

# Loading of quiz portion's q&a base on the txt file containing the data of the quiz creator program
def load_quiz_questions(quiz_file):
    with open(quiz_file, 'r') as file:
        content = file.read().strip()
    raw_questions = content.split("--------------------------------------------------")
    questions = []
    for block in raw_questions:
        lines = block.strip().splitlines()
        if not lines:
            continue
        q_data = {
            "question": lines[0].replace("Question: ", "").strip(),
            "choices": [],
            "answer": ""
        }
        
        if len(q_data["choices"]) == 4 and q_data["answer"] in ['a', 'b', 'c', 'd']:
            questions.append(q_data)

        for line in lines[1:]:
            line = line.strip()
            if line.startswith("a)") or line.startswith("b)") or line.startswith("c)") or line.startswith("d)"):
                q_data["choices"].append(line)
            elif line.startswith("Correct Answer:"):
                q_data["answer"] = line[-1].lower()
        questions.append(q_data)
    random.shuffle(questions) # Randomize the question set
    return questions

# Load quiz data
quiz_data = load_quiz_questions("quiz_creator_questions.txt")
current_question_index = 0
user_score = 0
user_answers = []

# Setup for quiz UI
quiz_font = pygame.font.Font(None, 25)
quiz_question_rect = pygame.Rect(580, 170, 270, 100)
quiz_choices_rects = [pygame.Rect(580, 220 + i*50, 270, 40) for i in range(4)]
question_timer = 21000

# Set screen layout during quiz game
def draw_quiz_screen():

    global quiz_data, current_question_index
    screen.blit(background_3, (0, 0))
    
    # Error handling if no q&a data to use
    if not quiz_data or current_question_index >= len(quiz_data):

        error_text_box = pygame.Surface((600, 200))
        error_text_box.fill((255, 255, 255))
        screen.blit(error_text_box, (WIDTH // 2 - 300, HEIGHT // 2 - 100))

        error_text = font.render("No quiz questions available.", True, (255, 0, 0))
        screen.blit(error_text, (WIDTH // 2 - 150, HEIGHT // 2)) 
        return
    
    question_data = quiz_data[current_question_index]
    
    progress = f"PROGRESS: {current_question_index + 1}/{len(quiz_data)}"
    screen.blit(font.render(progress, True, (0, 0, 0)), (WIDTH - 800, 240))

    question_surface = quiz_font.render(question_data["question"], True, (0, 0, 0))
    screen.blit(question_surface, quiz_question_rect.topleft)

    for i, rect in enumerate(quiz_choices_rects):
        if i < len(question_data["choices"]):  # ✅ Only draw available choices
            pygame.draw.rect(screen, (255, 255, 0), rect)
            choice_text = quiz_font.render(question_data["choices"][i], True, (0, 0, 0))
            screen.blit(choice_text, (rect.x + 10, rect.y + 10))

    timer_seconds = question_timer / 1000
    timer_surface = font.render(f"Time Left: {int(timer_seconds)}s", True, (255, 0, 0))
    screen.blit(timer_surface, (WIDTH - 800, 270))

# Update quiz timer handling
def handle_timer():
    global question_timer, current_question_index, user_score
    if question_timer <= 0:  # If the timer runs out
        question_timer = 21000  # Reset timer for the next question
        user_score -= 1  # Decrease score for incorrect answer (default behavior)
        current_question_index += 1  # Move to the next question
        if current_question_index >= len(quiz_data):
            return

# Reload quiz q&a set every play
def reset_quiz():
    global quiz_data, current_question_index, user_score, user_answers, quiz_transition_done
    quiz_data = load_quiz_questions(quiz_file)  # Reload and randomize the questions
    current_question_index = 0
    user_score = 0
    user_answers = []    
    quiz_transition_done = False

# Fade to black transition
def fade_to_black(duration=1000):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    fade_clock = pygame.time.Clock()
    alpha = 0
    fade_speed = 255 / (duration / 10)
    
    while alpha < 255:
        fade_surface.set_alpha(int(alpha))
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        alpha += fade_speed
        fade_clock.tick(60)

# Show quiz results
def draw_result_screen():
    screen.fill((0,0,0))
    screen.blit(background_3, (0, 0))
    result_text = f"You got {user_score}/{len(quiz_data)} correct!"
    result_surface = title_font.render(result_text, True, (12, 0, 0))
    screen.blit(result_surface, (WIDTH - 480, 220))

    # Show result mark image based on score
    if user_score == 0:
        mark_image = failed_mark
        char_expression = failed_expression
    elif user_score < len(quiz_data) // 2:
        mark_image = poor_mark
        char_expression = poor_expression
    elif user_score >= len(quiz_data) // 2:
        mark_image = passed_mark
        char_expression = passed_expression
    elif user_score == len(quiz_data):
        mark_image = perfect_mark
        char_expression = happy_expression
    screen.blit(mark_image, (WIDTH - 500, 230))
    screen.blit(char_expression, (WIDTH - 890, 130))

    # Draw "Press Esc to Exit" button
    exit_text = font.render("Press Esc to Exit", True, (255, 255, 255))
    exit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 230, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
    screen.blit(exit_text, (WIDTH // 2 - 80, HEIGHT // 2 + 245))

# Developer Information
def developer_info():
    screen.fill((0, 0, 128)) 
    lines = [
        "Quiz Day",
        "",
        "Developed by:",
        "Jacey Erin D. Concepcion",
        "",

        "",
        "GitHub: Jacey Concepcion | @eririii-sos",
        "https://github.com/eririii-sos/quiz_creator_program_2",
        "",
        "Special thanks to Prof. Danilo Madrigalajos!",
        "",

        "",
        "2025 | Made with Python and Pygame.",
        "",
        "[ Press ESC to return to Menu ]"
        ""
    ]

    y = 50
    for line in lines:
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (50, y))
        y += 30

# Main loop
music_1()

running = True
while running:
    
    dt = clock.tick(60)

    if game_state == "menu":
        draw_menu()
    
    elif game_state == "developer_info":
        developer_info()

    elif game_state == "play":
        screen.blit(background_2, (0, 0))

        if not hallway_scene_done:
            Hallway_scene(char_expression_1)  # Character fades in
            hallway_scene_done = True  

        if current_line < len(scene_1_monologue): # Update character expressions as monologue progresses
            typed_text, char_index = process_monologue(current_line, char_index, dt)
            expression_to_use = expression_map.get(current_line, expression_map[11])
            screen.blit(expression_to_use, (WIDTH // 2 - 150, HEIGHT - 400))
            draw_text_box()

        if current_line >= len(scene_1_monologue):  # Have Yes and No buttons appear after monologue
            show_yes_no = True
            screen.blit(char_expression_9, (WIDTH // 2 - 150, HEIGHT - 400))
            draw_yes_no_buttons()

    elif game_state == "quiz":

        if not quiz_transition_done:
            fade_to_black()
            quiz_transition_done = True
            show_popup_message()

        elif quiz_started and not quiz_finished:
            draw_quiz_screen()
            if question_timer > 0:
                question_timer -= dt
            else:
                question_timer = 0
                questions_answered += 1
                current_question_index += 1
                if current_question_index < len(quiz_data):
                    question_timer = 21000
                else:
                    quiz_finished = True
                    fade_to_black()  
                    game_state = "result"
            

    elif game_state == "result":
        draw_result_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if game_state == "menu":
                if start_button.collidepoint(mouse_pos):

                    music_2()
                    # Reset hallway scene 
                    current_line = 0
                    typed_text = ""
                    char_index = 0
                    text_timer = 0
                    hallway_scene_done = False
                    show_yes_no = False 
                    game_state = "play"               

                elif exit_button.collidepoint(mouse_pos):
                    running = False

                elif info_button.collidepoint(mouse_pos):
                    game_state = "developer_info"

            elif game_state == "play" and show_yes_no:
                if yes_button.collidepoint(mouse_pos):
                    reset_quiz()
                    game_state = "quiz"
                elif no_button.collidepoint(mouse_pos):
                    reset_quiz()
                    game_state = "menu"

            elif game_state == "quiz":

                if not quiz_finished and current_question_index < len(quiz_data):
                    for i, rect in enumerate(quiz_choices_rects):
                        if rect.collidepoint(mouse_pos):
                            question_data = quiz_data[current_question_index]
                            selected = question_data["choices"][i][0].lower()
                            correct = question_data["answer"]
                            user_answers.append(selected)
                            if selected == correct:
                                user_score += 1                            
                            current_question_index += 1
                            question_timer = 21000  # Reset timer for next question (20 seconds)

                            if current_question_index >= len(quiz_data):
                                fade_to_black()
                                game_state = "result"                

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "play":
                    if current_line < len(scene_1_monologue):
                        if char_index == len(scene_1_monologue[current_line]):
                            current_line += 1
                            typed_text = ""
                            char_index = 0

                elif game_state == "quiz" and quiz_transition_done and not quiz_started:
                    show_quiz_popup = False
                    quiz_started = True
                    quiz_active = True
                    question_timer = 21000  # Reset timer on start
                    start_time = pygame.time.get_ticks()  

            elif event.key == pygame.K_ESCAPE:
                game_state = "menu"                

    # Update the display
    pygame.display.flip()     

pygame.quit()
sys.exit()       