from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QVBoxLayout

class MainWidget(QWidget):
    def __init__(self, rows, cols):

        super().__init__()

        self.table_widget = QTableWidget(rows, cols)
        self.add_button = QPushButton("Add")
        self.save_button = QPushButton("Save")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.save_button)