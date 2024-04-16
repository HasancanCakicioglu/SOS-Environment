import numpy as np

from sos_environment.env.board import Board
import unittest

Board().reset()




class TestBoardClass(unittest.TestCase):
    def test_reset(self):
        board = Board()
        board.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        board.reset()
        self.assertEqual(board.board, [0] * 256)

    def test_get_board(self):
        board = Board()
        self.assertEqual(board.get_board(), [0] * 256)

    def test_get_possible_moves(self):
        board = Board()
        board.board = [0, 1, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(board.get_possible_moves(), [0, 2, 3, 4, 5, 6, 7, 8])

    def test_make_move(self):
        board = Board()
        board.make_move(0, 1)
        self.assertEqual(board.board, [1] + [0] * 255)
        board.make_move(255, 2)
        self.assertEqual(board.board, [1] + [0] * 254 + [2])

    def test_action_mask(self):
        board = Board()
        board.make_move(0,2)

        one_hot_encoded = np.eye(3)[board.get_board()]
        new_shape = (8, 8, 3)
        observation = one_hot_encoded.reshape(new_shape)
        action_mask = np.where(np.array(board.get_board()) == 0, 1, 0)
        print(observation.shape,observation)
        print(action_mask.shape,action_mask)

if __name__ == '__main__':
    unittest.main()
