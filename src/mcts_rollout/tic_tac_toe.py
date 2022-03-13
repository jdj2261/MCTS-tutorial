import re
import enum

from copy import deepcopy
from mcts import *

class Marker:
    X = 'X'
    O = 'O'
    EMPTY = '.'

class GAME_RESULT(enum.Enum):
    WIN = 0
    LOSE = 1
    DRAW = 2

class TTTBoard:
    def __init__(self, board=None, size=3):
        self.cur_player = Marker.X
        self.next_player = Marker.O
        self.empty = Marker.EMPTY

        self.first_player = Marker.X
        self.second_player = Marker.O
        self.winner = None

        self.position = {}
        self.size = size
        self._create_board()

        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
    
    def _create_board(self):
        for row in range(self.size):
            for col in range(self.size):
                self.position[row, col] = self.empty

    def __str__(self):
        board_str = "==" * self.size + "\n"
        for row in range(self.size):
            for col in range(self.size):
                board_str += " %s" % self.position[row, col]
            board_str += '\n'
        board_str += "==" * self.size + "\n"

        if self.cur_player == Marker.X:
            board_str += f'{self.cur_player}, Your turn!!\n'
        
        elif self.cur_player == Marker.O:
            board_str += f'{self.cur_player}, Your turn!!!\n'

        return board_str

    def move(self, row, col):
        board = TTTBoard(self)
        board.position[row, col] = self.cur_player
        board.cur_player, board.next_player = board.next_player, board.cur_player
        return board

    def evaluate_game(self):
        for row in range(self.size):
            win_cnt = 0
            lose_cnt = 0
            for col in range(self.size):
                if self.position[row, col] == self.first_player:
                    win_cnt += 1
                if self.position[row, col] == self.second_player:
                    lose_cnt += 1
                if win_cnt == self.size:
                    self.winner = self.first_player
                    return GAME_RESULT.WIN
                if lose_cnt == self.size:
                    self.winner = self.second_player
                    return GAME_RESULT.LOSE

        for col in range(self.size):
            win_cnt = 0
            lose_cnt = 0
            for row in range(self.size):
                if self.position[row, col] == self.first_player:
                    win_cnt += 1
                if self.position[row, col] == self.second_player:
                    lose_cnt += 1
                if win_cnt == self.size:
                    self.winner = self.first_player
                    return GAME_RESULT.WIN
                if lose_cnt == self.size:
                    self.winner = self.second_player
                    return GAME_RESULT.LOSE
        
        win_cnt = 0
        lose_cnt = 0
        for row in range(self.size):
            col = row
            if self.position[row, col] == self.first_player:
                win_cnt += 1
            if self.position[row, col] == self.second_player:
                lose_cnt += 1
            if win_cnt == self.size:
                self.winner = self.first_player
                return GAME_RESULT.WIN
            if lose_cnt == self.size:
                self.winner = self.second_player
                return GAME_RESULT.LOSE
        
        win_cnt = 0
        lose_cnt = 0
        for row in range(self.size):
            col = self.size - row - 1
            if self.position[row, col] == self.first_player:
                win_cnt += 1
            if self.position[row, col] == self.second_player:
                lose_cnt += 1
            if win_cnt == self.size:
                self.winner = self.first_player
                return GAME_RESULT.WIN
            if lose_cnt == self.size:
                self.winner = self.second_player
                return GAME_RESULT.LOSE
    
    def is_finished(self):
        for mark in self.position.values():
            if mark == self.empty:
                return False
        return True

    def get_all_possible_states(self):
        states = []
        for row in range(self.size):
            for col in range(self.size):
                if self.position[row, col] == self.empty:
                    states.append(self.move(row, col))
        return states

    def play(self):
        print('\n Start Tic Tac Toe \n')
        print('  Type "q" to quit the game')
        # self.position = {
        #     (0, 0): 'O', (0, 1): '.', (0, 2): '.',
        #     (1, 0): '.', (1, 1): 'X', (1, 2): '.',
        #     (2, 0): '.', (2, 1): '.', (2, 2): '.',
        # }
        print(self)
        while True:
            try:
                user_input = input('>> ')
                if user_input == 'q': break
                if user_input == '': continue
                
                row = int(re.split(r',|,\s+| ', user_input)[0])
                col = int(re.split(r',|, | ', user_input)[1])

                if self.position[row, col] != self.empty:
                    print('Already put!!')
                    continue

                self = self.move(row, col)
                print(self)
                
                result = self.evaluate_game()
                if result == GAME_RESULT.WIN:
                    print('player "%s" has won the game!\n' % self.winner)
                    break
                elif result == GAME_RESULT.LOSE:
                    print('player "%s" has won the game!\n' % self.winner)
                    break
                else:
                    if self.is_finished():
                        print('Game is drawn!\n')
                        break

                mcts = MCTS(
                    state=self,
                    budgets=1200,
                    exploration_constant=1.414,
                    max_depth=5,
                    visible_graph=True)

                action = mcts.search()
                self = action
                print(self)
                
                result = self.evaluate_game()
                if result == GAME_RESULT.WIN:
                    print('player "%s" has won the game!\n' % self.winner)
                    break
                elif result == GAME_RESULT.LOSE:
                    print('player "%s" has won the game!\n' % self.winner)
                    break
                else:
                    if self.is_finished():
                        print('Game is drawn!\n')
                        break

            except Exception as e:
                print('  Error:', e)
                print('  Invalid input!!')
            

if __name__ == "__main__":
    board = TTTBoard()
    while True:
        board.play()