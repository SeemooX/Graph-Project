from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QCheckBox
from PyQt6.QtCore import Qt
from Algos.Graphs.graphRep import GraphRep
from Visualisations.graphView import plot_side_by_side, visualize_colored_graph

class GaphInputPage(QWidget):
    def __init__(self, main_window, algorithm_name):
        super().__init__()
        self.main_window = main_window
        self.algorithm_name = algorithm_name

        self.setWindowTitle(f"{algorithm_name} - Input Page")

        layout = QVBoxLayout()

        title_label = QLabel(f"Input for {algorithm_name}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Node input
        node_layout = QHBoxLayout()
        node_label = QLabel("Nodes (comma seprated):")
        self.node_input = QLineEdit()
        node_layout.addWidget(node_label)
        node_layout.addWidget(self.node_input)
        layout.addLayout(node_layout)

        # Edge input
        edge_layout = QHBoxLayout()
        self.edge_input = QTextEdit()
        self.edge_input.setPlaceholderText("Enter edges (one per line)\nExample:\nA B\nB C")
        edge_layout.addWidget(self.edge_input)
        layout.addLayout(edge_layout)

        # Info label
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        # Run and Back Buttons
        button_layout = QHBoxLayout()
        run_button = QPushButton("Run Algorithm")
        back_button = QPushButton("Back")
        button_layout.addWidget(run_button)
        button_layout.addWidget(back_button)
        layout.addLayout(button_layout)

        # Is the graph directed or Not
        self.directed_checkbox = QCheckBox("Directed graph?")
        layout.addWidget(self.directed_checkbox)

        # Result output
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.setLayout(layout)

        # Connect buttons
        run_button.clicked.connect(self.run_algorithm)
        back_button.clicked.connect(self.go_back)

         # Adjust placeholder based on algorithm
        if self.algorithm_name in ["DFS", "BFS", "Coloration"]:
            self.edge_input.setPlaceholderText("Enter edges (one per line)\nExample:\nA B\nB C\n(No weights needed)")
        else:
            self.edge_input.setPlaceholderText("Enter edges (one per line)\nExample:\nA B 5\nB C 3")

    def run_algorithm(self):
        nodes_text = self.node_input.text()
        nodes = [n.strip() for n in nodes_text.split(",") if n.strip() != ""]

        edges_text = self.edge_input.toPlainText()
        edges = []
        for line in edges_text.splitlines():
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            node1, node2 = parts[0], parts[1]
            if self.algorithm_name in ["DFS", "BFS", "Coloration"]:
                edges.append((node1, node2))
            else:
                if len(parts) < 3:
                    continue  # Skip invalid
                weight = float(parts[2])
                edges.append((node1, node2, weight))
        
        directed = self.directed_checkbox.isChecked()

        graph = GraphRep(directed=directed)

        for node in nodes:
            graph.add_node(node)

        for edge in edges:
            if self.algorithm_name in ["DFS", "BFS", "Coloration"]:
                node1, node2 = edge
                graph.add_edge(node1, node2)
            else:
                node1, node2, weight = edge
                graph.add_edge(node1, node2, weight)

        result_text = ""

        if self.algorithm_name == "DFS":
            start_node = nodes[0] if nodes else None
            nodes_in_tree, edges_in_tree = graph.DFS(start_node)
            result_text += f"Nodes in DFS Tree: {nodes_in_tree}\nEdges in DFS Tree: {edges_in_tree}"
        elif self.algorithm_name == "BFS":
            start_node = nodes[0] if nodes else None
            nodes_in_tree, edges_in_tree = graph.BFS(start_node)
            result_text += f"Nodes in DFS Tree: {nodes_in_tree}\nEdges in DFS Tree: {edges_in_tree}"
        elif self.algorithm_name == "Dijkstra":
            start_node = nodes[0] if nodes else None
            nodes_in_tree, edges_in_tree, parent, distance = graph.DFS(start_node)
            result_text += f"Nodes: {nodes_in_tree}\nEdges: {edges_in_tree}\nDistances: {distance}"
        elif self.algorithm_name == "Prim":
            start_node = nodes[0] if nodes else None
            nodes_in_tree, edges_in_tree, min_tree = graph.Prim(start_node)
            result_text += f"Nodes: {nodes_in_tree}\nEdges: {edges_in_tree}"
        elif self.algorithm_name == "Bellman-Ford":
            start_node = nodes[0] if nodes else None
            nodes_in_tree, edges_in_tree, parent, distance = graph.Bellman_Ford(start_node)
            if nodes_in_tree is None:
                result_text += "Absorbent cycle detected. No valid paths."
            else:
                result_text += f"Nodes: {nodes_in_tree}\nEdges: {edges_in_tree}\nDistances: {distance}"
        elif self.algorithm_name == "Kruskal":
            nodes_in_tree, edges_in_tree, total_weight = graph.kruskal()
            result_text += f"Nodes: {nodes_in_tree}\nEdges: {edges_in_tree}\nTotal weight: {total_weight}"
        elif self.algorithm_name == "Coloration":
            colors = graph.graph_coloring()
            result_text += f"colors are: {colors}"
        elif self.algorithm_name == "Fulkerson":
            start_node = nodes[0] if nodes else None
            sink_node = nodes[len(graph.nodes) - 1] if nodes else None
            max_flow, nodes_in_tree, edges_in_tree = graph.ford_fulkerson(start_node, sink_node)
            result_text += f"maxflow is: {max_flow}\nEdges: {edges_in_tree}"
        else:
            result_text = "Unknown Algorithm"

        self.result_output.setPlainText(result_text)

        if self.algorithm_name == "Coloration":
            visualize_colored_graph(graph.adj_list, colors)
        else:
            plot_side_by_side(
            original_nodes=nodes,
            original_edges=edges,
            result_nodes=nodes_in_tree,
            result_edges=edges_in_tree,
            show_weights=(self.algorithm_name not in ["DFS", "BFS"]),
            directed=directed,
            graph_name=self.algorithm_name
            )

    def go_back(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.selection_page)
