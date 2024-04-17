import numpy as np


class Board:
    def __init__(self):
        # 0 is empty, 1 is S, 2 is O
        self.board = [0] * 64
        self.sos_count = 0

    def reset(self):
        self.board = [0] * 64

    def get_board(self):
        return self.board

    def get_possible_moves(self):
        return [i for i, x in enumerate(self.board) if x == 0]

    def make_move(self, move):
        # if symbol == 1 then S
        # if symbol == 2 then O
        if self.board[move[0]]==0:
            self.board[move[0]] = 1 if move[1] == 0 else 2
        else:
            return -1
        
        return self.calculate_reward()

    def calculate_reward(self):
        new_sos_count = self.calculate_sos_count()
        reward = new_sos_count - self.sos_count
        self.sos_count = new_sos_count
        return reward
    
    
    def calculate_sos_count(self):
        matrix = np.array(self.board).reshape(8, 8)
        sos_count = 0
        n = len(matrix)
        for y in range(n):
            for x in range(n):
                if matrix[y][x] == 1:
                    # Sağa doğru SOS kontrolü
                    if x + 2 < n and matrix[y][x + 1] == 2 and matrix[y][x + 2] == 1:
                        sos_count += 1
                    # Aşağı doğru SOS kontrolü
                    if y + 2 < n and matrix[y + 1][x] == 2 and matrix[y + 2][x] == 1:
                        sos_count += 1
                    # Sağ çapraz doğru SOS kontrolü
                    if x + 2 < n and y + 2 < n and matrix[y + 1][x + 1] == 2 and matrix[y + 2][x + 2] == 1:
                        sos_count += 1
                    # Sol çapraz doğru SOS kontrolü
                    if x - 2 >= 0 and y + 2 < n and matrix[y + 1][x - 1] == 2 and matrix[y + 2][x - 2] == 1:
                        sos_count += 1
        return sos_count

    def check_game_over(self):
        return not any(element == 0 for element in self.board)

    def __str__(self):
        result = ""
        for i in range(8):
            result += "|" + "---|" * 8 + "\n"
            result += "|"
            for j in range(8):
                if self.board[i * 8 + j] == 1:
                    result += " S |"
                elif self.board[i * 8 + j] == 2:
                    result += " O |"
                else:
                    result += "   |"  # Boşluk bırak
            result += "\n"
        result += "|" + "---|" * 8 + "\n"
        return result












