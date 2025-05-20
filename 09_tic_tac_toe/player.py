class Player:
    def __init__(self, symbol):
        self.symbol = symbol
        self.score = 0

    def make_move(self, board):
        while True:
            try:
                move = int(input(f"Player {self.symbol}, choose a position (1-9): "))
                if move < 1 or move > 9:
                    raise ValueError("Invalid range. Choose between 1 and 9.")
                row, col = (move - 1) // 3, (move - 1) % 3
                if not board.is_position_empty(row, col):
                    print("That position is already taken. Try another one.")
                    continue
                board.make_move(row, col, self.symbol)
                break
            except ValueError as e:
                print(f"Error: {e}")
