import os

import pytest

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
    actual_cost_dict = financial_model.calculate_tag_costs()
    expected_cost_dict = {
        "Groceries": 8.49 + 5.99 + 130.27,
        "Dining" : 6.89
    }

    assert actual_cost_dict == expected_cost_dict

    # Test adding a new entry.
    new_entry = ["Coney", "Leo's", "6.50", "2026-05-06", "Dining"]
    financial_model.add_entry(new_entry)
    actual_cost_dict = financial_model.calculate_tag_costs()
    expected_cost_dict = {
        "Groceries": 8.49 + 5.99 + 130.27,
        "Dining" : 6.89 + 6.50
    }

    assert actual_cost_dict == expected_cost_dict
    
    # Remove the new entry and other dining entry
    rows_to_remove = [financial_model.get_num_rows()-1, financial_model.get_num_rows()-2]
    financial_model.delete_rows(rows_to_remove)
    actual_cost_dict = financial_model.calculate_tag_costs()
    expected_cost_dict = {
        "Groceries": 8.49 + 5.99 + 130.27,
    }

    assert actual_cost_dict == expected_cost_dict