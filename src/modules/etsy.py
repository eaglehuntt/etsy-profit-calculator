import os
import glob 
import pandas as pd

class Etsy:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        # Path to the 'etsy' folder
        etsy_dir = os.path.join("src/data/etsy", "etsy_statement*.csv")

        # Create a joined list of all csvs in the etsy dir
        joined_list = glob.glob(etsy_dir) 

        # Use the joined list to make a data frame of all data
        df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 
        return df

    def get_net_profit(self):
        # Get all entries in "Net" column
        net = self.data["Net"]

        # Replace the random -- with a pandas NA
        net = net.replace("--", pd.NA)

        # Replace all $ with nothing
        net = net.str.replace("[$]", "", regex=True)

        # Fill the pandas NA with 0s
        net = net.fillna(0)

        # Convert the data type from string to float
        net = net.astype(float)

        # Calcluate the net profit by getting the sum of all entries in the net column
        return net.sum()


# USAGE: 
# etsy = Etsy()
# print(etsy.get_net_profit())