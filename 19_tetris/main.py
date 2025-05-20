import pygame
import random
from typing import List, Dict

# Initialize Pygame
pygame.init()

# === Constants ===
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

FONT_SIZE = 36
BIG_FONT_SIZE = 48
FALL_SPEED = 0.5  # seconds
BASE_SCORE = 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Shapes and their colors
SHAPES = [
    [[1, 1, 1, 1]],            # I
    [[1, 1], [1, 1]],          # O
    [[1, 1, 1], [0, 1, 0]],    # T
    [[1, 1, 1], [1, 0, 0]],    # L
    [[1, 1, 1], [0, 0, 1]],    # J
    [[1, 1, 0], [0, 1, 1]],    # S
    [[0, 1, 1], [1, 1, 0]]     # Z
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid: List[List[int]] = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece: Dict = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0

    def new_piece(self) -> Dict:
        shape = random.choice(SHAPES)
        return {
            'shape': shape,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def is_valid_position(self, piece: Dict, x: int, y: int) -> bool:
        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def rotate_piece(self):
        rotated = [list(row) for row in zip(*self.current_piece['shape'][::-1])]
        original_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        if not self.is_valid_position(self.current_piece, self.current_piece['x'], self.current_piece['y']):
            self.current_piece['shape'] = original_shape

    def clear_full_lines(self):
        lines_before = len(self.grid)
        self.grid = [row for row in self.grid if not all(row)]
        lines_cleared = lines_before - len(self.grid)
        for _ in range(lines_cleared):
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        if lines_cleared:
            self.lines_cleared += lines_cleared
            self.score += lines_cleared * BASE_SCORE * self.level
            self.level = self.lines_cleared // 10 + 1

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    color = SHAPE_COLORS[cell - 1]
                    pygame.draw.rect(self.screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def draw_piece(self):
        shape = self.current_piece['shape']
        color = SHAPE_COLORS[SHAPES.index(shape)]
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, (
                        (self.current_piece['x'] + j) * BLOCK_SIZE,
                        (self.current_piece['y'] + i) * BLOCK_SIZE,
                        BLOCK_SIZE - 1, BLOCK_SIZE - 1
                    ))

    def draw_ui(self):
        font = pygame.font.Font(None, FONT_SIZE)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))
        self.screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 10, 50))

    def hard_drop(self):
        while self.is_valid_position(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
            self.current_piece['y'] += 1

    def lock_piece(self):
        shape_index = SHAPES.index(self.current_piece['shape']) + 1
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = shape_index
        self.clear_full_lines()
        self.current_piece = self.new_piece()
        if not self.is_valid_position(self.current_piece, self.current_piece['x'], self.current_piece['y']):
            self.game_over = True

    def run(self):
        fall_time = 0
        while not self.game_over:
            fall_time += self.clock.get_rawtime()
            self.clock.tick()

            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.is_valid_position(self.current_piece, self.current_piece['x'] - 1, self.current_piece['y']):
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.is_valid_position(self.current_piece, self.current_piece['x'] + 1, self.current_piece['y']):
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_DOWN:
                        if self.is_valid_position(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()

            # Handle gravity
            if fall_time >= FALL_SPEED * 1000:
                if self.is_valid_position(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                    self.current_piece['y'] += 1
                else:
                    self.lock_piece()
                fall_time = 0

            # Draw everything
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece()
            self.draw_ui()
            pygame.display.flip()

        # Game Over
        font = pygame.font.Font(None, BIG_FONT_SIZE)
        text = font.render("GAME OVER", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == '__main__':
    Tetris().run()
    pygame.quit()
