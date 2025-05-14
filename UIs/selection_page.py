from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget
from PyQt6.QtCore import Qt
from UIs.graph_algo_page import GraphAlgorithmPage
from UIs.lp_input_page import LPInputPage

class SelectionPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        label = QLabel("What type of problem is it?")
        graph_button = QPushButton("Graph Problem")
        lp_button = QPushButton("Linear Programming Problem")

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        layout.addWidget(label)
        layout.addWidget(graph_button)
        layout.addWidget(lp_button)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        graph_button.clicked.connect(self.go_to_graph_page)
        lp_button.clicked.connect(self.go_to_lp_page)

        self.setLayout(layout)

    def go_to_graph_page(self):
        graph_page = GraphAlgorithmPage(self.main_window)
        self.main_window.switch_page(graph_page)

    def go_to_lp_page(self):
        lp_page = LPInputPage(self.main_window)
        self.main_window.switch_page(lp_page)
