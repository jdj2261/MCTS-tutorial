import enum

ROWS, COLUMMS = 3, 3
CELLS = ROWS * COLUMMS
SCORE = 3

class Player(enum.Enum):
    EMPTY=0
    X=1
    O=2

class Board:
    def __init__(self, first_player = Player.X):
        self._current_player = first_player
        self._board = self._create_board()
        self._move_cnt = 0
        self._winner = None
        self._scores = {'rows': [0] * ROWS, 
                        'cols': [0] * COLUMMS,
                        'diags':[0] * 2}
        self._score_maps = { Player.X: 1, Player.O: -1}

    def _create_board(self):
        return [[Player.EMPTY for _ in range(COLUMMS)] for _ in range(ROWS)]

    def __str__(self):
        display_player = {Player.EMPTY: " ",
                          Player.X: "X",
                          Player.O: "O"}
                            
        display_str = "==" * ROWS + "\n"
        for row in self._board:
            row_display = [display_player[player] for player in row]
            display_str += '|'.join(row_display)
            display_str += "\n"
        display_str += "==" * ROWS
        display_str += f"\nWinner is {display_player.get(self._winner, None)}\n"
        return display_str

    def play(self, row: int, col: int) -> bool:
        if self.is_finished():
            return False

        assert 0 <= row < len(self._board)
        assert 0 <= col < len(self._board[0])

        if self._board[row][col] in self._score_maps.keys():
            return False

        self._board[row][col] = self._current_player
        self._update_score(row, col)
        self._check_winner()
        self._update_player()
        self._move_cnt += 1

        return True

    def _update_score(self, row, col):
        
        self._scores['rows'][row] += self._score_maps[self._current_player]
        self._scores['cols'][col] += self._score_maps[self._current_player]
        
        if row == col:
            self._scores['diags'][0] += self._score_maps[self._current_player]
        if row == len(self._board) - col - 1:
            self._scores['diags'][1] += self._score_maps[self._current_player]

    def _update_player(self):
        if self._current_player == Player.X:
            self._current_player = Player.O
        else:
            self._current_player = Player.X

    def _check_winner(self):
        if self._winner:
            return self._winner

        for scores in self._scores.values():
            for score in scores:
                if score == SCORE:
                    self._winner = Player.X
                if score == -SCORE:
                    self._winner = Player.O

    def is_finished(self):
        return self._move_cnt == CELLS
            
    def display_available_positions(self):
        pass


if __name__ == "__main__":
    board = Board()
    print(board)

    board.play(0, 0)
    print(board)

    board.play(0, 2)
    print(board)

    board.play(1, 1)
    print(board)

    board.play(1, 2)
    print(board)

    board.play(2, 2)
    print(board)

    board.play(2, 0)
    print(board)