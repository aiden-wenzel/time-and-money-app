import logging

import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QGridLayout, 
    QLineEdit, QLabel
)
from PySide6.QtCore import Slot, Signal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from model import FinancialModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MainWidget(QWidget):

    add_entry = Signal(list, name="Adding Entry")
    save_to_file = Signal(name="Save to File")
    request_delete_sig = Signal(list, name="Delete Rows")

    def __init__(self, col_names: list[str]):

        super().__init__()
        self.layout = QGridLayout(self)
        self.col_names = col_names

        # Create table.
        self.table_widget = QTableWidget(0, len(self.col_names))
        self.table_widget.setHorizontalHeaderLabels(self.col_names)
        self.layout.setColumnMinimumWidth(1, 600)
        self.layout.setColumnMinimumWidth(2, 500)
        self.layout.addWidget(self.table_widget, 1, 1)

        # Create an input entry widget.
        self.inputWidget = InputWidget(self.col_names)

        # Create pie chart figure.
        # Checkout https://www.youtube.com/watch?v=AHhcwFPQlfQ for a good video on how to do this.
        fig = Figure(figsize=(500, 500, "px"))
        self.pie_canvas = FigureCanvasQTAgg(fig)
        self.layout.addWidget(self.pie_canvas, 1, 2)
        self.ax = fig.add_subplot()

        # Create buttons.
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.inputWidget.show)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_to_file.emit)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.request_delete)

        self.layout.addWidget(self.add_button, 2, 1)
        self.layout.addWidget(self.save_button, 3, 1)
        self.layout.addWidget(self.delete_button, 4, 1)

        self.add_entry_table = QTableWidget(1, len(self.col_names))
        self.layout.addWidget(self.add_entry_table, 2, 2, 3, 1)

    
    def fill_pie_chart(self, tag_cost_dict: dict):

        self.ax.clear()
        x = list(tag_cost_dict.values())
        labels = list(tag_cost_dict.keys())

        pie = self.ax.pie(x)

        x_str = ["$" + str(num) for num in x]
        self.ax.pie_label(pie, x_str)
        self.ax.legend(labels)
        self.pie_canvas.draw()

    def fill_table(self, entries: pd.DataFrame):
        
        num_rows = entries.shape[0]
        num_cols = entries.shape[1]

        # Set entries.
        for i in range(num_rows):
            self.table_widget.insertRow(i)
            for j in range(num_cols):
                tmp_item = QTableWidgetItem(str(entries.iat[i, j]))
                self.table_widget.setItem(i, j, tmp_item)
    
    @Slot()
    def refresh_table(self, model: FinancialModel):
        num_rows = self.table_widget.rowCount()
        for i in range(num_rows):
            self.table_widget.removeRow(0)

        self.fill_table(model.get_all_data())
        self.fill_pie_chart(model.calculate_tag_costs())

    @Slot()
    def request_save(self):
        self.save_to_file.emit()

    @Slot()
    def request_delete(self):

        selected_items = self.table_widget.selectedIndexes()
        row_set = set({})
        for item in selected_items:
            row_set.add(item.row())

        rows = []
        for row in row_set:
            rows.append(self.get_row(row))
        
        self.request_delete_sig.emit(rows)

    def get_row(self, row: int) -> list[str]:
        num_cols = self.table_widget.columnCount()
        tmp_list = []
        for col in range(num_cols):
            tmp_item = self.table_widget.item(row, col)
            tmp_list.append(tmp_item.text())
        
        return tmp_list

class InputWidget(QWidget):

    forward_data_sig = Signal(list, name="Forward data")
    def __init__(self, column_names: list[str]):
        super().__init__()
        self.layout = QGridLayout(self)
        self.column_names = column_names

        self.input_lines = {}
        self.input_col = 1
        self.label_col = 0
        for i in range(len(column_names)):
            self.input_lines[column_names[i]] = QLineEdit(parent=self)
            self.layout.addWidget(self.input_lines[column_names[i]], i, self.input_col)

            description_tmp = QLabel(f"{column_names[i]}: ")
            self.layout.addWidget(description_tmp, i, self.label_col)

        button_width = 50
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMaximumWidth(button_width)
        self.layout.addWidget(self.cancel_button, len(column_names), 0)

        self.cancel_button.clicked.connect(self.close)

        self.done_button = QPushButton("Ok")
        self.done_button.setMaximumWidth(button_width)
        self.layout.addWidget(self.done_button, len(column_names), 1)
        self.done_button.clicked.connect(self.forward_data)
    
    @Slot()
    def forward_data(self):
        out = []
        for name in self.column_names:
            tmp_text = self.input_lines[name].text()
            if tmp_text == "":
                logger.warning(f"Cannot have empty fields! Try again.")
                return
            else:
                out.append(tmp_text)

        logger.info(f"Forwarding entry: {out} to main application.")
        self.forward_data_sig.emit(out)        
