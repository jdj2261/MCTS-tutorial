import random
import numpy as np

# tree node class definition
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.visits = 0
        self.reward = 0
        self.value = 0
        self.parent = parent
        self.children = []

# MCTS class definition
class MCTS:
    def __init__(self, n_iters=1500, exploration_constant=2):
        self.n_iters = n_iters
        self.c = exploration_constant

        # for debug
        self.o_cnt = 0
        self.x_cnt = 0
    
    def search(self, state):
        self.root = TreeNode(state, parent=None)
        for _ in range(self.n_iters):
            leaf_node = self.select(self.root)

            print("------------------- Debug -------------------")
            print(leaf_node.state)
            print(leaf_node.visits)
            print(leaf_node.reward)
            print(leaf_node.value)
            print("---------------------------------------------")
            print()

            reward = self.rollout(leaf_node)
            self.backpropagate(leaf_node, reward)

        child_id = np.argmax([child.value for child in self.root.children])
        return self.root.children[child_id]

    # TODO (expand or UCB)
    def select(self, node):
        if node.visits == 0:
            posslbie_states = node.state.get_all_possible_states()
            for state in posslbie_states:
                new_node = TreeNode(state, node)
                node.children.append(new_node)

        for child in node.children:
            if child.visits == 0:
                return child

        return self.find_best_leaf_node(node)

    def find_best_leaf_node(self, node):
        ucts = []
        for child_node in node.children:
            exploit = child_node.reward / child_node.visits
            # print(node.visits, child_node.visits)
            explore = np.sqrt(np.log(node.visits) / child_node.visits)
            value = exploit + self.c * explore
            child_node.value = value
            ucts.append(value)
        best_idx = np.argmax(ucts)
        return node.children[best_idx]

    def rollout(self, node):
        board = node.state
        while not board.evaluate_game():
            possible_states = board.get_all_possible_states()
            if possible_states:
                board = random.choice(possible_states)
            else:
                return 0

        # Debug
        if board.winner == "X":
            self.x_cnt += 1
        elif board.winner == "O":
            self.o_cnt += 1
        print(self.x_cnt, self.o_cnt)

        if board.winner == "X":
            return -1
        elif board.winner == "O":
            return 1
        
    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent