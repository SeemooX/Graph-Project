from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QFileDialog, QHBoxLayout, QPlainTextEdit
from PyQt6.QtCore import Qt
import re
from Algos.LP.LPP import simplex

class LPInputPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Linear Programming - Input Page")

        layout = QVBoxLayout()

        title_label = QLabel("Linear Programming Input")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Import button + Info label
        button_layout = QHBoxLayout()
        import_button = QPushButton("Import LPP File")
        self.info_label = QLabel("No file imported")
        button_layout.addWidget(import_button)
        button_layout.addWidget(self.info_label)
        layout.addLayout(button_layout)

        # Display parsed file content
        self.parsed_display = QTextEdit()
        self.parsed_display.setReadOnly(True)
        layout.addWidget(self.parsed_display)

        # Run + Back buttons
        button_layout2 = QHBoxLayout()
        run_button = QPushButton("Run LP Solver")
        back_button = QPushButton("Back")
        button_layout2.addWidget(run_button)
        button_layout2.addWidget(back_button)
        layout.addLayout(button_layout2)

        self.result_output = QPlainTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.setLayout(layout)

        # Connect buttons
        import_button.clicked.connect(self.import_file)
        back_button.clicked.connect(self.go_back)
        run_button.clicked.connect(self.run_lp_solver)

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import LPP File", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()

                self.info_label.setText(f"Imported: {file_path.split('/')[-1]}")
                self.parsed_display.setPlainText(content)

                # Parse and nicely show structured info
                self.lp_data = self.parse_lp_file(content)
                pretty_text = self.pretty_print_lp_data(self.lp_data)
                self.parsed_display.setPlainText(pretty_text)

            except Exception as e:
                self.info_label.setText("Failed to load file")
                self.parsed_display.setPlainText(str(e))

    def pretty_print_lp_data(self, data):
        text = ""
        text += f"Objective: {data['objective']}\n"
        text += f"Coefficients: {data['coefficients']}\n"
        text += "Constraints:\n"
        for coeffs, sign, rhs in data['constraints']:
            text += f"  {coeffs} {sign} {rhs}\n"
            text += "Bounds:\n"
        for var, sign, value in data['bounds']:
            text += f"  {var} {sign} {value}\n"
        return text

    def parse_lp_file(self, content):
        lp_data = {
            'objective': None,
            'coefficients': [],
            'constraints': [],
            'bounds': []
        }

        lines = content.strip().splitlines()
        section = None

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):  # Skip empty or commented lines
                continue

            # Detect section headers
            if line.lower().startswith("objective:"):
                section = 'objective'
                lp_data['objective'] = line.split(":")[1].strip().lower()
            elif line.lower().startswith("coefficients:"):
                section = 'coefficients'
                coeffs = line.split(":")[1].strip().split()
                lp_data['coefficients'] = list(map(float, coeffs))
            elif line.lower() == "constraints:":
                section = 'constraints'
            elif line.lower() == "bounds:":
                section = 'bounds'
            else:
                if section == 'constraints':
                    # Example: 2 1 <= 5
                    tokens = line.split()
                    coeffs = list(map(float, tokens[:-2]))
                    sign = tokens[-2]
                    rhs = float(tokens[-1])
                    lp_data['constraints'].append((coeffs, sign, rhs))
                elif section == 'bounds':
                    # Example: x1 >= 0
                    match = re.match(r'(x\d+)\s*(<=|>=)\s*([\d\.\-]+)', line)
                    if match:
                        var, sign, value = match.groups()
                        lp_data['bounds'].append((var, sign, float(value)))

        return lp_data

    def run_lp_solver(self):
         # Make sure lp_data is available
        if not self.lp_data:
            self.result_output.setPlainText("Please import a valid LP file first.")
            return

        lp_data = self.lp_data

        objective = lp_data['objective']
        c = lp_data['coefficients']
        constraints = lp_data['constraints']

        # Parse constraints into A and b
        A = []
        b = []
        for coeffs, sign, rhs in constraints:
            if sign != "<=":
                self.result_output.setPlainText(f"Only <= constraints are supported currently. Found: {sign}")
                return
            A.append(coeffs)
            b.append(rhs)

        if objective != "max":
            self.result_output.setPlainText(f"Only maximization problems are supported currently. Found: {objective}")
            return

        # Run simplex
        optimal_value, solution = simplex(c, A, b)

        # Display result
        if optimal_value is None:
            self.result_output.setPlainText("The problem is unbounded or infeasible.")
        else:
            result_text = f"Optimal value: {optimal_value}\nSolution:\n"
            for idx, val in enumerate(solution, 1):
                result_text += f"x{idx} = {val}\n"
                self.result_output.setPlainText(result_text)
            
    def go_back(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.selection_page)