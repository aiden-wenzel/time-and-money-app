from MainWidget import MainWidget
from PySide6.QtWidgets import QApplication, QTableWidgetItem
from PySide6.QtCore import Slot
import pandas as pd
import sys
import os

class App:
    def __init__(self, expense_data_path: str):
        self.app = QApplication(sys.argv)

        self.expense_data_path = expense_data_path
        # Create empty table if no file exists.
        expense_data_dir = expense_data_path.split('/')
        expense_data_dir = "/" + "/".join(expense_data_dir[1:-1])
        if not os.path.exists(self.expense_data_path):
            os.mkdir(expense_data_dir)

        if not os.path.isfile(self.expense_data_path):
            tmp_df = pd.DataFrame(columns=["Name", "Store", "Price", "Date", "Tag"])
            tmp_df.to_csv(self.expense_data_path, index=False)
        
        self.data = pd.read_csv(self.expense_data_path, na_filter=False)
        (self.rows, self.cols) = self.data.shape
        self.cols_names = self.data.columns.values

        # Create table
        self.main_widget = MainWidget(self.rows, self.cols)
        self.fill_table()

        self.main_widget.add_button.clicked.connect(self.add_row)
        self.main_widget.save_button.clicked.connect(self.save_to_file)
        self.main_widget.delete_button.clicked.connect(self.delete_selected_items)

        self.tag_costs = self.calculate_tag_costs()
        # Prevent pie chart from being filled if there is no table.
        if (len(self.tag_costs) > 0):
            self.main_widget.fill_pie_chart(self.tag_costs)
         

    def fill_table(self):
        self.main_widget.table_widget.setHorizontalHeaderLabels(self.cols_names)
        
        # Set entries.
        for i in range(self.rows):
            for j in range(len(self.cols_names)):
                tmp_item = QTableWidgetItem(str(self.data.iat[i, j]))
                self.main_widget.table_widget.setItem(i, j, tmp_item)

    def calculate_tag_costs(self):
        tag_index = 0
        amount_index = 0
        for i in range(self.cols):
            if self.main_widget.table_widget.horizontalHeaderItem(i).text() == "Tag":
                tag_index = i
            elif self.main_widget.table_widget.horizontalHeaderItem(i).text() == "Price":
                amount_index = i
        
        all_tags = []
        for row in range(self.rows):
            all_tags.append(self.main_widget.table_widget.item(row, tag_index).text())

        tag_dict = {}
        for tag in all_tags:
            if tag == "":
                continue
            else:
                tag_dict[tag] = 0
        
        for row in range(self.rows):
            tag = self.main_widget.table_widget.item(row, tag_index).text()
            if tag == "":
                continue
            else:
                cost = float(self.main_widget.table_widget.item(row, amount_index).text())
                tag_dict[tag] += cost

        return tag_dict

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

    def run(self):
        self.main_widget.show()
        self.app.exec()