import numpy as np
import pygame
import sys
import math

# Constants
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

class ConnectFour:
    def __init__(self):
        pygame.init()  # ✅ Must be first before any pygame.* method
        pygame.display.set_caption("Connect Four")

        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.turn = 0
        self.game_over = False
        self.width = COLUMN_COUNT * SQUARESIZE
        self.height = (ROW_COUNT + 1) * SQUARESIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("monospace", 75)

        self.draw_board()

    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                        int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                          self.height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                             self.height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece):
        # Check horizontal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Check vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True

        return False

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                    posx = event.pos[0]
                    color = RED if self.turn == 0 else YELLOW
                    pygame.draw.circle(self.screen, color, (posx, int(SQUARESIZE / 2)), RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if self.is_valid_location(col):
                        row = self.get_next_open_row(col)
                        player_piece = 1 if self.turn == 0 else 2
                        self.drop_piece(row, col, player_piece)

                        if self.winning_move(player_piece):
                            label = self.font.render(f"Player {player_piece} wins!!", 1,
                                                     RED if player_piece == 1 else YELLOW)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True

                        self.draw_board()
                        self.turn ^= 1  # Toggle between 0 and 1

                        if self.game_over:
                            pygame.time.wait(3000)

if __name__ == "__main__":
    ConnectFour().run()