# Made By AKShaheen <abdelazizshaheen162@gmail.com> For Python Workshop In Cic
# Forked by 


import pygame.display
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BGCOLOR = (255, 182, 193)
TEXT_COLOR = (255, 255, 179)
FOOD_COLOR = (155, 215, 255)
SNAKE_COLOR = (255, 0, 84)

# Snake properties
SNAKE_SIZE = 20
SNAKE_SPEED = 20
SNAKE_BODY = [(WIDTH / 2, HEIGHT / 2)]
SNAKE_DIRECTION = (1, 0)

# Food properties
FOOD_SIZE = 20
food_pos = (random.randint(0, WIDTH - FOOD_SIZE), random.randint(0, HEIGHT - FOOD_SIZE))

# Score
score = 0
highest_score = 0

# Load font
font = pygame.font.Font(None, 36)

# Function to display score
def display_score():
    score_text = font.render("Score: " + str(score), True, TEXT_COLOR)
    WINDOW.blit(score_text, (10, 10))

# Function to display highest score
def display_highest_score():
    highest_score_text = font.render("Highest Score: " + str(highest_score), True, TEXT_COLOR)
    WINDOW.blit(highest_score_text, (WIDTH - highest_score_text.get_width() - 10, 10))

# Function to reset game and display "Game Over"
def reset_game():
    global SNAKE_BODY, SNAKE_DIRECTION, score, food_pos
    SNAKE_BODY = [(WIDTH / 2, HEIGHT / 2)]
    SNAKE_DIRECTION = (1, 0)
    score = 0
    food_pos = (random.randint(0, WIDTH - FOOD_SIZE), random.randint(0, HEIGHT - FOOD_SIZE))
    
    # Display "Game Over" text
    game_over_text = font.render("Game Over", True, TEXT_COLOR)
    WINDOW.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    
    # Wait for a short moment before resetting
    pygame.time.delay(2000)  # Wait for 2 seconds
    
    # Reset the screen
    WINDOW.fill(BGCOLOR)
    pygame.display.update()

# Main game loop
clock = pygame.time.Clock()
running = False
start_text_rendered = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if not running:
                # Start the game if Enter key is pressed
                if event.key == pygame.K_RETURN:
                    running = True
                    start_text_rendered = False
            else:
                # Change direction based on key presses
                if event.key == pygame.K_UP and SNAKE_DIRECTION != (0, 1):
                    SNAKE_DIRECTION = (0, -1)
                elif event.key == pygame.K_DOWN and SNAKE_DIRECTION != (0, -1):
                    SNAKE_DIRECTION = (0, 1)
                elif event.key == pygame.K_LEFT and SNAKE_DIRECTION != (1, 0):
                    SNAKE_DIRECTION = (-1, 0)
                elif event.key == pygame.K_RIGHT and SNAKE_DIRECTION != (-1, 0):
                    SNAKE_DIRECTION = (1, 0)

    if not running:
        # Display "Press Enter to Start" text
        if not start_text_rendered:
            start_text = font.render("Press Enter to Start", True, TEXT_COLOR)
            WINDOW.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
            pygame.display.update()
            start_text_rendered = True
        continue

    # Game starts

    # Move the snake
    new_head = (SNAKE_BODY[0][0] + SNAKE_SPEED * SNAKE_DIRECTION[0],
                SNAKE_BODY[0][1] + SNAKE_SPEED * SNAKE_DIRECTION[1])
    SNAKE_BODY.insert(0, new_head)

    # Check for collision with food
    if pygame.Rect(new_head, (SNAKE_SIZE, SNAKE_SIZE)).colliderect(pygame.Rect(food_pos, (FOOD_SIZE, FOOD_SIZE))):
        score += 1
        if score > highest_score:
            highest_score = score
        food_pos = (random.randint(0, WIDTH - FOOD_SIZE), random.randint(0, HEIGHT - FOOD_SIZE))
    else:
        SNAKE_BODY.pop()

    # Check for collision with walls or itself
    if (SNAKE_BODY[0][0] < 0 or SNAKE_BODY[0][0] >= WIDTH or
        SNAKE_BODY[0][1] < 0 or SNAKE_BODY[0][1] >= HEIGHT or
        len(SNAKE_BODY) != len(set(SNAKE_BODY))):
        reset_game()
        running = False  # Set running to False after the game ends
        
    # Draw everything
    WINDOW.fill(BGCOLOR)
    pygame.draw.rect(WINDOW, FOOD_COLOR, (*food_pos, FOOD_SIZE, FOOD_SIZE))

    for segment in SNAKE_BODY:
        pygame.draw.rect(WINDOW, SNAKE_COLOR, (*segment, SNAKE_SIZE, SNAKE_SIZE))

    display_score()
    display_highest_score()
    pygame.display.update()
    clock.tick(7)
