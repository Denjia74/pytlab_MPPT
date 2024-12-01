import sys
import requests
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QDateEdit, QTextEdit
from PySide6.QtCore import QDate

class ModelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Параметри моделювання")
        self.setGeometry(100, 100, 400, 400)
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table_label = QLabel("Оберіть назву таблиці:")
        self.table_combobox = QComboBox()
        self.table_combobox.addItem("pvgis_api")
        self.table_combobox.addItem("station_data")

        self.start_date_label = QLabel("Дата початку:")
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setDate(QDate(2020, 1, 1))
        self.start_date_edit.setCalendarPopup(True)

        self.end_date_label = QLabel("Дата кінця:")
        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setDate(QDate(2020, 1, 5))
        self.end_date_edit.setCalendarPopup(True)

        self.submit_button = QPushButton("Отримати дані")
        self.submit_button.clicked.connect(self.fetch_data)

        self.results_label = QTextEdit(self)
        self.results_label.setReadOnly(True) 
        self.results_label.setPlaceholderText("Результати будуть тут")

        layout.addWidget(self.table_label)
        layout.addWidget(self.table_combobox)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_edit)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_edit)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.results_label)

        self.setLayout(layout)

    def fetch_data(self):
        table = self.table_combobox.currentText()
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")

        url = f"http://127.0.0.1:3000/view?columns=Irradiance-Temperature&table={table}&startDate={start_date}&endDate={end_date}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            formatted_data = json.dumps(data, indent=4)
            self.results_label.setPlainText(formatted_data)

        except requests.exceptions.RequestException as e:
            self.results_label.setText(f"Помилка при отриманні даних: {str(e)}")

    def closeEvent(self, event):
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = ModelApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
