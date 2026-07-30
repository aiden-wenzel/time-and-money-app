import os

import pytest
import pandas as pd

from model import FinancialModel

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def test_model():

    # Basic test
    file_path = DIR_PATH + "/data/money_data.csv"
    financial_model = FinancialModel(file_path)
    assert financial_model.get_num_rows() == 4
    assert financial_model.get_num_cols() == 5

    # Test getting unique tags.
    actual_unique_tags = financial_model.get_unique_tags()
    expected_unique_tags = ["Groceries", "Dining"]
    actual_unique_tags.sort() 
    expected_unique_tags.sort()

    assert actual_unique_tags == expected_unique_tags

    # Test tag costs.
    actual_cost_dict = financial_model.calculate_tag_costs((pd.Timestamp.min, pd.Timestamp.max))
    expected_cost_dict = {
        "Groceries": 8.49 + 5.99 + 130.27,
        "Dining" : 6.89
    }

    assert actual_cost_dict == expected_cost_dict

    # Test adding a new entry.
    new_entry = ["Coney", "Leo's", "6.50", "2026-05-06", "Dining"]
    financial_model.add_entry(new_entry)
    actual_cost_dict = financial_model.calculate_tag_costs((pd.Timestamp.min, pd.Timestamp.max))
    expected_cost_dict = {
        "Groceries": 8.49 + 5.99 + 130.27,
        "Dining" : 6.89 + 6.50
    }

    assert actual_cost_dict == expected_cost_dict
    
    # Remove the new entry and other dining entry
    rows_to_remove = [financial_model.get_num_rows()-1, financial_model.get_num_rows()-2]
    financial_model.delete_rows(rows_to_remove)
    actual_cost_dict = financial_model.calculate_tag_costs((pd.Timestamp.min, pd.Timestamp.max))
    expected_cost_dict = {
        "Groceries": 8.49 + 5.99 + 130.27,
    }

    assert actual_cost_dict == expected_cost_dict    

def test_date_range():
    file_path = DIR_PATH + "/data/money_data.csv"
    financial_model = FinancialModel(file_path)

    # Get data within the month of April.
    current_day = pd.Timestamp("2026-04-30")
    april_finances = financial_model.get_data_in_date_range(
        pd.offsets.MonthBegin().rollback(current_day), 
        pd.offsets.MonthEnd().rollforward(current_day),
    )
    assert april_finances.shape[0] == 1
    assert april_finances["Name"].iat[0] == "Groceries"
    assert april_finances["Store"].iat[0] == "Meijer"

def test_edit_item():
    file_path = DIR_PATH + "/data/money_data.csv"
    financial_model = FinancialModel(file_path)
    data = financial_model.get_all_data()
    selection_index = data.loc[data["Name"] == "Groceries"].index
    col_to_change = "Price"
    value = 15.0
    financial_model.edit_item(selection_index, col_to_change, value) 

    pytest.approx(data.loc[selection_index, col_to_change], 15.0)

    try:
        financial_model.edit_item(selection_index, "Date", 15.0)
    except TypeError:
        pass