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
        self.rows+=1 # need row for column names

        # Create table
        self.main_widget = MainWidget(self.rows, self.cols)
        self.fill_table()

        self.main_widget.add_button.clicked.connect(self.add_row)
        self.main_widget.save_button.clicked.connect(self.save_to_file)

    def fill_table(self):
        # Set headers.
        for i in range(len(self.cols_names)):
            tmp_item = QTableWidgetItem(self.cols_names[i])
            self.main_widget.table_widget.setItem(0, i, tmp_item)
        
        # Set entries.
        for i in range(self.rows-1):
            for j in range(len(self.cols_names)):
                tmp_item = QTableWidgetItem(str(self.data.iat[i, j]))
                self.main_widget.table_widget.setItem(i+1, j, tmp_item)
    
    @Slot()
    def add_row(self):
        self.main_widget.table_widget.insertRow(self.rows)
        self.rows+=1

    @Slot()
    def save_to_file(self):
        print("Saving")
        tmp_col_names = []
        tmp_data = []
        for row in range(self.rows):
            tmp_row = []
            for col in range(self.cols):
                item = self.main_widget.table_widget.item(row, col)
                if item != None:
                    tmp_row.append(item.text())
                else:
                    tmp_row.append("")
            
            if row == 0:
                tmp_col_names = tmp_row
            else:
                tmp_data.append(tmp_row)

        save_df = pd.DataFrame(data=tmp_data, columns=tmp_col_names)
        save_df.to_csv("experimental_altered.csv", index=False)

    def run(self):
        self.main_widget.show()
        self.app.exec()

app = App()
app.run()