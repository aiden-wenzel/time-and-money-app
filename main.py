import pandas as pd

class ExpenseData:
    def __init__(self):
        self.cols = ["name", "store", "amount", "date"]

    def load_file(self, file_path:str):
        self.data = pd.read_csv(file_path)
        self.data["date"] = pd.to_datetime(self.data["date"])

    def save_file(self, file_path:str):
        self.data.to_csv(file_path, index=False)

    def add_entry(self, name, store, amount, date):
        tmp_entry = pd.DataFrame([[name, store, amount, pd.Timestamp(date)]], columns=self.cols)
        self.data = pd.concat([self.data, tmp_entry], ignore_index=True)
    
    def delete_entry(self):
        self.data.drop([0], inplace=True)
    



TimeManager = ExpenseData()
TimeManager.load_file("experimental_original.csv")
TimeManager.add_entry("Nuggets", "Target", 50.9, "05-24-2026")
TimeManager.delete_entry()
TimeManager.save_file("experimental_altered.csv")