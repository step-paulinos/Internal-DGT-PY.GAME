# Dodge the Rocks - Achieved Version (v1.0)
# A simple game where the player dodges falling rocks
# Uses: variables, input, output, conditionals, loops, lists
# test
import pygame
import random

# Start up pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Dodge the Rocks")

# Set up the clock for controlling game speed
clock = pygame.time.Clock()

# Set up font for displaying text
font = pygame.font.SysFont("Arial", 28)

# Colours (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 220)
RED = (200, 50, 50)
GREY = (150, 150, 150)
GREEN = (50, 200, 50)
YELLOW = (255, 220, 0)

# Player starting position and size
player_x = 275
player_y = 430
player_width = 50
player_height = 20

# Rock settings
rocks = []           # List to store all current rocks on screen
rock_timer = 0       # Counts how long since last rock spawned

# Game variables
score = 0
game_running = True
lives = 3

# Main game loop
while game_running:
    clock.tick(60)  # Run at 60 frames per second

    # --- Handle Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # --- Player Movement ---
    # Check which keys are pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5  # Move left
    if keys[pygame.K_RIGHT]:
        player_x += 5  # Move right

    # Stop player from going off the screen edges
    if player_x < 0:
        player_x = 0
    if player_x > 550:
        player_x = 550

    # --- Spawn Rocks ---
    rock_timer += 1
    if rock_timer >= 40:  # A new rock spawns every 40 frames
        rock_x = random.randint(0, 570)
        rock_y = -20
        rock_speed = random.randint(3, 7)
        rocks.append([rock_x, rock_y, rock_speed])  # Add rock to the list
        rock_timer = 0

    # --- Move Rocks and Check Collisions ---
    rocks_to_remove = []  # Rocks that have gone off screen or hit the player

    for rock in rocks:
        rock[1] += rock[2]  # Move rock down by its speed

        # Check if rock went off the bottom of the screen
        if rock[1] > 520:
            rocks_to_remove.appgend(rock)
            score += 1  # Player earns a point for dodging a rock

        # Check if rock hit the player (simple box collision)
        if (rock[0] < player_x + player_width and
                rock[0] + 20 > player_x and
                rock[1] < player_y + player_height and
                rock[1] + 20 > player_y):
            rocks_to_remove.append(rock)
            lives -= 1  # Player loses a life

    # Remove rocks that are done
    for rock in rocks_to_remove:
        if rock in rocks:
            rocks.remove(rock)

    # Check if game is over
    if lives <= 0:
        game_running = False

    # --- Draw Everything ---
    screen.fill(BLACK)  # Clear the screen with black background

    # Draw the player as a blue rectangle
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # Draw all the rocks as grey circles
    for rock in rocks:
        pygame.draw.circle(screen, GREY, (rock[0], rock[1]), 10)

    # Display the score and lives
    score_text = font.render("Score: " + str(score), True, WHITE)
    lives_text = font.render("Lives: " + str(lives), True, YELLOW)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 45))

    # Update the display
    pygame.display.flip()

# --- Game Over Screen ---
screen.fill(BLACK)
over_font = pygame.font.SysFont("Arial", 48)
over_text = over_font.render("GAME OVER", True, RED)
final_text = font.render("Final Score: " + str(score), True, WHITE)
quit_text = font.render("Close the window to exit", True, GREY)

screen.blit(over_text, (170, 180))
screen.blit(final_text, (220, 250))
screen.blit(quit_text, (170, 300))
pygame.display.flip()

# Wait until the player closes the window
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False

pygame.quit()
