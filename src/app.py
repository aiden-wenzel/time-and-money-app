from MainWidget import MainWidget
from ErrorPopup import ErrorPopup
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QDialog
from PySide6.QtCore import Slot, QKeyCombination, Qt
from PySide6.QtGui import QShortcut, QKeySequence 
import pandas as pd
import sys
import os

class EmptyCellError(Exception):
    """Raised when a cell is empty with type NoneType or an empty string."""

class App:
    def __init__(self, expense_data_dir: str):
        if not os.path.exists(expense_data_dir):
            os.mkdir(expense_data_dir)

        expense_file_name = "money_data.csv"
        self.expense_data_path = expense_data_dir + expense_file_name
        if not os.path.isfile(self.expense_data_path):
            tmp_df = pd.DataFrame(columns=["Name", "Store", "Price", "Date", "Tag"])
            tmp_df.to_csv(self.expense_data_path, index=False)
        
        self.data = pd.read_csv(self.expense_data_path, na_filter=False)
        (self.rows, self.cols) = self.data.shape
        self.cols_names = self.data.columns.values

        # Create table
        self.app = QApplication(sys.argv)
        self.main_widget = MainWidget(self.rows, self.cols)
        self.fill_table()

        #self.main_widget.add_button.clicked.connect(self.insert_row)
        self.main_widget.save_button.clicked.connect(self.save_to_file)
        self.main_widget.delete_button.clicked.connect(self.delete_selected_items)

        # Find the tag column and price column.
        for i in range(self.cols):
            if self.main_widget.table_widget.horizontalHeaderItem(i).text() == "Tag":
                self.tag_index = i
            elif self.main_widget.table_widget.horizontalHeaderItem(i).text() == "Price":
                self.amount_index = i

        self.calculate_tag_costs()
        # Prevent pie chart from being filled if there is no table.
        if (len(self.tag_dict) > 0):
            self.main_widget.fill_pie_chart(self.tag_dict)

        # Create shortcuts.
        tmp = QKeySequence("Ctrl+Return")
        self.enteritem_shortcut = QShortcut(tmp, self.main_widget, self.save_to_file)
        self.main_widget.add_button.clicked.connect(self.insert_row)
         

    def fill_table(self):
        self.main_widget.table_widget.setHorizontalHeaderLabels(self.cols_names)
        
        # Set entries.
        for i in range(self.rows):
            for j in range(len(self.cols_names)):
                tmp_item = QTableWidgetItem(str(self.data.iat[i, j]))
                self.main_widget.table_widget.setItem(i, j, tmp_item)
    
    def initialize_tag_costs_dict(self):
        self.tag_dict = {}
        for row in range(self.rows):
            tag_item = self.main_widget.table_widget.item(row, self.tag_index)
            self.tag_dict[tag_item.text()] = 0.0

    def calculate_tag_costs(self):
        # Reset the dictionary.
        self.initialize_tag_costs_dict()

        for row in range(self.rows):
            tag_item = self.main_widget.table_widget.item(row, self.tag_index)
            cost_item = self.main_widget.table_widget.item(row, self.amount_index)
            self.tag_dict[tag_item.text()] += float(cost_item.text())
        # Round to 2 decimal places.
        for key in self.tag_dict:
            self.tag_dict[key] = round(self.tag_dict[key], 2)

    @Slot()
    def insert_row(self):
        """
        Insert values from the entry fields into the table.
        """
        self.main_widget.table_widget.insertRow(self.rows)
        self.rows+=1
        for col in range(self.cols):
            tmp_item = self.main_widget.add_entry_table.item(0, col)
            self.main_widget.table_widget.setItem(self.rows-1, col, QTableWidgetItem(tmp_item.text()))

        self.main_widget.add_entry_table.clearContents()

    @Slot()
    def save_to_file(self):
        tmp_data = []
        try:
            for row in range(self.rows):
                tmp_row = []
                for col in range(self.cols):
                    item = self.main_widget.table_widget.item(row, col)
                    if item is None:
                        raise EmptyCellError("Cannot have empty cell!")
                    elif item.text() == "":
                        raise EmptyCellError("Cannot have empty cell!")
                    else:
                        tmp_row.append(item.text())
                
                tmp_data.append(tmp_row)

        except EmptyCellError:
            dlg = ErrorPopup(self.main_widget)
            dlg.exec()
            return

        save_df = pd.DataFrame(data=tmp_data, columns=self.cols_names)
        print(f"Saving to: {self.expense_data_path}")
        save_df.to_csv(self.expense_data_path, index=False)

        # Also refresh the chart!
        self.refresh_pie_chart()
    
    @Slot()
    def delete_selected_items(self):
        selected_items = self.main_widget.table_widget.selectedIndexes()
        row_set = set({})
        for item in selected_items:
            row_set.add(item.row())
        selected_rows = list(reversed(sorted(row_set)))
        for row in selected_rows:
            self.main_widget.table_widget.removeRow(row)
            self.rows -= 1
    
    @Slot()
    def refresh_pie_chart(self):
        self.calculate_tag_costs()
        if (len(self.tag_dict) > 0):
            self.main_widget.fill_pie_chart(self.tag_dict)

    def run(self):
        self.main_widget.show()
        self.app.exec()