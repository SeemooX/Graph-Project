from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from UIs.graph_input_page import GaphInputPage

class GraphAlgorithmPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        label = QLabel("Select a Graph Algorithm")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        BFS_button = QPushButton("BFS's Algorithm")
        DFS_button = QPushButton("DFS's Algorithm")
        Dijkstra_button = QPushButton("Dijkstra's Algorithm")
        Prim_button = QPushButton("Prim's Algorithm")
        Bellman_button = QPushButton("Bellman-Ford's Algorithm")
        kruskal_button = QPushButton("Kruskal's Algorithm")
        fulkerson_button = QPushButton("Ford_Fulkerson's Algorithm")
        coloration_button = QPushButton("Coloration's Algorithm")
        union_button = QPushButton("Union's Algorithm")

        back_button = QPushButton("Back")

        layout.addWidget(BFS_button)
        layout.addWidget(DFS_button)
        layout.addWidget(Dijkstra_button)
        layout.addWidget(Prim_button)
        layout.addWidget(Bellman_button)
        layout.addWidget(kruskal_button)
        layout.addWidget(fulkerson_button)
        layout.addWidget(coloration_button)
        layout.addWidget(union_button)
        layout.addWidget(back_button)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # The lambda's role here is to make sure that the "go_to_input_page" doesn't get called until the user click the button
        BFS_button.clicked.connect(lambda: self.go_to_input_page("BFS"))
        DFS_button.clicked.connect(lambda: self.go_to_input_page("DFS"))
        Dijkstra_button.clicked.connect(lambda: self.go_to_input_page("Dijkstra"))
        Prim_button.clicked.connect(lambda: self.go_to_input_page("Prim"))
        Bellman_button.clicked.connect(lambda: self.go_to_input_page("Bellman-Ford"))
        kruskal_button.clicked.connect(lambda: self.go_to_input_page("Kruskal"))
        fulkerson_button.clicked.connect(lambda: self.go_to_input_page("Fulkerson"))
        coloration_button.clicked.connect(lambda: self.go_to_input_page("Coloration"))
        union_button.clicked.connect(lambda: self.go_to_input_page("Union"))
        back_button.clicked.connect(self.go_back)

        self.setLayout(layout)

    def go_to_input_page(self, algorithm_name):
        input_page = GaphInputPage(self.main_window, algorithm_name)
        self.main_window.switch_page(input_page)

    def go_back(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.selection_page)