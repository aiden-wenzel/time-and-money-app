from MainWidget import MainWidget
from PySide6.QtWidgets import QApplication, QTableWidgetItem
from PySide6.QtCore import Slot
import pandas as pd
import sys
import os

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

        self.main_widget.add_button.clicked.connect(self.add_row)
        self.main_widget.save_button.clicked.connect(self.save_to_file)
        self.main_widget.delete_button.clicked.connect(self.delete_selected_items)

        # Find the tag column and price column.
        for i in range(self.cols):
            if self.main_widget.table_widget.horizontalHeaderItem(i).text() == "Tag":
                self.tag_index = i
            elif self.main_widget.table_widget.horizontalHeaderItem(i).text() == "Price":
                self.amount_index = i

        self.initialize_tag_costs_dict()
        self.calculate_tag_costs()
        # Prevent pie chart from being filled if there is no table.
        if (len(self.tag_dict) > 0):
            self.main_widget.fill_pie_chart(self.tag_dict)
         

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
            if type(tag_item) == None or tag_item.text() == "":
                self.tag_dict["None"] = 0.0
            else:
                self.tag_dict[tag_item.text()] = 0.0

    def calculate_tag_costs(self):
        # Reset the dictionary.
        for key in self.tag_dict:
            self.tag_dict[key] = 0.0

        for row in range(self.rows):
            tag_item = self.main_widget.table_widget.item(row, self.tag_index)
            cost_item = self.main_widget.table_widget.item(row, self.amount_index)
            if type(cost_item) == None:
                continue
            elif cost_item.text() == "":
                continue
            elif type(tag_item) == None or tag_item.text() == "":
                self.tag_dict["None"] += float(cost_item.text())
            else:
                self.tag_dict[tag_item.text()] += float(cost_item.text())
        # Round to 2 decimal places.
        for key in self.tag_dict:
            self.tag_dict[key] = round(self.tag_dict[key], 2)

    @Slot()
    def add_row(self):
        self.main_widget.table_widget.insertRow(self.rows)
        self.rows+=1

    @Slot()
    def save_to_file(self):
        tmp_data = []
        for row in range(self.rows):
            tmp_row = []
            for col in range(self.cols):
                item = self.main_widget.table_widget.item(row, col)
                if item != None:
                    tmp_row.append(item.text())
                else:
                    tmp_row.append("")
            
            tmp_data.append(tmp_row)

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