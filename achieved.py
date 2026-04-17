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
