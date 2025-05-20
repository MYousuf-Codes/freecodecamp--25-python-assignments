from player import Player

class Board:
    def __init__(self):
        self.grid = [[" " for _ in range(3)] for _ in range(3)]

    def display(self):
        print("\nCurrent board:")
        for row in self.grid:
            print(" | ".join(row))
            print("-" * 9)
        print()

    def is_full(self):
        return all(cell != " " for row in self.grid for cell in row)

    def is_position_empty(self, row, col):
        return self.grid[row][col] == " "

    def make_move(self, row, col, symbol):
        self.grid[row][col] = symbol

    def check_winner(self, symbol):
        for i in range(3):
            if all(cell == symbol for cell in self.grid[i]) or all(row[i] == symbol for row in self.grid):
                return True
        if all(self.grid[i][i] == symbol for i in range(3)) or all(self.grid[i][2 - i] == symbol for i in range(3)):
            return True
        return False


class TicTacToeGame:
    def __init__(self):
        self.players = [Player("X"), Player("O")]
        self.board = Board()
        self.current_player_idx = 0

    @staticmethod
    def print_guide():
        print("\nTic-Tac-Toe Guide:")
        print("1 | 2 | 3")
        print("---------")
        print("4 | 5 | 6")
        print("---------")
        print("7 | 8 | 9\n")

    def switch_player(self):
        self.current_player_idx = 1 - self.current_player_idx

    def ask_replay(self):
        while True:
            choice = input("\nPlay again? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'.")

    def play(self):
        print("\n🎮 Welcome to Tic-Tac-Toe!")
        self.print_guide()

        while True:
            self.board = Board()  # Reset board
            while True:
                self.board.display()
                current_player = self.players[self.current_player_idx]
                current_player.make_move(self.board)

                if self.board.check_winner(current_player.symbol):
                    self.board.display()
                    print(f"🎉 Player {current_player.symbol} wins!")
                    current_player.score += 1
                    break

                if self.board.is_full():
                    self.board.display()
                    print("It's a draw! 🤝")
                    break

                self.switch_player()

            print(f"\n🏆 Scoreboard:")
            for player in self.players:
                print(f"Player {player.symbol}: {player.score}")

            if not self.ask_replay():
                print("Thanks for playing! 👋")
                break

if __name__ == "__main__":
    game = TicTacToeGame()
    game.play()