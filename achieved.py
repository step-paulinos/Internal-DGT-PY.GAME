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
