# Dodge the Rocks - Achieved Version (v1.0)
# A simple game where the player dodges falling rocks
# Uses: variables, input, output, conditionals, loops, lists

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
