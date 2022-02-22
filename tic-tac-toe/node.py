from tic_tac_toe import Board, Player

class MCTSNode:
    """
    A node in a MCTS
    """

    def __init__(self, state: Board, depth: int=0):
        self.state = state
        self.depth = depth
        self.Q = 0
        self.N = 0
        self.parent = None
        self.children = []
        self.visited = False
        self.expanded = False

if __name__ == "__main__":
    pass