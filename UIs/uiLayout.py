from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTextEdit
)

class GraphUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Algrorithms Visualiser")
        self.setMinimumSize(600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setup_inputs()
        self.setup_buttons()
        self.setup_output()

    def setup_inputs(self):
        # The graph type
        graph_type_layout = QHBoxLayout()
        graph_type_label = QLabel("Graph Type: ")
        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems(["Undirected", "Directed"])
        graph_type_layout.addWidget(graph_type_label)
        graph_type_layout.addWidget(self.graph_type_combo)

        # The node input
        node_layout = QHBoxLayout()
        node_label = QLabel("Nodes (use comma between nodes): )")
        self.node_input = QLineEdit()
        node_layout.addWidget(node_label)
        node_layout.addWidget(self.node_input)

        # The edge input
        edge_layout = QHBoxLayout()
        edge_label = QLabel("Edges (A,B,Weight): ")
        self.edge_input = QLineEdit()
        edge_layout.addWidget(edge_label)
        edge_layout.addWidget(self.edge_input)

        # The algorithms
        algo_layout = QHBoxLayout()
        algo_label = QLabel("Algorithms: ")
        self.algo_combo = QComboBox()
        self.algo_combo.addItems([
            "BFS", "DFS", "Dijkstra", "Bellman-Ford", "Shortest-path", "Minmum Spanning Tree", "Toplogicale Sort", "Connected Components", "PageRank"
        ])
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo)

        # Adding al the layouts to the main
        self.layout.addLayout(graph_type_layout)
        self.layout.addLayout(node_layout)
        self.layout.addLayout(edge_layout)
        self.layout.addLayout(algo_layout)

    def setup_buttons(self):
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Algorithm")
        self.clear_button = QPushButton("Clear")
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.clear_button)
        self.layout.addLayout(button_layout)

    def setup_output(self):
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(QLabel("Output: "))
        self.layout.addWidget(self.output_text)