import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_graph(adjacency_matrix, infected_indices, timestep):
    G = nx.from_numpy_array(np.array(adjacency_matrix))

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)  # positions for all nodes
    colors = ['red' if i in infected_indices else 'lightblue' for i in range(len(G.nodes))]
    nx.draw(G, pos, node_color=colors, with_labels=False, edge_color='gray', width=2, node_size=10, font_size=2)
    plt.title(f'Graph at Timestep: {timestep}')
    plt.show()