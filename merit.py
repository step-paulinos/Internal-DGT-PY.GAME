# Dodge the Rocks - Merit Version (v2.0)
# A well-structured game where the player dodges falling rocks
# Merit improvements: descriptive variable names, meaningful comments, boundary case handling

import pygame
import random

pygame.init()

# -----------------------------------------------
# Screen and display setup
# -----------------------------------------------
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Rocks - Merit")
clock = pygame.time.Clock()
FRAMES_PER_SECOND = 60

# -----------------------------------------------
# Fonts for displaying text on screen
# -----------------------------------------------
heading_font = pygame.font.SysFont("Arial", 48)
info_font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

# -----------------------------------------------
# Colour definitions (RGB tuples)
# -----------------------------------------------
COLOUR_BACKGROUND = (15, 15, 30)     # Dark blue-black
COLOUR_PLAYER = (50, 150, 255)       # Bright blue player
COLOUR_ROCK = (160, 80, 30)          # Brown rocks
COLOUR_WHITE = (255, 255, 255)
COLOUR_RED = (220, 50, 50)
COLOUR_YELLOW = (255, 220, 0)
COLOUR_GREEN = (50, 210, 80)
COLOUR_GREY = (120, 120, 120)

# -----------------------------------------------
# Player settings - descriptive names make this easy to read
# -----------------------------------------------
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 15
PLAYER_MOVE_SPEED = 6          # Pixels per frame the player moves
PLAYER_START_X = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
PLAYER_Y_POSITION = SCREEN_HEIGHT - 60  # Player stays near the bottom

# -----------------------------------------------
# Rock spawning settings
# -----------------------------------------------
ROCK_SPAWN_INTERVAL = 35       # Frames between each new rock spawning
ROCK_MIN_SPEED = 3
ROCK_MAX_SPEED = 7
ROCK_RADIUS = 12               # Size of each rock circle

# -----------------------------------------------
# Game state variables
# -----------------------------------------------
player_x_position = PLAYER_START_X
falling_rocks = []             # List of all active rocks [ [x, y, speed], ... ]
frames_since_last_rock = 0    # Tracks when to spawn the next rock
current_score = 0
player_lives = 3
is_game_running = True


def draw_player(surface, x_pos):
    """Draw the player's ship as a blue rectangle at the given x position."""
    pygame.draw.rect(surface, COLOUR_PLAYER,
                     (x_pos, PLAYER_Y_POSITION, PLAYER_WIDTH, PLAYER_HEIGHT))
    # Draw a small cockpit on top of the ship
    cockpit_x = x_pos + PLAYER_WIDTH // 2 - 8
    cockpit_y = PLAYER_Y_POSITION - 10
    pygame.draw.rect(surface, COLOUR_WHITE, (cockpit_x, cockpit_y, 16, 12))


def draw_rock(surface, rock):
    """Draw a single rock as a brown circle at its current position."""
    rock_x, rock_y, _ = rock
    pygame.draw.circle(surface, COLOUR_ROCK, (int(rock_x), int(rock_y)), ROCK_RADIUS)
    # Inner highlight to make it look more like a rock
    pygame.draw.circle(surface, (200, 120, 60), (int(rock_x) - 3, int(rock_y) - 3), 4)


def check_collision(rock, player_x):
    """
    Check if a rock has hit the player using bounding box collision.
    Returns True if the rock and player are overlapping.
    """
    rock_x, rock_y, _ = rock
    # Create collision boxes for both objects
    rock_left = rock_x - ROCK_RADIUS
    rock_right = rock_x + ROCK_RADIUS
    rock_top = rock_y - ROCK_RADIUS
    rock_bottom = rock_y + ROCK_RADIUS

    player_right = player_x + PLAYER_WIDTH
    player_bottom = PLAYER_Y_POSITION + PLAYER_HEIGHT

    # Check if the two boxes overlap on both axes
    horizontal_overlap = rock_right > player_x and rock_left < player_right
    vertical_overlap = rock_bottom > PLAYER_Y_POSITION and rock_top < player_bottom
    return horizontal_overlap and vertical_overlap


def draw_hud(surface, score, lives):
    """Draw the Heads-Up Display showing score and lives in the top corners."""
    score_surface = info_font.render("Score: " + str(score), True, COLOUR_WHITE)
    lives_surface = info_font.render("Lives: " + str(lives), True, COLOUR_YELLOW)
    surface.blit(score_surface, (10, 10))
    surface.blit(lives_surface, (10, 45))

    # Draw lives as small coloured circles for visual clarity
    for i in range(lives):
        heart_x = SCREEN_WIDTH - 30 - (i * 30)
        pygame.draw.circle(surface, COLOUR_RED, (heart_x, 25), 10)


# -----------------------------------------------
# Main game loop
# -----------------------------------------------
while is_game_running:
    clock.tick(FRAMES_PER_SECOND)

    # --- Handle window close and quit events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False

    # --- Handle player keyboard input ---
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT]:
        player_x_position -= PLAYER_MOVE_SPEED
    if keys_pressed[pygame.K_RIGHT]:
        player_x_position += PLAYER_MOVE_SPEED

    # Boundary checking: keep player fully inside the screen edges
    if player_x_position < 0:
        player_x_position = 0
    if player_x_position > SCREEN_WIDTH - PLAYER_WIDTH:
        player_x_position = SCREEN_WIDTH - PLAYER_WIDTH

    # --- Spawn new rocks at regular intervals ---
    frames_since_last_rock += 1
    if frames_since_last_rock >= ROCK_SPAWN_INTERVAL:
        new_rock_x = random.randint(ROCK_RADIUS, SCREEN_WIDTH - ROCK_RADIUS)
        new_rock_speed = random.randint(ROCK_MIN_SPEED, ROCK_MAX_SPEED)
        falling_rocks.append([new_rock_x, -ROCK_RADIUS, new_rock_speed])
        frames_since_last_rock = 0

    # --- Update rock positions and detect events ---
    rocks_to_remove = []

    for rock in falling_rocks:
        # Move each rock downward by its speed
        rock[1] += rock[2]

        # Rock passed the bottom of the screen — player dodged it, award a point
        if rock[1] > SCREEN_HEIGHT + ROCK_RADIUS:
            rocks_to_remove.append(rock)
            current_score += 1

        # Boundary case: rock hit the player — remove rock and deduct a life
        elif check_collision(rock, player_x_position):
            rocks_to_remove.append(rock)
            player_lives -= 1

    # Clean up rocks that are no longer active
    for finished_rock in rocks_to_remove:
        if finished_rock in falling_rocks:
            falling_rocks.remove(finished_rock)

    # Check win/lose condition: game ends when player runs out of lives
    if player_lives <= 0:
        is_game_running = False

    # --- Render the frame ---
    screen.fill(COLOUR_BACKGROUND)

    # Draw a subtle ground line to show the playfield boundary
    pygame.draw.line(screen, COLOUR_GREY, (0, SCREEN_HEIGHT - 40),
                     (SCREEN_WIDTH, SCREEN_HEIGHT - 40), 1)

    draw_player(screen, player_x_position)

    for rock in falling_rocks:
        draw_rock(screen, rock)

    draw_hud(screen, current_score, player_lives)

    pygame.display.flip()

# -----------------------------------------------
# Game Over Screen
# -----------------------------------------------
screen.fill(COLOUR_BACKGROUND)
game_over_text = heading_font.render("GAME OVER", True, COLOUR_RED)
final_score_text = info_font.render("Final Score: " + str(current_score), True, COLOUR_WHITE)
exit_prompt_text = small_font.render("Close the window to exit", True, COLOUR_GREY)

# Centre the text on the screen
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 180))
screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 250))
screen.blit(exit_prompt_text, (SCREEN_WIDTH // 2 - exit_prompt_text.get_width() // 2, 310))
pygame.display.flip()

# Wait for the player to close the window
waiting_for_close = True
while waiting_for_close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_close = False

pygame.quit()
