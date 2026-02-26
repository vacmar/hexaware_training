# current_account.py
 
from account import Account
 
class CurrentAccount(Account):
    def __init__(self, account_number, customer_name, balance=0, overdraft_limit=5000):
        super().__init__(account_number, customer_name, balance)
        self.overdraft_limit = overdraft_limit
 
    def withdraw(self, amount):
        if amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            print(f"Withdrawn: {amount}")
        else:
            print("Overdraft limit exceeded!")
 
