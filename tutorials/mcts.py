from platform import node
import random
from sqlite3 import DatabaseError
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass
from networkx.drawing.nx_agraph import graphviz_layout
from scipy import rand

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
    DEPTH = 'depth'
    STATE = 'state'
    REWARD = 'reward'
    VALUE = 'value'
    VISITS = 'visits'

class MCTS:
    def __init__(
        self,
        state,
        budgets=1000, 
        exploration_constant=2,
        max_depth=10
    ):
        self.state = state
        self.budgets = budgets
        self.c = exploration_constant
        self.max_depth = max_depth

        self.tree = self._create_tree(state)

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

    def search(self):
        for _ in range(self.budgets):
            leaf_node = self._select_node()
            check_game_state = self.tree.nodes[leaf_node][NodeData.STATE].evaluate_game()
            
            if check_game_state is None:
                leaf_node = self._expand_leaf_node(leaf_node)
            score = self._rollout(leaf_node)
            self._backpropagate(leaf_node, score)

        return self._get_best_action(root_node=0)

    def _select_node(self):
        is_leaf_node = False
        leaf_node = 0
        while not is_leaf_node:
            children = [child for child in self.tree.neighbors(leaf_node)]
            if not children:
                is_leaf_node = True
            else:
                leaf_node = self._find_best_node_with_uct(children)
        return leaf_node

    def _find_best_node_with_uct(self, children):
        best_node = children[0]
        max_uct = -np.inf
        for child in children:
            w = self.tree.nodes[child][NodeData.REWARD]
            n = self.tree.nodes[child][NodeData.VISITS]
            total_n = self.tree.nodes[0][NodeData.VISITS]

            if n == 0:
                n = 1e-4

            exploitation = w / n
            exploration = np.sqrt(np.log(total_n / n))
            uct = exploitation + self.c * exploration

            if uct > max_uct:
                best_node = child
                max_uct = uct 
        return best_node

    def _expand_leaf_node(self, leaf_node):
        leaf_state = self.tree.nodes[leaf_node][NodeData.STATE]
        possible_states = leaf_state.get_all_possible_states()
        depth = self.tree.nodes[leaf_node][NodeData.DEPTH]

        expanded_node = leaf_node
        if possible_states:
            for possible_state in possible_states:
                new_node = self.tree.number_of_nodes()
                self.tree.add_node(new_node)
                self.tree.update(
                    nodes=[(new_node, {NodeData.DEPTH: depth+1,
                                       NodeData.STATE: possible_state,
                                       NodeData.REWARD: 0,
                                       NodeData.VALUE: -np.inf,
                                       NodeData.VISITS: 0})])
                self.tree.add_edge(leaf_node, new_node)
            expanded_node = random.choice([child for child in self.tree.neighbors(leaf_node)])
        return expanded_node
        
    def _rollout(self, leaf_node):
        state = self.tree.nodes[leaf_node][NodeData.STATE]
        while not state.evaluate_game():
            possible_states = state.get_all_possible_states()
            if possible_states:
                state = random.choice(possible_states) 
            else:
                return 0

        if state.winner == "X":
            return -1
        elif state.winner == "O":
            return 1
        
    def _backpropagate(self, leaf_node, score):
        is_parent_node = True
        while is_parent_node:
            parent_nodes = [node for node in self.tree.predecessors(leaf_node)]
            cur_node = self.tree.nodes[leaf_node]
            cur_node[NodeData.VISITS] += 1
            cur_node[NodeData.REWARD] += score
            cur_node[NodeData.VALUE] = cur_node[NodeData.REWARD] / cur_node[NodeData.VISITS]

            if not parent_nodes:
                is_parent_node = False
            else:
                leaf_node = parent_nodes[0]

    def _get_best_action(self, root_node=0):
        children = [child for child in self.tree.neighbors(root_node)]
        best_idx = np.argmax([self.tree.nodes[child][NodeData.VALUE] for child in children])
        return self.tree.nodes[children[best_idx]][NodeData.STATE]

    def visualize(self):
        visited_nodes = [n for n in self.tree.nodes if self.tree.nodes[n][NodeData.VISITS] > 0]
        visited_tree = self.tree.subgraph(visited_nodes)
        labels = { n: 'depth:{:d}\nvisits:{:d}\nreward:{:.4f}\nvalue:{:.4f}'.format(
                self.tree.nodes[n][NodeData.DEPTH], 
                self.tree.nodes[n][NodeData.VISITS], 
                self.tree.nodes[n][NodeData.REWARD], 
                self.tree.nodes[n][NodeData.VALUE]) for n in visited_tree.nodes}

        plt.figure(figsize=(8, 8))
        pos = graphviz_layout(visited_tree, prog='dot')
        nx.draw(visited_tree, pos, labels=labels, node_shape="s", node_color="none",
                bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))

        plt.title('s')
        plt.axis("equal")
        plt.show()


if __name__ == "__main__":
    mcts = MCTS(None)
    mcts.visualize()