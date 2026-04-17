# Dodge the Rocks - Excellence Version (v3.0)
# A flexible and robust game where the player dodges falling rocks
# Excellence improvements: constants replace all literals, robust input handling,
# difficulty levels, high score, and thorough edge case management

import pygame
import random
import sys

pygame.init()

# ================================================================
# CONSTANTS - All game values defined here for easy adjustment
# ================================================================

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

# Frame rate
FPS = 60

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 15
PLAYER_MOVE_SPEED = 6
PLAYER_START_X = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
PLAYER_Y = SCREEN_HEIGHT - 60       # Y position of the player (fixed row)
PLAYER_MIN_X = 0                    # Left screen boundary for player
PLAYER_MAX_X = SCREEN_WIDTH - PLAYER_WIDTH  # Right boundary

# Rock settings
ROCK_RADIUS = 12
ROCK_MIN_SPEED = 3
ROCK_MAX_SPEED = 7
ROCK_START_Y = -ROCK_RADIUS         # Rocks start just above the top of screen
ROCK_MIN_X = ROCK_RADIUS            # Keep rocks fully on-screen horizontally
ROCK_MAX_X = SCREEN_WIDTH - ROCK_RADIUS

# Difficulty scaling: every this many points, spawn rate gets faster
DIFFICULTY_SCALE_EVERY = 5          # Speed up after every 5 points
BASE_SPAWN_INTERVAL = 35            # Starting frames between rock spawns
MIN_SPAWN_INTERVAL = 12             # Fastest possible spawn rate (cap so it's fair)

# Scoring
POINTS_PER_DODGE = 1

# Colours
COL_BACKGROUND = (15, 15, 30)
COL_PLAYER = (50, 150, 255)
COL_PLAYER_COCKPIT = (200, 230, 255)
COL_ROCK = (160, 80, 30)
COL_ROCK_HIGHLIGHT = (200, 120, 60)
COL_WHITE = (255, 255, 255)
COL_RED = (220, 50, 50)
COL_YELLOW = (255, 220, 0)
COL_GREEN = (50, 210, 80)
COL_GREY = (120, 120, 120)
COL_DARK_GREY = (60, 60, 60)
COL_ORANGE = (255, 140, 0)
COL_GROUND = (40, 40, 60)

# Starting lives
STARTING_LIVES = 3

# Difficulty options shown on the menu
DIFFICULTY_OPTIONS = ["Easy", "Normal", "Hard"]
DIFFICULTY_LIFE_COUNTS = {"Easy": 5, "Normal": 3, "Hard": 1}
DIFFICULTY_SPEED_MULTIPLIERS = {"Easy": 0.7, "Normal": 1.0, "Hard": 1.4}

# ================================================================
# Setup
# ================================================================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Rocks - Excellence")
clock = pygame.time.Clock()

heading_font = pygame.font.SysFont("Arial", 48)
info_font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)
tiny_font = pygame.font.SysFont("Arial", 16)

# High score persists across rounds within the same session
session_high_score = 0
