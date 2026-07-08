import pandas as pd

class FinancialModel:
    def __init__(self, file_path):
        self.col_names = ["Name", "Store", "Price", "Date", "Tag"]
        self.data = pd.read_csv(file_path)
    
    def get_num_rows(self):
        return self.data.shape[0]
    
    def get_num_cols(self):
        return self.data.shape[1]
    
    def add_entry(self, entry : list):
        tmp_entry = pd.DataFrame([entry], columns=self.col_names)
        self.data = pd.concat([self.data, tmp_entry], ignore_index=True)

    def delete_rows(self):
        pass

    def calculate_tag_costs(self) -> dict[str, float]:
        """
        Return a dictionary of the cost breakdown for each tag. 
        """
        tags = self.get_unique_tags()
        cost_dict = {}
        for tag in tags:
            tmp_tag_only_df = self.data[self.data["Tag"] == tag]
            cost_dict[tag] = tmp_tag_only_df["Price"].sum()

        return cost_dict

    def get_unique_tags(self):
        """
        Return a list containing the unique tags in data.
        """
        tags = self.data["Tag"]
        unique_tags = set({})
        for tag in tags:
            unique_tags.add(tag)

        return list(unique_tags)


    def save_to_file(self, file_path):
        pass