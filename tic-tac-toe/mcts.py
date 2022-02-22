from node import MCTSNode

class MCTS:
    def __init__(
        self, 
        max_iters=100,
        max_depth=5, 
        exploration_constant=2,        
    ):
        self.root = MCTSNode()
        self.max_iters = max_iters
        self.max_depth = max_depth
        self.c = exploration_constant

    def selection(self):
        """
        Select leaf node which have maximum uct value
        """
        pass

    def _compute_ucb1(self):
        pass

    def expansion(self):
        """
        
        """
        pass

    def _is_terminal(self):
        pass

    def simulation(self):
        """
        """
        pass

    def back_propagation(self):
        """
        """
        pass