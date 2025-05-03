import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox
from uiLayout import GraphUI
from Algos.Graphs.graphRep import graph_representation
from Visualisations.graphView import GraphView


class MainApp(GraphUI):
    def __init__(self):
        super().__init__()
        self.graph = None

        self.run_button.clicked.connect(self.run_algorithm)
        self.clear_button.clicked.connect(self.clear_all)

    def run_algorithm(self):
        try:
            # --- 1. Read UI inputs ---
            graph_type = self.graph_type_combo.currentText()
            raw_nodes = self.node_input.text()
            nodes = [node.strip() for node in raw_nodes.split(",") if node.strip()]
            raw_edges = self.edge_input.text()
            edges = [edge.strip() for edge in raw_edges.split(";") if edge.strip()]
            algorithm = self.algo_combo.currentText()

            # --- 2. Create the graph representation ---
            self.graph = graph_representation(directed=(graph_type == "Directed"))

            for node in nodes:
                self.graph.add_Node(node)

            for edge_str in edges:
                parts = edge_str.split(",")
                if len(parts) >= 2:
                    u, v = parts[0].strip(), parts[1].strip()
                    weight = int(parts[2].strip()) if len(parts) == 3 else 1
                    self.graph.add_Edge(u, v, weight)

            # --- 3. Run selected algorithm ---
            result = self.execute_algorithm(algorithm)
            self.output_text.setText(result)

            # --- 4. Show graph visualization (IMPORTANT FIX: keep reference!) ---
            self.viewer = GraphView(self.graph.get_graph())  # Keep reference here
            self.viewer.show()

        except Exception as error:
            print("Traceback:", traceback.format_exc())
            QMessageBox.critical(self, "Error", f"{type(error).__name__}: {error}")


        except Exception as error:
            print("Traceback:", traceback.format_exc())
            QMessageBox.critical(self, "Error", f"{type(error).__name__}: {error}")

    def execute_algorithm(self, algo):
        if algo == "BFS":
            return str(self.graph.BFS(source=list(self.graph.graph.nodes)[0]))
        elif algo == "DFS":
            return str(self.graph.DFS(source=list(self.graph.graph.nodes)[0]))
        elif algo == "Dijkstra":
            return str(self.graph.dijkstra(source=list(self.graph.graph.nodes)[0]))
        elif algo == "Bellman-Ford":
            return str(self.graph.bellman_ford(source=list(self.graph.graph.nodes)[0]))
        elif algo == "Shortest-path":
            nodes = list(self.graph.graph.nodes)
            return str(self.graph.shortest_path(source=nodes[0], target=nodes[-1]))
        elif algo == "Minmum Spanning Tree":
            return str(self.graph.minimum_spanning_tree().edges(data=True))
        elif algo == "Toplogicale Sort":
            return str(self.graph.topological_sort())
        elif algo == "Connected Components":
            return str(self.graph.connected_components())
        elif algo == "PageRank":
            return str(self.graph.pagerank())
        else:
            return "Unknown algorithm"

    def clear_all(self):
        self.node_input.clear()
        self.edge_input.clear()
        self.output_text.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
