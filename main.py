import pygame
import random
from collections import deque

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 650

ROWS = 10
COLS = 10

CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous AI Treasure Hunt Agent")

# Fonts
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)

# Clock
clock = pygame.time.Clock()

# AI movement delay
MOVE_DELAY = 300
last_move_time = pygame.time.get_ticks()

# Timer
TIME_LIMIT = 30
start_ticks = pygame.time.get_ticks()

# Player starting position
player_pos = [0, 0]

# Random treasure position
treasure_pos = [
    random.randint(5, 9),
    random.randint(5, 9)
]

# Random trap generation
traps = []

while len(traps) < 10:
    trap = [
        random.randint(0, 9),
        random.randint(0, 9)
    ]
    if (
        trap != player_pos
        and trap != treasure_pos
        and trap not in traps
    ):
        traps.append(trap)

# BFS Algorithm
def bfs(start, goal):
    queue = deque()
    queue.append((start, []))
    visited = set()
    visited.add(tuple(start))
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for dx, dy in directions:
            nx = current[0] + dx
            ny = current[1] + dy
            next_cell = [nx, ny]
            if (
                0 <= nx < ROWS
                and 0 <= ny < COLS
                and tuple(next_cell) not in visited
                and next_cell not in traps
            ):
                visited.add(tuple(next_cell))
                queue.append((next_cell, path + [next_cell]))
    return []

# AI Hint Generator
def get_ai_hint():
    path = bfs(player_pos, treasure_pos)
    if not path:
        return "AI: No Safe Path Found!"
    next_step = path[0]
    if next_step[0] > player_pos[0]:
        return "AI Hint: MOVE DOWN"
    if next_step[0] < player_pos[0]:
        return "AI Hint: MOVE UP"
    if next_step[1] > player_pos[1]:
        return "AI Hint: MOVE RIGHT"
    if next_step[1] < player_pos[1]:
        return "AI Hint: MOVE LEFT"
    return "AI: Exploring..."

# Draw grid
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, GRAY, rect, 1)

# Draw objects
def draw_objects():
    # Draw treasure
    treasure_rect = pygame.Rect(
        treasure_pos[1] * CELL_SIZE,
        treasure_pos[0] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )
    pygame.draw.rect(screen, GOLD, treasure_rect)

    # Draw traps
    for trap in traps:
        trap_rect = pygame.Rect(
            trap[1] * CELL_SIZE,
            trap[0] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, RED, trap_rect)

    # Draw AI player
    player_rect = pygame.Rect(
        player_pos[1] * CELL_SIZE,
        player_pos[0] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )
    pygame.draw.rect(screen, BLUE, player_rect)

# Main game loop
running = True
message = ""

while running:
    screen.fill(WHITE)
    draw_grid()
    draw_objects()

    # AI Hint Display
    hint = get_ai_hint()
    hint_text = font.render(hint, True, BLACK)
    screen.blit(hint_text, (20, 610))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI Autonomous Movement
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > MOVE_DELAY:
        path = bfs(player_pos, treasure_pos)
        if path:
            player_pos = path[0]
        last_move_time = current_time

    # Check win
    if player_pos == treasure_pos:
        message = "AI SUCCESSFULLY FOUND THE TREASURE!"
        running = False

    # Check trap collision
    if player_pos in traps:
        message = "AI HIT A TRAP!"
        running = False

    # Timer
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining_time = max(0, TIME_LIMIT - seconds)

    if remaining_time <= 0:
        message = "TIME OVER! AI FAILED!"
        running = False

    # Display timer
    timer_text = font.render(f"Time Left: {remaining_time}", True, BLACK)
    screen.blit(timer_text, (400, 610))

    pygame.display.update()
    clock.tick(60)

# Final screen
screen.fill(WHITE)
final_text = big_font.render(
    message,
    True,
    GREEN if "SUCCESSFULLY" in message else RED
)
screen.blit(final_text, (20, 250))

exit_text = font.render("Press ESC to Exit", True, BLACK)
screen.blit(exit_text, (190, 330))
pygame.display.update()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                waiting = False

pygame.quit()