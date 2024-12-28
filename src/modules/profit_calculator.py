import pandas as pd
import etsy
import printful

etsy = etsy.Calculator()
printful = printful.Calculator()

class ProfitCalculator:

    def __init__(self) -> None:
        self.credit_card_cashback = 0.015
        self.transaction_data = self.load_transaction_data()

    def load_transaction_data(self):
        
        # Load Etsy and Printful data
        etsy_transactions = etsy.data.loc[:, ("Info", "Amount", "Type", "Title", "Date", "Fees & Taxes")].copy()
        printful_transactions = printful.data.loc[:, ("Date", "Order", "Products", "Shipping", "Total")].copy()

        # Convert Printful's Total column to negative (fees expense)
        printful_transactions["Total"] = printful_transactions["Total"].astype(float) * -1
        printful_transactions["Products"] = printful_transactions["Products"].astype(float) * -1
        printful_transactions["Shipping"] = printful_transactions["Shipping"].astype(float) * -1

        printful_transactions.rename(columns={
            'Date': 'Date_Processed', 
            'Total': 'Printful_Total_Fees',
        }, inplace=True)

        # Rename Etsy's Info column to match Printful's 'Order'
        etsy_transactions.rename(columns={"Info": "Order"}, inplace=True)

        # Step 1: Sum negative values in Etsy's "Fees & Taxes" column by Order number
        etsy_fees = etsy_transactions[etsy_transactions['Fees & Taxes'] < 0]  # Filter out negative fees
        etsy_fees_total = etsy_fees.groupby('Order')['Fees & Taxes'].sum().reset_index()  # Sum negative fees by Order number
        etsy_fees_total.rename(columns={'Fees & Taxes': 'Etsy_Total_Fees'}, inplace=True)  # Rename for clarity

        # Step 2: Get the corresponding "Amount" value from Etsy for each Order number
        # Filter out rows where Amount is 0, then drop duplicates based on 'Order'
        etsy_amount = etsy_transactions[etsy_transactions['Amount'] > 0][['Order', 'Amount']].drop_duplicates(subset='Order').reset_index(drop=True)

        # Rename the 'Amount' column to 'Customer_Paid' for clarity
        etsy_amount.rename(columns={'Amount': 'Customer_Paid'}, inplace=True)

        # Step 3: Merge the Printful data with the Etsy fees and Amount data
        merged_df = pd.merge(printful_transactions, etsy_fees_total, how='left', on='Order')
        merged_df = pd.merge(merged_df, etsy_amount, how='left', on='Order')

        # Step 4: Calculate the Net Profit (Amount from Etsy + (Printful Total Fees + Etsy Total Fees))

        merged_df['Customer_Paid'] = merged_df['Customer_Paid'].fillna(0)
        merged_df['Etsy_Total_Fees'] = merged_df['Etsy_Total_Fees'].fillna(0)

        merged_df['Net_Profit'] = merged_df['Customer_Paid'] + (merged_df['Printful_Total_Fees'] + merged_df['Etsy_Total_Fees'])

        # Step 5: Finalize the columns
        result_df = merged_df[['Order', 'Date_Processed', 'Printful_Total_Fees', 'Etsy_Total_Fees', 'Customer_Paid', 'Net_Profit']]

        return result_df
        

    def get_yearly_profit(self):
        etsy_net_profit = etsy.get_yearly_net_profit_total()
        printful_expenses = printful.get_yearly_expense_total()
        return etsy_net_profit - printful_expenses

    def get_total_net_profit_by_month(self, month: int):
        if month > 12 or month < 1:
            raise ValueError("Month must be between 1 and 12")
        
        etsy_net_profit = etsy.get_net_profit_by_month(month)
        printful_expenses = printful.get_expenses_by_month(month)

        return etsy_net_profit - printful_expenses
    
    def get_yearly_credit_card_savings(self):
        return printful.get_yearly_expense_total() * self.credit_card_cashback

    def generate_total_profit_csv(self):
        # Output the final dataframe
        self.transaction_data.to_csv('out.csv', index=False) 
        pass

    def generate_monthly_profit_csv(self, month: int):
        pass

# USAGE:
profit_calculator = ProfitCalculator()
# profit_calculator.generate_total_profit_csv()
# print(profit_calculator.get_yearly_profit())
# print(profit_calculator.get_total_net_profit_by_month(12))
# print(profit_calculator.get_yearly_credit_card_savings())
