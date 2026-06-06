from ExpenseData import ExpenseData
from PySide6 import QtWidgets
import sys

class App:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.ExpenseManager = ExpenseData()
        self.ExpenseManager.load_file("experimental_original.csv")
        (self.rows, self.cols) = self.ExpenseManager.data.shape
        self.rows+=1 # need row for column names

        # Create table
        self.table_widget = QtWidgets.QTableWidget(self.rows, self.cols)
        self.fill_table()

    def fill_table(self):
        # Set headers.
        col_names = self.ExpenseManager.get_cols()
        for i in range(len(col_names)):
            tmp_item = QtWidgets.QTableWidgetItem(col_names[i])
            self.table_widget.setItem(0, i, tmp_item)
        
        # Set entries.
        for i in range(self.rows-1):
            for j in range(self.cols):
                tmp_item = QtWidgets.QTableWidgetItem(str(self.ExpenseManager.data.iat[i, j]))
                self.table_widget.setItem(i+1, j, tmp_item)


    def run(self):
        self.table_widget.show()
        self.app.exec()

app = App()
app.run()