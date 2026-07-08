import os
import Model


dir_path = os.path.dirname(os.path.realpath(__file__))

def test_model():
    file_path = dir_path + "/data/money_data.csv"
    model = Model.FinancialModel(file_path)
    assert model.get_num_rows() == 4
    assert model.get_num_cols() == 5