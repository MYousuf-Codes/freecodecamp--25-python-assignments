import pygame
import random
import sys

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        """Prevent 180° reversal."""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def update(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)

        if new_head in self.positions[3:]:
            return False  # Collision with self

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def render(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, self.color, (pos[0]*GRID_SIZE, pos[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def main():
    snake = Snake()
    food = Food()
    game_over = False

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                else:
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)

        if not game_over:
            if not snake.update():
                game_over = True

            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()

        snake.render(screen)
        food.render(screen)
        draw_text(screen, f"Score: {snake.score}", 36, 10, 10)

        if game_over:
            draw_text(screen, "Game Over! Press any key to restart", 36, WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2)

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()

