from MainWidget import MainWidget
from ErrorPopup import ErrorPopup
from model import FinancialModel
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QDialog
from PySide6.QtCore import Slot, QKeyCombination, Qt, Signal, QObject
from PySide6.QtGui import QShortcut, QKeySequence 
from model import FormatError
import pandas as pd
import sys
import os

class EmptyCellError(Exception):
    """Raised when a cell is empty with type NoneType or an empty string."""

class App(QObject):
    data_changed = Signal(FinancialModel, name="Data Changed")

    def __init__(self, expense_data_dir: str):
        super().__init__()
        if not os.path.exists(expense_data_dir):
            os.mkdir(expense_data_dir)

        expense_file_name = "money_data.csv"
        self.expense_data_path = expense_data_dir + expense_file_name
        self.col_names = ["Name", "Store", "Price", "Date", "Tag"]
        if not os.path.isfile(self.expense_data_path):
            tmp_df = pd.DataFrame(columns=self.col_names)
            tmp_df.to_csv(self.expense_data_path, index=False)
        
        self.finance_model = FinancialModel(self.expense_data_path)

        # Create table
        self.app = QApplication(sys.argv)
        self.main_widget = MainWidget(self.col_names)
        self.main_widget.fill_table(self.finance_model.get_data())
        self.main_widget.fill_pie_chart(self.finance_model.calculate_tag_costs())

        self.main_widget.add_entry.connect(self.insert_row)
        self.data_changed.connect(self.main_widget.refresh_table)
        self.main_widget.save_to_file.connect(self.save_to_file)
        # self.main_widget.delete_button.clicked.connect(self.delete_selected_items)

    @Slot()
    def insert_row(self, entry):
        try:
            self.finance_model.add_entry(entry)
        except FormatError:
            print("Entry not well formed! Double check price and date are valid!")
            return 

        self.data_changed.emit(self.finance_model)
    
    @Slot()
    def save_to_file(self):
        self.finance_model.save_to_file(self.expense_data_path)

    def run(self):
        self.main_widget.show()
        self.app.exec()