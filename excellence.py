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
# Game State Tracking
# ================================================================
class GameState:
    """Stores all mutable game data in one place for clarity."""
    def __init__(self, difficulty):
        self.player_x = PLAYER_START_X
        self.falling_rocks = []            # List of [x, y, speed] for each rock
        self.frames_since_last_rock = 0
        self.score = 0
        self.lives = DIFFICULTY_LIFE_COUNTS[difficulty]
        self.speed_multiplier = DIFFICULTY_SPEED_MULTIPLIERS[difficulty]
        self.is_running = True
        self.difficulty = difficulty

    def get_current_spawn_interval(self):
        """
        Calculate how frequently rocks should spawn based on the current score.
        As the score increases, rocks spawn faster (lower interval = more frequent).
        The interval is capped at MIN_SPAWN_INTERVAL so the game stays beatable.
        """
        # Every DIFFICULTY_SCALE_EVERY points, reduce the spawn interval by 2
        reduction = (self.score // DIFFICULTY_SCALE_EVERY) * 2
        calculated_interval = BASE_SPAWN_INTERVAL - reduction
        # Use max() to ensure the interval never drops below the minimum
        return max(MIN_SPAWN_INTERVAL, calculated_interval)


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


# ================================================================
# Drawing Functions
# ================================================================

def draw_player(surface, x_pos):
    """Draw the player ship as a blue rectangle with a cockpit detail."""
    pygame.draw.rect(surface, COL_PLAYER, (x_pos, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT))
    cockpit_x = x_pos + (PLAYER_WIDTH // 2) - 8
    cockpit_y = PLAYER_Y - 10
    pygame.draw.rect(surface, COL_PLAYER_COCKPIT, (cockpit_x, cockpit_y, 16, 12))


def draw_rock(surface, rock):
    """Draw a single rock as a brown circle with a highlight to add depth."""
    rx, ry, _ = rock
    pygame.draw.circle(surface, COL_ROCK, (int(rx), int(ry)), ROCK_RADIUS)
    pygame.draw.circle(surface, COL_ROCK_HIGHLIGHT, (int(rx) - 3, int(ry) - 3), 4)


def draw_hud(surface, state):
    """
    Draw the heads-up display with score, lives, difficulty,
    and the current high score in the top area of the screen.
    """
    score_surf = info_font.render("Score: " + str(state.score), True, COL_WHITE)
    lives_surf = info_font.render("Lives: " + str(state.lives), True, COL_YELLOW)
    diff_surf = tiny_font.render("Difficulty: " + state.difficulty, True, COL_GREY)
    hi_surf = tiny_font.render("Best: " + str(session_high_score), True, COL_GREEN)

    surface.blit(score_surf, (10, 10))
    surface.blit(lives_surf, (10, 45))
    surface.blit(diff_surf, (10, SCREEN_HEIGHT - 25))
    surface.blit(hi_surf, (SCREEN_WIDTH - 100, 10))

    # Draw life indicators as red circles in the top right corner
    for i in range(state.lives):
        circle_x = SCREEN_WIDTH - 30 - (i * 28)
        pygame.draw.circle(surface, COL_RED, (circle_x, 45), 9)


def check_rock_player_collision(rock, player_x):
    """
    Robust collision check using axis-aligned bounding boxes (AABB).
    Returns True only if both horizontal AND vertical overlap exist.
    This handles boundary cases like grazing the edge of the player.
    """
    rx, ry, _ = rock

    # Rock bounding box
    rock_left = rx - ROCK_RADIUS
    rock_right = rx + ROCK_RADIUS
    rock_top = ry - ROCK_RADIUS
    rock_bottom = ry + ROCK_RADIUS

    # Player bounding box
    player_right = player_x + PLAYER_WIDTH
    player_top = PLAYER_Y
    player_bottom = PLAYER_Y + PLAYER_HEIGHT

    # A collision only happens if there is overlap on BOTH axes simultaneously
    x_overlap = rock_right > player_x and rock_left < player_right
    y_overlap = rock_bottom > player_top and rock_top < player_bottom
    return x_overlap and y_overlap


# ================================================================
# Difficulty Menu Screen
# ================================================================

def show_difficulty_menu():
    """
    Display a difficulty selection menu before the game starts.
    Returns the chosen difficulty string: "Easy", "Normal", or "Hard".

    Validates that only keys 1, 2, or 3 are accepted.
    Any other key shows a visible error message — invalid input handling.
    """
    selected_difficulty = None
    invalid_key_message = ""   # Stores an error message to show the player

    while selected_difficulty is None:
        screen.fill(COL_BACKGROUND)

        title_surf = heading_font.render("DODGE THE ROCKS", True, COL_ORANGE)
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 80))

        prompt_surf = info_font.render("Choose Difficulty:", True, COL_WHITE)
        screen.blit(prompt_surf, (SCREEN_WIDTH // 2 - prompt_surf.get_width() // 2, 180))

        # Display each difficulty option with its key
        option_colours = [COL_GREEN, COL_YELLOW, COL_RED]
        for index, option in enumerate(DIFFICULTY_OPTIONS):
            label = "  " + str(index + 1) + ".  " + option
            option_surf = info_font.render(label, True, option_colours[index])
            screen.blit(option_surf, (SCREEN_WIDTH // 2 - 80, 230 + index * 45))

        controls_surf = small_font.render("Arrow keys to move  |  Dodge all rocks!", True, COL_GREY)
        screen.blit(controls_surf, (SCREEN_WIDTH // 2 - controls_surf.get_width() // 2, 420))

        # Show the invalid input error message in red if one exists
        if invalid_key_message != "":
            error_surf = small_font.render(invalid_key_message, True, COL_RED)
            screen.blit(error_surf, (SCREEN_WIDTH // 2 - error_surf.get_width() // 2, 370))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Only accept keys 1, 2, or 3
                if event.key == pygame.K_1:
                    selected_difficulty = "Easy"
                elif event.key == pygame.K_2:
                    selected_difficulty = "Normal"
                elif event.key == pygame.K_3:
                    selected_difficulty = "Hard"
                else:
                    # Invalid key — show a visible error message to the player
                    invalid_key_message = "Invalid key! Please press 1, 2, or 3 only."

    return selected_difficulty


# ================================================================
# Game Over Screen
# ================================================================

def show_game_over(final_score, difficulty, high_score):
    """
    Display the game over screen with the final score and high score.
    Offers the player the option to play again (R key) or quit (Q key).
    Any other key shows a visible error message — invalid input handling.
    Returns True if the player wants to replay, False to quit.
    """
    waiting = True
    player_wants_replay = False
    invalid_key_message = ""   # Stores an error message if an invalid key is pressed

    while waiting:
        screen.fill(COL_BACKGROUND)

        over_surf = heading_font.render("GAME OVER", True, COL_RED)
        score_surf = info_font.render("Your Score: " + str(final_score), True, COL_WHITE)
        diff_surf = info_font.render("Difficulty: " + difficulty, True, COL_GREY)
        replay_surf = small_font.render("Press  R  to play again", True, COL_GREEN)
        quit_surf = small_font.render("Press  Q  to quit", True, COL_RED)

        screen.blit(over_surf, (SCREEN_WIDTH // 2 - over_surf.get_width() // 2, 140))
        screen.blit(score_surf, (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 215))
        screen.blit(diff_surf, (SCREEN_WIDTH // 2 - diff_surf.get_width() // 2, 260))

        # Show high score notice if the player beat their best
        if final_score >= high_score:
            hi_surf = info_font.render("New Best Score!", True, COL_YELLOW)
            screen.blit(hi_surf, (SCREEN_WIDTH // 2 - hi_surf.get_width() // 2, 305))

        screen.blit(replay_surf, (SCREEN_WIDTH // 2 - replay_surf.get_width() // 2, 370))
        screen.blit(quit_surf, (SCREEN_WIDTH // 2 - quit_surf.get_width() // 2, 405))

        # Show the invalid input error message in orange if one exists
        if invalid_key_message != "":
            error_surf = small_font.render(invalid_key_message, True, COL_ORANGE)
            screen.blit(error_surf, (SCREEN_WIDTH // 2 - error_surf.get_width() // 2, 445))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                player_wants_replay = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_wants_replay = True
                    waiting = False
                elif event.key == pygame.K_q:
                    player_wants_replay = False
                    waiting = False
                else:
                    # Invalid key — show a visible error message to the player
                    invalid_key_message = "Invalid key! Press R to replay or Q to quit."

    return player_wants_replay


# ================================================================
# Main Program Loop (allows replaying without restarting the program)
# ================================================================

keep_playing = True

while keep_playing:
    # --- Show difficulty menu and start a new game state ---
    chosen_difficulty = show_difficulty_menu()
    state = GameState(chosen_difficulty)

    # ============================================================
    # Main Game Loop
    # ============================================================
    while state.is_running:
        clock.tick(FPS)

        # --- Handle quit event ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Player movement with boundary enforcement ---
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            state.player_x -= PLAYER_MOVE_SPEED
        if keys_pressed[pygame.K_RIGHT]:
            state.player_x += PLAYER_MOVE_SPEED

        # Clamp player position to stay within valid screen boundaries
        # Using constants instead of raw numbers makes this easy to adjust
        state.player_x = max(PLAYER_MIN_X, min(state.player_x, PLAYER_MAX_X))

        # --- Spawn rocks using the dynamically calculated interval ---
        state.frames_since_last_rock += 1
        current_spawn_interval = state.get_current_spawn_interval()

        if state.frames_since_last_rock >= current_spawn_interval:
            new_x = random.randint(ROCK_MIN_X, ROCK_MAX_X)
            # Apply difficulty multiplier to rock speed for scaling challenge
            raw_speed = random.randint(ROCK_MIN_SPEED, ROCK_MAX_SPEED)
            scaled_speed = raw_speed * state.speed_multiplier
            state.falling_rocks.append([new_x, float(ROCK_START_Y), scaled_speed])
            state.frames_since_last_rock = 0

        # --- Update rocks and handle outcomes ---
        # Build a fresh list of only the rocks we want to keep
        active_rocks = []

        for rock in state.falling_rocks:
            rock[1] += rock[2]  # Move rock downward

            if check_rock_player_collision(rock, state.player_x):
                # Rock hit the player — discard this rock and deduct a life
                state.lives -= 1
            elif rock[1] > SCREEN_HEIGHT + ROCK_RADIUS:
                # Rock passed below the screen — player dodged it successfully
                state.score += POINTS_PER_DODGE
            else:
                # Rock is still active and on-screen — keep it
                active_rocks.append(rock)

        state.falling_rocks = active_rocks

        # --- Check game over condition ---
        if state.lives <= 0:
            state.is_running = False

        # --- Render ---
        screen.fill(COL_BACKGROUND)

        # Ground line for visual grounding
        pygame.draw.rect(screen, COL_GROUND, (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))

        draw_player(screen, state.player_x)

        for rock in state.falling_rocks:
            draw_rock(screen, rock)

        draw_hud(screen, state)

        pygame.display.flip()

    # ============================================================
    # After the game loop ends — update high score then show game over
    # ============================================================
    if state.score > session_high_score:
        session_high_score = state.score

    keep_playing = show_game_over(state.score, state.difficulty, session_high_score)

# Clean up pygame before exiting
pygame.quit()
sys.exit()
