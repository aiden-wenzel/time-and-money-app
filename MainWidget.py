from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class MainWidget(QWidget):
    def __init__(self, rows, cols):

        super().__init__()

        self.table_widget = QTableWidget(rows, cols)
        self.add_button = QPushButton("Add")
        self.save_button = QPushButton("Save")
        self.delete_button = QPushButton("Delete")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.delete_button)

        # Create pie chart figure
        # Checkout https://www.youtube.com/watch?v=AHhcwFPQlfQ for a good video on how to do this.
        fig = Figure()
        self.pie_canvas = FigureCanvasQTAgg(fig)
        self.layout.addWidget(self.pie_canvas)
        ax = fig.add_subplot()
        ax.plot(range(10), range(10))
