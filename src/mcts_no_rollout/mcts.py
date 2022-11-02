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
    ACTION = 'action'
    VISITS = 'visits'
    REWARD = 'reward'
    Q = 'q'
    HISTORY = 'history'
    NODE = 'node'
    PLAYER = 'player'

class MCTS(NodeData):

    def __init__(
        self,
        state,
        sampling_method=None,
        n_iters=1200, 
        exploration_constant=1.414,
        max_depth=20,
        gamma=1,
        visible_graph=False
    ):
        self.state = state
        self._sampling_method = sampling_method
        self._n_iters = n_iters
        self.c = exploration_constant
        self._max_depth = max_depth
        self.gamma = gamma
        self.visible = visible_graph
        self.tree = self._create_tree(state)
        
    def _create_tree(self, state):
        tree = nx.DiGraph()
        tree.add_node(0)
        tree.update(
            nodes=[(0, {NodeData.DEPTH: 0,
                        NodeData.STATE: state,
                        NodeData.ACTION: None,
                        NodeData.VISITS: 0,
                        NodeData.REWARD: 0,
                        NodeData.Q: -np.inf,
                        NodeData.NODE: 0,
                        NodeData.PLAYER: state.first_player,
                        NodeData.HISTORY: []})])
        return tree

    def do_planning(self):
        for i in range(self._n_iters):
            print(f"{sc.HEADER}=========== Search iteration : {i+1} ==========={sc.ENDC}")
            self._search(cur_node=0, depth=0)
            # if self.visible:
            #     if (i+1) % self._n_iters == 0:
            #         self.visualize("Backpropagatge")
            #         print("==="*20)
        return self._get_best_action(root_node=0)

    def _search(self, cur_node, depth):
        state = self.tree.nodes[cur_node][NodeData.STATE]
        # print(state)

        # Not use in tic-tac-toe game
        if depth >= self._max_depth:
            return 0

        if self._is_terminal(state, depth):
            reward = self._get_reward(state)
            self.tree.nodes[cur_node][NodeData.VISITS] += 1
            self.tree.nodes[cur_node][NodeData.REWARD] = reward
            self.tree.nodes[cur_node][NodeData.Q] = reward
            self.tree.nodes[cur_node][NodeData.HISTORY].append(reward)
            return reward

        action, next_node = self._select_action(cur_node, state, depth)
        # self.visualize(f"SelectAction Node: {cur_node} Depth: {depth}")
        
        next_state, reward = self._simulate(state, action)
        self.tree.nodes[next_node][NodeData.STATE] = next_state
        # print(f"Simulate Node: {cur_node} Depth: {depth}")
        # self.visualize("Simulate")

        Q_sum = reward + self.gamma * self._search(next_node, depth+1)
        self._update_value(cur_node, Q_sum)

        # print(f"Backpropagation Node: {cur_node} Depth: {depth}")
        # self.visualize("Backpropagation")

        return Q_sum

    @staticmethod
    def _is_terminal(state, depth):
        if state.check_winner() or state.is_finished():
            return True
        return False
    
    def _get_reward(self, state):
        print(f"{sc.OKBLUE}************* Winner is {state.winner}!!! *************{sc.ENDC}")
        if state.winner == state.first_player:
            return -1
        if state.winner == state.second_player:
            return 1
        return 0

    def _select_action(self, cur_node, state, depth):
        children = [child for child in self.tree.neighbors(cur_node)]
        if not children:
            print(f"Cur node {cur_node} is a leaf node, So expand")
            self._expand_node(cur_node, state, depth)
            next_node = random.choice([child for child in self.tree.neighbors(cur_node)])
        else:
            print(f"Cur node has children {children}")
            next_node = self._find_best_node_with_uct(children)
        action = self.tree.nodes[next_node][NodeData.ACTION]
        print(f"Get best action node is {next_node}, and Action is {action}")
        return action, next_node

    def _expand_node(self, cur_node, state, depth):
        possible_actions = state.get_all_possible_actions()
        for possible_action in possible_actions:
            next_node = self.tree.number_of_nodes()
            self.tree.add_node(next_node)        
            self.tree.update(nodes=[(next_node, { NodeData.DEPTH: depth+1,
                                                  NodeData.STATE: None,
                                                  NodeData.ACTION: possible_action,
                                                  NodeData.VISITS: 0,
                                                  NodeData.REWARD: 0,
                                                  NodeData.Q: -np.inf,
                                                  NodeData.NODE: next_node,
                                                  NodeData.PLAYER: state.cur_player,
                                                  NodeData.HISTORY: []})])
            self.tree.add_edge(cur_node, next_node)

    def _find_best_node_with_uct(self, children):
        assert len(children) != 0

        ucts = []
        for child in children:
            w = self.tree.nodes[child][NodeData.Q]
            n = self.tree.nodes[child][NodeData.VISITS]
            total_n = self.tree.nodes[0][NodeData.VISITS]

            if n == 0:
                uct = float('inf')
            else:
                exploitation = w
                exploration = np.sqrt(np.log(total_n) / n)
                uct = exploitation + self.c * exploration
            ucts.append(uct)

        best_node_idx = np.argmax(ucts)
        next_node = children[best_node_idx]
        return next_node

    @staticmethod
    def _simulate(state, action):
        next_state = state.move(*action)
        reward = 0
        return next_state, reward

    def _update_value(self, cur_node, Q_sum):
        self.tree.nodes[cur_node][NodeData.VISITS] += 1
        self.tree.nodes[cur_node][NodeData.HISTORY].append(Q_sum)
        if Q_sum > self.tree.nodes[cur_node][NodeData.Q]:
            self.tree.nodes[cur_node][NodeData.Q] = Q_sum

    def _get_best_action(self, root_node=0):
        children = [child for child in self.tree.neighbors(root_node)]
        best_idx = np.argmax([self.tree.nodes[child][NodeData.Q] for child in children])
        
        print(f"Reward: {[self.tree.nodes[child][NodeData.REWARD] for child in children]}")
        print(f"Q : {[self.tree.nodes[child][NodeData.Q] for child in children]}")
        print(f"Visits: {[self.tree.nodes[child][NodeData.VISITS] for child in children]}")
        
        return self.tree.nodes[children[best_idx]][NodeData.STATE]

    def visualize(self, title):
        # visited_nodes = [n for n in self.tree.nodes if self.tree.nodes[n][NodeData.VISITS] > 0]
        # visited_tree = self.tree.subgraph(visited_nodes)
        labels = { n: 'D:{:d}\nV:{:d}\nR:{:d}\nQ:{:.2f}\nN:{:d}\nP:{:s}'.format(
                self.tree.nodes[n][NodeData.DEPTH],
                self.tree.nodes[n][NodeData.VISITS],
                self.tree.nodes[n][NodeData.REWARD],
                self.tree.nodes[n][NodeData.Q],
                self.tree.nodes[n][NodeData.NODE],
                self.tree.nodes[n][NodeData.PLAYER],) for n in self.tree.nodes}

        plt.figure(title, figsize=(12, 8),)
        pos = graphviz_layout(self.tree, prog='dot')
        nx.draw(self.tree, pos, labels=labels, node_shape="s", node_color="none",
                bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.1'))
        plt.show()

    @property
    def sampling_method(self):
        return self._sampling_method

    @sampling_method.setter
    def sampling_method(self, sampling_method):
        self._sampling_method = sampling_method

    @property
    def n_iters(self):
        return self._n_iters

    @n_iters.setter
    def n_iters(self, n_iters):
        self._n_iters = n_iters

    @property
    def budgets(self):
        return self._budgets

    @budgets.setter
    def budgets(self, budgets):
        self._budgets = budgets