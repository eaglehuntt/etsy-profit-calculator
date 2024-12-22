import os
import glob 
import pandas as pd

import etsy
import printful

etsy = etsy.Calculator()
printful = printful.Calculator()

class ProfitCalculator:

    def __init__(self) -> None:
        self.credit_card_cashback = 0.015
        pass

    def get_yearly_profit(self):
        etsy_net_profit = etsy.get_yearly_net_profit_total()
        printful_expenses = printful.get_yearly_expense_total()
        return etsy_net_profit - printful_expenses

    def get_total_net_profit_by_month(self, month:int):
        if month > 12 or month < 1:
            raise ValueError("Month must be between 1 and 12")
        
        etsy_net_profit = etsy.get_net_profit_by_month(month)
        printful_expenses = printful.get_expenses_by_month(month)

        return etsy_net_profit - printful_expenses
    
    def get_yearly_credit_card_savings(self):
        return printful.get_yearly_expense_total() * self.credit_card_cashback


# USAGE:
# profit_calculator = ProfitCalculator()
# print(profit_calculator.get_yearly_profit())
# print(profit_calculator.get_total_net_profit_by_month(12))
# print(profit_calculator.get_yearly_credit_card_savings())
