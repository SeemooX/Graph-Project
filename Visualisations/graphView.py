import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(nodes, edges, show_weights=False, directed=False, title="Graph Visualization", ax=None):
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(nodes)

    # Add edges
    if show_weights:
        for u, v, w in edges:
            G.add_edge(u, v, weight=w)
    else:
        for u, v, *_ in edges:
            G.add_edge(u, v)

    pos = nx.spring_layout(G)

    # If ax is not provided (standalone plot)
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))

    nx.draw(
        G, pos, ax=ax,
        with_labels=True,
        node_color='black',
        edge_color='gray',
        node_size=600,
        font_size=14,
        font_color = 'white',
        arrows=directed,
        connectionstyle='arc3,rad=0.1' if directed else 'arc3'
    )

    # If weights, draw edge labels
    if show_weights:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)

    ax.set_title(title, fontsize=14)
    ax.axis('off')


def plot_side_by_side(original_nodes, original_edges, result_nodes, result_edges, show_weights, directed, graph_name="Result Graph"):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    plot_graph(original_nodes, original_edges, show_weights=show_weights, directed=directed, title="Input Graph", ax=axes[0])
    plot_graph(result_nodes, result_edges, show_weights=show_weights, directed=directed, title=graph_name, ax=axes[1])

    plt.tight_layout()
    plt.show()

def visualize_colored_graph(adj_list, colors):
    G = nx.Graph()
    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    node_colors = [colors[node] for node in G.nodes()]
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color=node_colors, cmap=plt.cm.Set3, node_size=800, font_weight='bold')
    plt.show()