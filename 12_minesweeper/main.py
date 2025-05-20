import random

class Minesweeper:
    def __init__(self, size=5, mines=5):
        self.size = size
        self.mines = mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.mine_locations = set()
        self.generate_board()

    def generate_board(self):
        mine_positions = random.sample(range(self.size * self.size), self.mines)
        for pos in mine_positions:
            r, c = divmod(pos, self.size)
            self.mine_locations.add((r, c))

        self.numbers = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for r, c in self.mine_locations:
            self.numbers[r][c] = -1
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.numbers[nr][nc] != -1:
                        self.numbers[nr][nc] += 1

    def print_board(self):
        print("\n    " + " ".join(str(i) for i in range(self.size)))
        print("   " + "--" * self.size)
        for r in range(self.size):
            row = [self.get_display_value(r, c) for c in range(self.size)]
            print(f"{r} | " + " ".join(row))
        print()

    def get_display_value(self, r, c):
        if self.revealed[r][c]:
            if self.numbers[r][c] == -1:
                return '💣'
            elif self.numbers[r][c] == 0:
                return '.'
            else:
                return str(self.numbers[r][c])
        else:
            return '■'

    def reveal(self, r, c):
        if self.revealed[r][c]:
            return
        self.revealed[r][c] = True

        if self.numbers[r][c] == -1:
            print("\n💥 Game Over! You hit a mine.")
            self.reveal_all()
            self.print_board()
            exit()
        elif self.numbers[r][c] == 0:
            # Recursively reveal neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        self.reveal(nr, nc)

    def reveal_all(self):
        for r in range(self.size):
            for c in range(self.size):
                self.revealed[r][c] = True

    def check_win(self):
        for r in range(self.size):
            for c in range(self.size):
                if not self.revealed[r][c] and (r, c) not in self.mine_locations:
                    return False
        return True

    def play(self):
        print("🎮 Welcome to Command Line Minesweeper!")
        while True:
            self.print_board()
            try:
                r, c = map(int, input("Enter row and column to reveal (e.g., 1 2): ").split())
                if 0 <= r < self.size and 0 <= c < self.size:
                    self.reveal(r, c)
                    if self.check_win():
                        self.reveal_all()
                        self.print_board()
                        print("🎉 Congratulations! You cleared all the mines!")
                        break
                else:
                    print("⚠️ Invalid input. Please enter values within board range.")
            except ValueError:
                print("⚠️ Invalid input format. Please enter two integers separated by space.")

# Run the game
if __name__ == "__main__":
    game = Minesweeper(size=5, mines=5)
    game.play()