# main.py
 
from savings_acc import SavingsAccount
from current_acc import CurrentAccount
 
print("----- Savings Account -----")
savings = SavingsAccount("S123", "Bhuvaneswari", 10000)
savings.deposit(2000)
savings.add_interest()
savings.withdraw(3000)
savings.display_balance()
 
print("\n----- Current Account -----")
current = CurrentAccount("C456", "Visweswaran", 5000)
current.withdraw(7000)
current.display_balance()
 