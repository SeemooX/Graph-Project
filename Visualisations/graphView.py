import networkx as nx
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphView(QWidget):
    def __init__(self, graph):
        super().__init__()
        self.setWindowTitle("Graph Visualization")
        self.setMinimumSize(500, 500)

        self.graph = graph
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.canvas = FigureCanvas(Figure())
        layout.addWidget(self.canvas)

        self.plot_graph()

    def plot_graph(self):
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, ax=ax, with_labels=True, node_color='skyblue', edge_color='gray')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels={(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)}, ax=ax)

        self.canvas.draw()
