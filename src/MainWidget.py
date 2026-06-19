from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QGridLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import numpy as np

class MainWidget(QWidget):
    def __init__(self, rows, cols):

        super().__init__()

        self.table_widget = QTableWidget(rows, cols)
        self.add_button = QPushButton("Add")
        self.save_button = QPushButton("Save")
        self.delete_button = QPushButton("Delete")

        self.layout = QGridLayout(self)
        self.layout.setColumnMinimumWidth(1, 600)
        self.layout.setColumnMinimumWidth(2, 500)
        self.layout.addWidget(self.table_widget, 1, 1)

        # Create pie chart figure
        # Checkout https://www.youtube.com/watch?v=AHhcwFPQlfQ for a good video on how to do this.
        fig = Figure(figsize=(500, 500, "px"))
        self.pie_canvas = FigureCanvasQTAgg(fig)
        self.layout.addWidget(self.pie_canvas, 1, 2)
        self.ax = fig.add_subplot()

        self.layout.addWidget(self.add_button, 2, 1)
        self.layout.addWidget(self.save_button, 3, 1)
        self.layout.addWidget(self.delete_button, 4, 1)
    
    def fill_pie_chart(self, tag_cost_dict: dict):

        x = list(tag_cost_dict.values())
        labels = list(tag_cost_dict.keys())

        pie = self.ax.pie(x)

        x_str = ["$" + str(num) for num in x]
        self.ax.pie_label(pie, x_str)
        self.ax.legend(labels)