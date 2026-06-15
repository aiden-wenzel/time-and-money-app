from MainWidget import MainWidget
from PySide6.QtWidgets import QApplication, QTableWidgetItem
from PySide6.QtCore import Slot
import pandas as pd
import sys

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.data = pd.read_csv("experimental_original.csv", na_filter=False)
        self.cols_names = ["name", "store", "amount", "date"]
        (self.rows, self.cols) = self.data.shape

        # Create table
        self.main_widget = MainWidget(self.rows, self.cols)
        self.fill_table()

        self.main_widget.add_button.clicked.connect(self.add_row)
        self.main_widget.save_button.clicked.connect(self.save_to_file)
        self.main_widget.delete_button.clicked.connect(self.delete_selected_items)

    def fill_table(self):
        self.main_widget.table_widget.setHorizontalHeaderLabels(self.cols_names)
        
        # Set entries.
        for i in range(self.rows):
            for j in range(len(self.cols_names)):
                tmp_item = QTableWidgetItem(str(self.data.iat[i, j]))
                self.main_widget.table_widget.setItem(i, j, tmp_item)
    
    @Slot()
    def add_row(self):
        self.main_widget.table_widget.insertRow(self.rows)
        self.rows+=1

    @Slot()
    def save_to_file(self):
        print("Saving")
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
        save_df.to_csv("experimental_altered.csv", index=False)

    @Slot()
    def delete_selected_items(self):
        print("Deleting selected rows")
        selected_items = self.main_widget.table_widget.selectedItems()
        for item in selected_items:
            item_row = item.row()
            self.main_widget.table_widget.removeRow(item_row)
            self.rows -= 1

    def run(self):
        self.main_widget.show()
        self.app.exec()

app = App()
app.run()