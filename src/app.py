import sys
import os
import logging

import pandas as pd
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Slot, Signal, QObject

from MainWidget import MainWidget, InputWidget
from model import FinancialModel, FormatError

logger = logging.getLogger(__name__)
# logging.basicConfig(filename = os.path.dirname(os.path.realpath(__file__)) + "/app.log", level=logging.INFO)
logging.basicConfig(level=logging.INFO)

class App(QObject):
    data_changed = Signal(FinancialModel, name="Data Changed")

    def __init__(self, expense_data_dir: str):
        super().__init__()
        if not os.path.exists(expense_data_dir):
            logger.info(f"{expense_data_dir} does not exist. Creating new path.")
            os.mkdir(expense_data_dir)

        expense_file_name = "money_data.csv"
        self.expense_data_path = os.path.join(expense_data_dir, expense_file_name)
        self.col_names = ["Name", "Store", "Price", "Date", "Tag"]

        logger.info(f"Checking for {self.expense_data_path}.")
        if not os.path.isfile(self.expense_data_path):
            logger.info(f"{self.expense_data_path} does not exist. Creating new file.")
            tmp_df = pd.DataFrame(columns=self.col_names)
            tmp_df.to_csv(self.expense_data_path, index=False)
        else:
            logger.info(f"{self.expense_data_path} found.")
        
        self.finance_model = FinancialModel(self.expense_data_path)

        # Create table
        self.app = QApplication(sys.argv)
        self.main_widget = MainWidget(self.col_names)
        self.main_widget.fill_table(self.finance_model.get_all_data())
        self.main_widget.fill_pie_chart(self.finance_model.calculate_tag_costs())

        self.main_widget.inputWidget.forward_data_sig.connect(self.insert_row)
        self.data_changed.connect(self.main_widget.refresh_table)
        self.main_widget.save_to_file_sig.connect(self.save_to_file)
        self.main_widget.request_delete_sig.connect(self.remove_selected_entries)

    @Slot()
    def insert_row(self, entry):
        try:
            logger.info(f"Inserting: {entry} into finance model.")
            self.finance_model.add_entry(entry)
        except FormatError:
            logger.warning("Entry not well formed! Double check price and date are valid!")
            return 

        logger.info("Requesting refresh.")
        self.data_changed.emit(self.finance_model)
    
    @Slot()
    def save_to_file(self):
        logger.info(f"Saving to {self.expense_data_path}")
        self.finance_model.save_to_file(self.expense_data_path)
    
    @Slot()
    def remove_selected_entries(self, entries):
        logger.info("Deleting: ")
        for entry in entries: 
            logger.info(entry)

        self.finance_model.delete_entries(entries) 
        self.data_changed.emit(self.finance_model)

    def run(self):
        logger.info("Running application.")
        self.main_widget.show()
        self.app.exec()