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
