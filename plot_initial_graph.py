import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_graph(adjacency_matrix):
    G = nx.from_numpy_array(np.array(adjacency_matrix))

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=False, node_color='lightblue', edge_color='gray', width=2, node_size=10, font_size=2)
    plt.show()