import os
import glob 
import pandas as pd

class Calculator:
    def __init__(self) -> None:
        unsafe_data = self.load_data()
        self.data = self.sanitize_data(unsafe_data)

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
    
    def sanitize_data(self, data):
        
        sanitized_data = data.copy()

        sanitized_data.loc[:, "Order"] = sanitized_data.loc[:, "Order"].str.replace("Order ", "")
        sanitized_data.loc[:, "Order"] = sanitized_data.loc[:, "Order"].str.replace("Refund to wallet ", "")

        # Replace all $ with nothing and convert data from string to float

        sanitized_data.loc[:, "Total"] = sanitized_data.loc[:, "Total"].str.replace("[$]", "", regex=True).astype(float)

        sanitized_data.loc[:, "Products"] = sanitized_data.loc[:, "Products"].str.replace("[$]", "", regex=True).astype(float)

        sanitized_data.loc[:, "Shipping"] = sanitized_data.loc[:, "Shipping"].str.replace("[$]", "", regex=True).astype(float)

        return sanitized_data
    
    def get_yearly_expense_total(self):
        total_expenses = 0
        
        for i in range(12):
            total_expenses += self.get_expenses_by_month(i + 1)    
            
        return total_expenses

    def get_expenses_by_month(self, month:int):
        if month > 12 or month < 1:
            raise ValueError("Month must be between 1 and 12")
        
        month_expenses = self.data[self.data["Date"].str.contains(self.months[month - 1])]["Total"]

        # Calcluate the net profit by getting the sum of all entries in the net column
        return month_expenses.sum()
    
# USAGE:
# printful = Calculator()
# print(printful.get_yearly_expense_total())