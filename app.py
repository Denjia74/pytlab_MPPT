import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QFileDialog
import matlab.engine

class PVModelingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PV Modeling")

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.Gn_input = QLineEdit(self)
        self.Tn_input = QLineEdit(self)
        self.Vocn_input = QLineEdit(self)
        self.Vmp_input = QLineEdit(self)
        self.Imp_input = QLineEdit(self)
        self.Iscn_input = QLineEdit(self)
        self.Ki_input = QLineEdit(self)
        self.Kv_input = QLineEdit(self)
        self.Ns_input = QLineEdit(self)

        self.model_name_input = QLineEdit(self)

        self.form_layout.addRow("Model Name:", self.model_name_input)
        
        self.form_layout.addRow("Nominal Irradiance (Gn):", self.Gn_input)
        self.form_layout.addRow("Nominal Temperature (Tn):", self.Tn_input)
        self.form_layout.addRow("Open Circuit Voltage (Vocn):", self.Vocn_input)
        self.form_layout.addRow("Maximum Power Voltage (Vmp):", self.Vmp_input)
        self.form_layout.addRow("Maximum Power Current (Imp):", self.Imp_input)
        self.form_layout.addRow("Short Circuit Current (Iscn):", self.Iscn_input)
        self.form_layout.addRow("Temperature Coefficient of Current (Ki):", self.Ki_input)
        self.form_layout.addRow("Temperature Coefficient of Voltage (Kv):", self.Kv_input)
        self.form_layout.addRow("Number of Cells in Series (Ns):", self.Ns_input)

        self.run_button = QPushButton("Run Model", self)
        self.run_button.clicked.connect(self.run_model)
        self.layout.addWidget(self.run_button)

        self.save_button = QPushButton("Save Data", self)
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Data", self)
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        self.load_data()

        self.setGeometry(100, 100, 800, 600)

    def save_data(self):
        data = {
            "Model Name": self.model_name_input.text(),
            "Gn": self.Gn_input.text(),
            "Tn": self.Tn_input.text(),
            "Vocn": self.Vocn_input.text(),
            "Vmp": self.Vmp_input.text(),
            "Imp": self.Imp_input.text(),
            "Iscn": self.Iscn_input.text(),
            "Ki": self.Ki_input.text(),
            "Kv": self.Kv_input.text(),
            "Ns": self.Ns_input.text()
        }

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"Data saved to {file_path}")
            except Exception as e:
                print(f"Error saving data: {e}")

    def load_data(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.model_name_input.setText(data.get("Model Name", "")) 
                    self.Gn_input.setText(data.get("Gn", ""))
                    self.Tn_input.setText(data.get("Tn", ""))
                    self.Vocn_input.setText(data.get("Vocn", ""))
                    self.Vmp_input.setText(data.get("Vmp", ""))
                    self.Imp_input.setText(data.get("Imp", ""))
                    self.Iscn_input.setText(data.get("Iscn", ""))
                    self.Ki_input.setText(data.get("Ki", ""))
                    self.Kv_input.setText(data.get("Kv", ""))
                    self.Ns_input.setText(data.get("Ns", ""))
                print(f"Data loaded from {file_path}")
            except Exception as e:
                print(f"Error loading data: {e}")

    def run_model(self):
        Gn = float(self.Gn_input.text())
        Tn = float(self.Tn_input.text())
        Vocn = float(self.Vocn_input.text())
        Vmp = float(self.Vmp_input.text())
        Imp = float(self.Imp_input.text())
        Iscn = float(self.Iscn_input.text())
        Ki = float(self.Ki_input.text())
        Kv = float(self.Kv_input.text())
        Ns = int(self.Ns_input.text())

        eng = matlab.engine.start_matlab()

        s = eng.genpath('.')
        eng.addpath(s, nargout=0)
        eng.method1(Gn, Tn, Vocn, Vmp, Imp, Iscn, Ki, Kv, Ns, nargout=10)
        input("Click Enter to proceed...")
        eng.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PVModelingApp()
    window.show()
    sys.exit(app.exec())
