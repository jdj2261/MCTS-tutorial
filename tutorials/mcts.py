import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass

# tree node class definition
# Tree operation
# Graph structure package NewtworkX
    # RRT (괜찮음)
    # MCTS (Sub Tree, Minimum spanding Tree, 최단 거리, Tree structure Visualize 지원)
 
# MCTS class definition
# TODO (Expand or UCB)
# recursive 추가

@dataclass
class NodeData:
    DEPTH = 'depth',
    STATE = 'state',
    REWARD = 'reward',
    VALUE = 'value',
    VISITS = 'visits'

class MCTS:
    def __init__(
        self,
        init_state,
        budgets=1500, 
        exploration_constant=2,
        max_depth=10
    ):
        self.budgets = budgets
        self.c = exploration_constant
        self.max_depth = max_depth

        self.tree = self._create_tree(init_state)

        # for debug
        self.o_cnt = 0
        self.x_cnt = 0
    
    def _create_tree(self, state):
        tree = nx.DiGraph()
        tree.add_node(0)
        tree.update(
            nodes=[(0, {NodeData.DEPTH: 0,
                        NodeData.STATE: state,
                        NodeData.REWARD: 0,
                        NodeData.VALUE: -np.inf,
                        NodeData.VISITS: 0})])
        return tree

    def search(self, state):
        for _ in range(self.budgets):
            leaf_node = self._select_node(state)
            
            if self.tree.nodes[leaf_node][NodeData.VISITS] != 0:
                leaf_node = self._expand_node(leaf_node)
            score = self.rollout(leaf_node)
            self.backpropagate(leaf_node, score)

        child_id = np.argmax([child.uct for child in self.root.children])
        return self.root.children[child_id]

    def _select_node(self):
        is_leaf_node = False
        leaf_node = 0

        while not is_leaf_node:
            children = self.tree.neighbors(leaf_node)
            if not children:
                is_leaf_node = True
            leaf_node = self._find_best_node_with_uct(children)
        return leaf_node

    def _find_best_node_with_uct(self, children):
        best_node = children[0]
        max_uct = -np.inf
        for child in children:
            node = self.tree.nodes[child]
            exploitation = node[NodeData.REWARD] / node[NodeData.VISITS]
            exploration = np.sqrt(np.log(self.tree.nodes[0][NodeData.VISITS]) / node[NodeData.VISITS])
            uct = exploitation + self.c * exploration
            
            if uct > max_uct:
                best_node = node
                max_uct = uct 

        return best_node

    def _expand_node(self):
        pass

    def rollout(self, node):
        board = node.state
        while not board.evaluate_game():
            # get_all_possible_states() 중요!!
            # 많은 노력 예상
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

    def visualizae_tree(self):
        pass