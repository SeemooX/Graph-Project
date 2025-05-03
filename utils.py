import networkx as nx
import matplotlib.pyplot as plt

# 1. Create a weighted undirected graph
G = nx.Graph()

# 2. Add nodes and weighted edges
G.add_edge("A", "B", weight=4)
G.add_edge("A", "C", weight=2)
G.add_edge("B", "C", weight=1)
G.add_edge("B", "D", weight=5)
G.add_edge("C", "D", weight=8)
G.add_edge("C", "E", weight=10)
G.add_edge("D", "E", weight=2)

# 3. Get the Minimum Spanning Tree
mst = nx.minimum_spanning_tree(G)

# 4. Draw the original graph
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1200, font_size=14)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels)
plt.title("Original Graph")

# 5. Draw the MST
plt.subplot(1, 2, 2)
nx.draw(mst, pos, with_labels=True, node_color='lightgreen', edge_color='green', node_size=1200, font_size=14)
mst_edge_labels = nx.get_edge_attributes(mst, 'weight')
nx.draw_networkx_edge_labels(mst, pos, mst_edge_labels)

plt.tight_layout()
plt.show()


