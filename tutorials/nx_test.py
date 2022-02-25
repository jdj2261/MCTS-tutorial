import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

tree = nx.DiGraph()

tree.add_node(0)
tree.update(nodes=[(0, 
                    {'depth' : 0,
                     'state' : 0,
                     'reward': 0,
                     'value' : 0,
                     'visits': 0,
                    })])

tree.add_node(1)
tree.update(nodes=[(1, 
                    {'depth' : 1,
                     'state' : 1,
                     'reward': 1,
                     'value' : 1,
                     'visits': 1,
                    })])

tree.add_edge(0, 1)

tree.add_node(2)
tree.update(nodes=[(2, 
                    {'depth' : 2,
                     'state' : 2,
                     'reward': 2,
                     'value' : 2,
                     'visits': 2,
                    })])

tree.add_edge(0, 2)

tree.add_node(3)
tree.update(nodes=[(3, 
                    {'depth' : 3,
                     'state' : 3,
                     'reward': 3,
                     'value' : 3,
                     'visits': 3,
                    })])

tree.add_edge(0, 3)

tree.add_node(4)
tree.update(nodes=[(4, 
                    {'depth' : 4,
                     'state' : 4,
                     'reward': 4,
                     'value' : 4,
                     'visits': 4,
                    })])
tree.add_edge(1, 4)


tree.add_node(5)
tree.update(nodes=[(5, 
                    {'depth' : 5,
                     'state' : 5,
                     'reward': 5,
                     'value' : 5,
                     'visits': 5,
                    })])

tree.add_edge(1, 5)

tree.add_node(6)
tree.update(nodes=[(6, 
                    {'depth' : 6,
                     'state' : 6,
                     'reward': 6,
                     'value' : 6,
                     'visits': 6,
                    })])
tree.add_edge(3, 6)


tree.add_node(7)
tree.update(nodes=[(7, 
                    {'depth' : 7,
                     'state' : 7,
                     'reward': 7,
                     'value' : 7,
                     'visits': 7,
                    })])
tree.add_edge(3, 7)


tree.add_node(8)
tree.update(nodes=[(8, 
                    {'depth' : 8,
                     'state' : 8,
                     'reward': 8,
                     'value' : 8,
                     'visits': 8,
                    })])
tree.add_edge(3, 8)


tree.add_node(9)
tree.update(nodes=[(9, 
                    {'depth' : 9,
                     'state' : 9,
                     'reward': 9,
                     'value' : 9,
                     'visits': 9,
                    })])
tree.add_edge(4, 9)


data = nx.tree_data(tree, root=0)
print(len(data))
print(data['children'])
print(len(data['children']))
print([node for node in tree.neighbors(0)])
# for i in range(tree.number_of_nodes()):
#     if not nx.tree_data(tree, root=i)['children']:
#         print(i)


# print(data['children'])

# # labels = nx.get_node_attributes(tree, "label", "layer")
labels = { n: 'depth:{:d}\nvisit:{:d}\nreward:{:.4f}\nvalue:{:.4f}'.format(tree.nodes[n]['depth'], tree.nodes[n]['visits'], tree.nodes[n]['reward'], tree.nodes[n]['value']) for n in tree.nodes}
options = {
    "node_size": 600,
    "alpha": 0.5,
    "node_color": "blue",
    "labels": labels,
    "font_size": 10,
}
plt.figure(figsize=(8, 8))
pos = graphviz_layout(tree, prog='dot')
nx.draw_networkx(tree, pos, **options)
plt.title('s')
plt.axis("equal")
plt.show()
