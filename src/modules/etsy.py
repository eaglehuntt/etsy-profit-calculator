import os
import glob 
import pandas as pd

class Etsy:
    def __init__(self):
        self.data = self.load_data()
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    def load_data(self):
        # Path to the 'etsy' folder
        etsy_dir = os.path.join("src/data/etsy", "etsy_statement*.csv")

        # Create a joined list of all csvs in the etsy dir
        joined_list = glob.glob(etsy_dir) 

        # Use the joined list to make a data frame of all data
        df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 
        return df

    def get_yearly_net_profit_total(self):
       net_profit_total = 0
       
       for i in range(12):
           net_profit_total += self.get_net_profit_by_month(i + 1)    
           
       return net_profit_total
    
    def get_net_profit_by_month(self, month:int):

        if month > 12 or month < 1:
            raise ValueError("Month must be between 1 and 12")

        # Get all transactions from specified month
        month_net_profit = self.data[self.data["Date"].str.contains(self.months[month - 1])]["Net"]

        # Replace the -- with a pandas NA
        month_net_profit = month_net_profit.replace("--", pd.NA)

        # Replace all $ with nothing
        month_net_profit = month_net_profit.str.replace("[$]", "", regex=True)

        # Fill the pandas NA with 0s
        month_net_profit = month_net_profit.fillna(0)

        # Convert the data type from string to float
        month_net_profit = month_net_profit.astype(float)

        # Calcluate the net profit by getting the sum of all entries in the net column
        return month_net_profit.sum()

# USAGE: 
# etsy = Etsy()
# print(etsy.get_net_profit_total())