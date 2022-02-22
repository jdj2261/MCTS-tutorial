

class MCTSNode:
    """
    A node in a MCTS
    """

    def __init__(self, state, depth):
        self.state = state
        self.depth = depth
        self.Q = 0
        self.N = 0
        self.parent = None
        self.children = []
        self.visited = False
        self.expanded = False