import pandas as pd

class FormatError(Exception):
    '''Raised when an input to the financial model is not formatted correctly'''

class FinancialModel:
    def __init__(self, file_path: str):
        self.data = pd.read_csv(file_path)
        self.column_names = self.data.columns
        for i in range(len(self.column_names)):
            if self.column_names[i] == "Price":
                self.price_column = i
            elif self.column_names[i] == "Date":
                self.date_column = i
        
        # Set the datatypes
        self.data["Price"].astype(float)
        self.data["Date"] = pd.to_datetime(self.data["Date"])
    
    def get_num_rows(self) -> int:
        return self.data.shape[0]
    
    def get_num_cols(self) -> int:
        return self.data.shape[1]
    
    def add_entry(self, entry: list[str]) -> None:
        tmp_entry = []
        try:
            for i in range(len(entry)):
                if entry[i] == "":
                    raise FormatError("Error: cannot have empty entries.")

                if i == self.price_column:
                    tmp_entry.append(float(entry[i]))
                elif i == self.date_column:
                    tmp_entry.append(pd.Timestamp(entry[i]))
                else:
                    tmp_entry.append(entry[i])
        except:
            raise FormatError("Error: format not correct")

        tmp_entry = pd.DataFrame([tmp_entry], columns=self.column_names)
        self.data = pd.concat([self.data, tmp_entry], ignore_index=True)

    def delete_rows(self, rows_to_delete):
        self.data.drop(index=rows_to_delete, inplace=True)
    
    def delete_entries(self, entries_to_delete: list[str]) -> None:
        for entry in entries_to_delete:
            # TODO: Prevent these from being hardcoded.
            name = entry[0]
            store = entry[1]
            price = float(entry[2])
            date = entry[3]
            tag = entry[4]
            series_to_remove = self.data[(self.data["Name"] == name) 
                            & (self.data["Store"] == store) 
                            & (self.data["Price"] == price)
                            & (self.data["Date"] == date)
                            & (self.data["Tag"] == tag)]
            index_to_remove = series_to_remove.index
            self.data.drop(index_to_remove, inplace=True)

    def calculate_tag_costs(self, date_range: tuple) -> dict[str, float]:
        """
        Return a dictionary of the cost breakdown for each tag. 
        """
        tags = self.get_unique_tags()
        data = self.get_data_in_date_range(date_range[0], date_range[1])
        cost_dict = {}
        for tag in tags:
            tmp_tag_only_df = data[data["Tag"] == tag]
            tmp_sum = 0
            for i in range(len(tmp_tag_only_df["Price"])):
                tmp_sum += tmp_tag_only_df["Price"].iloc[i]

            if tmp_sum > 0:
                cost_dict[tag] = tmp_sum

        return cost_dict

    def get_unique_tags(self) -> list:
        """
        Return a list containing the unique tags in data.
        """
        tags = self.data["Tag"]
        unique_tags = set({})
        for tag in tags:
            unique_tags.add(tag)

        return list(unique_tags)

    def save_to_file(self, file_path: str) -> None:
        self.data.to_csv(file_path, index=False)
    
    def get_all_data(self) -> pd.DataFrame:
        return self.data
    
    def get_data_in_date_range(
        self, 
        start_date: pd.Timestamp, 
        end_date: pd.Timestamp,
        sorted = False
    ) -> pd.DataFrame:
        selected_data = self.data[(start_date <= self.data["Date"]) & (self.data["Date"] <= end_date)]
        if sorted:
            selected_data.sort_values("Date", inplace=True)

        return selected_data