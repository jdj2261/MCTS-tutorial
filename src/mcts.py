import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from dataclasses import dataclass
from networkx.drawing.nx_agraph import graphviz_layout

from utils import ShellColors as sc

import signal
def handler(signum, frame):
    exit()
# Set the signal handler
signal.signal(signal.SIGINT, handler)

@dataclass
class NodeData:
    DEPTH = 'depth'
    STATE = 'state'
    VISITS = 'visits'
    REWARD = 'reward'
    VALUE = 'value'
    PLAYER = 'player'
    
class MCTS:
    def __init__(
        self,
        state,
        budgets=1200, 
        exploration_constant=1.414,
        max_depth=5
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
                        NodeData.VISITS: 0,
                        NodeData.PLAYER: state.first_player})])
        return tree

    def search(self):
        for i in range(self.budgets):
            # print(f"{sc.OKGREEN}Iteration : {i+1} {sc.ENDC}")
            leaf_node = self._select_node()
            print(f"{sc.OKCYAN}Select Node {leaf_node}{sc.ENDC}")
            print(self.tree.nodes[leaf_node][NodeData.STATE])

            state = self.tree.nodes[leaf_node][NodeData.STATE]
            visits = self.tree.nodes[leaf_node][NodeData.VISITS]
            
            is_terminal = state.evaluate_game()
            if not is_terminal and (visits != 0 or leaf_node == 0):
                leaf_node = self._expand_leaf_node(leaf_node)
                print(f"{sc.OKCYAN}Expand Node {leaf_node}{sc.ENDC}")
                print(self.tree.nodes[leaf_node][NodeData.STATE])    
                
            winner = self._rollout(leaf_node)
            self._backpropagate(leaf_node, winner)
            
            if (i+1) % 1200 == 0:
                self.visualize("Backpropagatge")
                print("==="*20)
        return self._get_best_action(root_node=0)

    def _select_node(self):
        cur_node = 0
        while True:
            children = [child for child in self.tree.neighbors(cur_node)]
            if not children:
                break
            cur_node = self._find_best_node_with_uct(children)
        return cur_node

    def _find_best_node_with_uct(self, children):        
        assert len(children) != 0

        ucts = []
        for child in children:
            w = self.tree.nodes[child][NodeData.REWARD]
            n = self.tree.nodes[child][NodeData.VISITS]
            total_n = self.tree.nodes[0][NodeData.VISITS]

            if n == 0:
                uct = float('inf')
            else:
                exploitation = w / n
                exploration = np.sqrt(np.log(total_n) / n)
                uct = exploitation + self.c * exploration
            ucts.append(uct)

        best_node_idx = np.argmax(ucts)
        best_node = children[best_node_idx]
        return best_node

    def _expand_leaf_node(self, leaf_node):
        leaf_state = self.tree.nodes[leaf_node][NodeData.STATE]
        possible_states = leaf_state.get_all_possible_states()
        depth = self.tree.nodes[leaf_node][NodeData.DEPTH]

        expanded_node = leaf_node
        if possible_states and depth < self.max_depth:
            for possible_state in possible_states:
                new_node = self.tree.number_of_nodes()
                self.tree.add_node(new_node)
                self.tree.update(
                    nodes=[(new_node, {NodeData.DEPTH: depth+1,
                                       NodeData.STATE: possible_state,
                                       NodeData.REWARD: 0,
                                       NodeData.VALUE: -np.inf,
                                       NodeData.VISITS: 0,
                                       NodeData.PLAYER: possible_state.next_player})])
                self.tree.add_edge(leaf_node, new_node)
            expanded_node = random.choice([child for child in self.tree.neighbors(leaf_node)])
        return expanded_node
        
    def _rollout(self, leaf_node):
        # print(f"{sc.OKCYAN}Rollout{sc.ENDC}")
        state = self.tree.nodes[leaf_node][NodeData.STATE]
        # print(f"{sc.WARNING}Current Player is {state.cur_player}{sc.ENDC}")
        self.tree.nodes[leaf_node][NodeData.PLAYER] = state.next_player
        while not state.evaluate_game():
            possible_states = state.get_all_possible_states()
            if possible_states:
                state = random.choice(possible_states)
                # print(state)
            else:
                print(f"{sc.OKBLUE}************* Draw !!! *************{sc.ENDC}")
                return

        print(f"{sc.OKBLUE}************* Winner is {state.winner}!!! *************{sc.ENDC}")
        return state.winner

    def _backpropagate(self, leaf_node, winner):
        is_parent_node = True
        while is_parent_node:
            parent_nodes = [node for node in self.tree.predecessors(leaf_node)]
            cur_node = self.tree.nodes[leaf_node]
            
            cur_node[NodeData.VISITS] += 1
            
            if winner:
                if cur_node[NodeData.PLAYER] == winner:
                    cur_node[NodeData.REWARD] += 1
                if cur_node[NodeData.PLAYER] != winner:
                    cur_node[NodeData.REWARD] -= 1

            cur_node[NodeData.VALUE] = cur_node[NodeData.REWARD] / cur_node[NodeData.VISITS]

            if not parent_nodes:
                is_parent_node = False
            else:
                leaf_node = parent_nodes[0]

    def _get_best_action(self, root_node=0):
        children = [child for child in self.tree.neighbors(root_node)]
        best_idx = np.argmax([self.tree.nodes[child][NodeData.VALUE] for child in children])
        print(f"Reward: {[self.tree.nodes[child][NodeData.REWARD] for child in children]}")
        print(f"Value : {[self.tree.nodes[child][NodeData.VALUE] for child in children]}")
        print(f"Visits: {[self.tree.nodes[child][NodeData.VISITS] for child in children]}")
        return self.tree.nodes[children[best_idx]][NodeData.STATE]

    def visualize(self, title):
        # visited_nodes = [n for n in self.tree.nodes if self.tree.nodes[n][NodeData.VISITS] > 0]
        # visited_tree = self.tree.subgraph(visited_nodes)
        labels = { n: 'D:{:d}\nV:{:d}\nR:{:d}\nQ:{:.2f}\nP:{:s}'.format(
                self.tree.nodes[n][NodeData.DEPTH], 
                self.tree.nodes[n][NodeData.VISITS], 
                self.tree.nodes[n][NodeData.REWARD], 
                self.tree.nodes[n][NodeData.VALUE],
                self.tree.nodes[n][NodeData.PLAYER],) for n in self.tree.nodes}

        plt.figure(title, figsize=(12, 8),)
        pos = graphviz_layout(self.tree, prog='dot')
        nx.draw(self.tree, pos, labels=labels, node_shape="s", node_color="none",
                bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.1'))
        plt.show()