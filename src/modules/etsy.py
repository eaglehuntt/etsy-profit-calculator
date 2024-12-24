import os
import glob 
import re
import pandas as pd

class Calculator:
    def __init__(self):
        unsafe_data = self.load_data()
        self.data = self.sanitize_data(unsafe_data)
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    def load_data(self):
        # Path to the 'etsy' folder
        etsy_dir = os.path.join("src/data/etsy", "etsy_statement*.csv")

        # Create a joined list of all csvs in the etsy dir
        joined_list = glob.glob(etsy_dir) 

        # Use the joined list to make a data frame of all data
        df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 
        return df
    
    def sanitize_data(self, data):
        sanitized_data = data.copy()

        sanitized_data.loc[:, "Info"] = sanitized_data.loc[:, "Info"].str.replace("Order #", "")

        condition = sanitized_data['Info'].isna() | sanitized_data['Info'].str.match(r"Funds will be available on .*", na=False)
        sanitized_data.loc[condition, 'Info'] = sanitized_data.loc[condition, 'Title']

        sanitized_data.loc[:, "Info"] = sanitized_data.loc[:, "Info"].str.replace("Payment for Order #", "")

        # Replace the -- with a pandas NA
        sanitized_data["Net"] = sanitized_data["Net"].replace("--", pd.NA)

        # Replace all $ with nothing
        sanitized_data["Net"] = sanitized_data["Net"].str.replace("[$]", "", regex=True)

        # Fill the pandas NA with 0s
        sanitized_data["Net"] = sanitized_data["Net"].fillna(0)

        # Convert the data type from string to float
        sanitized_data["Net"] = sanitized_data["Net"].astype(float)


        sanitized_data["Fees & Taxes"] = sanitized_data["Fees & Taxes"].str.replace("[$]", "", regex=True)
        sanitized_data["Fees & Taxes"] = sanitized_data["Fees & Taxes"].replace("--", pd.NA)
        sanitized_data["Fees & Taxes"] = sanitized_data["Fees & Taxes"].fillna(0)
        sanitized_data["Fees & Taxes"] = sanitized_data["Fees & Taxes"].astype(float)
        
        sanitized_data["Amount"] = sanitized_data["Amount"].str.replace("[$]", "", regex=True)
        sanitized_data["Amount"] = sanitized_data["Amount"].replace("--", pd.NA)
        sanitized_data["Amount"] = sanitized_data["Amount"].fillna(0)
        sanitized_data["Amount"] = sanitized_data["Amount"].astype(float)
        
        return sanitized_data

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

        # Calcluate the net profit by getting the sum of all entries in the net column
        return month_net_profit.sum()

# USAGE: 
# etsy = Calculator()
# print(etsy.get_yearly_net_profit_total())