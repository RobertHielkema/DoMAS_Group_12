import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_graph(adjacency_matrix, infected_indices, timestep, pos):
    G = nx.from_numpy_array(np.array(adjacency_matrix))

    plt.figure(figsize=(10, 8))
    colors = ['red' if i in infected_indices else 'lightblue' for i in range(len(G.nodes))]
    pos = nx.spring_layout(G, pos=pos, fixed=pos.keys())
    nx.draw(G, pos, node_color=colors, with_labels=False, edge_color='gray', width=1, node_size=5, font_size=0.5)
    plt.title(f'Graph at Timestep: {timestep}')
    path = f'./graphs/graph_timestep_{timestep}.png'
    plt.savefig(path)
    #plt.show()
    plt.close()
    print(f"Graph saved to {path}")
