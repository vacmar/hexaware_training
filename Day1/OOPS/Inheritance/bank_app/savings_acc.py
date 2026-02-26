# savings_account.py
 
from account import Account
 
class SavingsAccount(Account):
    def __init__(self, account_number, customer_name, balance=0, interest_rate=4):
        super().__init__(account_number, customer_name, balance)
        self.interest_rate = interest_rate
 
    def add_interest(self):
        interest = (self.balance * self.interest_rate) / 100
        self.balance += interest
        print(f"Interest Added: {interest}")
 
