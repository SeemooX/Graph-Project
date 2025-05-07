import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget
from UIs.selection_page import SelectionPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Algorithm Solver App")
        self.setGeometry(300, 300, 900, 600)

        # The stack of pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # The selection page
        self.selection_page = SelectionPage(self)
        self.stacked_widget.addWidget(self.selection_page)

    def switch_page(self, widget):
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())