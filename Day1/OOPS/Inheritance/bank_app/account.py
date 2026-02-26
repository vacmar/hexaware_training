# account.py
 
class Account:
    def __init__(self, account_number, customer_name, balance=0):
        self.account_number = account_number
        self.customer_name = customer_name
        self.balance = balance
 
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount}")
 
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn: {amount}")
        else:
            print("Insufficient balance!")
 
    def display_balance(self):
        print(f"Account Holder: {self.customer_name}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: {self.balance}")
 
