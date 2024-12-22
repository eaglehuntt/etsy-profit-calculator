import os
import glob 
import pandas as pd

class Calculator:
    def __init__(self) -> None:
        self.data = self.load_data()
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
    def load_data(self):
        # Path to the 'printful' folder
        printful_dir = os.path.join("src/data/printful/*")
        printful_dir = glob.glob(printful_dir)

        joined_list = []

        for subfolder in printful_dir:
            joined_list += glob.glob(os.path.join(subfolder, "Orders.csv")) 

        df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 

        expenses = df[df["Date"] != "Total paid ($):"]

        return expenses
    
    def get_yearly_expense_total(self):
        total_expenses = 0
        
        for i in range(12):
            total_expenses += self.get_expenses_by_month(i + 1)    
            
        return total_expenses

    def get_expenses_by_month(self, month:int):
        if month > 12 or month < 1:
            raise ValueError("Month must be between 1 and 12")
        
        month_expenses = self.data[self.data["Date"].str.contains(self.months[month - 1])]["Total"]

        # Replace all $ with nothing
        month_expenses = month_expenses.str.replace("[$]", "", regex=True)

        # Convert the data type from string to float
        month_expenses = month_expenses.astype(float)

        # Calcluate the net profit by getting the sum of all entries in the net column
        return month_expenses.sum()
    
# USAGE:
# printful = Printful()
# print(printful.get_yearly_total_expenses())