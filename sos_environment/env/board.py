

class Board:
    def __init__(self):
        # 0 is empty, 1 is S, 2 is O
        self.board = [0] * 64

    def reset(self):
        self.board = [0] * 64

    def get_board(self):
        return self.board

    def get_possible_moves(self):
        return [i for i, x in enumerate(self.board) if x == 0]

    def make_move(self, move, symbol):
        # if symbol == 1 then S
        # if symbol == 2 then O
        self.board[move] = symbol









