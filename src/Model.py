import pandas as pd

class FinancialModel:
    def __init__(self, file_path):
        self.col_names = ["Name", "Store", "Price", "Date", "Tag"]
        self.data = pd.read_csv(file_path)
    
    def get_num_rows(self):
        return self.data.shape[0]
    
    def get_num_cols(self):
        return self.data.shape[1]
    
    def add_entry(self):
        pass

    def delete_rows(self):
        pass

    def calculate_tag_costs(self):
        pass

    def save_to_file(self, file_path):
        pass