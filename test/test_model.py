import os
from model import FinancialModel


dir_path = os.path.dirname(os.path.realpath(__file__))

def test_model():
    file_path = dir_path + "/data/money_data.csv"
    financial_model = FinancialModel(file_path)
    assert financial_model.get_num_rows() == 4
    assert financial_model.get_num_cols() == 5

    actual_unique_tags = financial_model.get_unique_tags()
    expected_unique_tags = ["Groceries", "Dining"]
    actual_unique_tags.sort() 
    expected_unique_tags.sort()
    assert actual_unique_tags == expected_unique_tags