class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance      # private - can't access directly
 
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
 
    def withdraw(self, amount):
        if amount > self.__balance:
            return "Insufficient funds"
        self.__balance -= amount
 
    def get_balance(self):            # controlled access
        return self.__balance
 
acc = BankAccount("Alice", 1000)
print(acc.owner)          # Alice
print(acc.get_balance())   # 1000   
#print(acc.__balance)      # AttributeError: private attribute can't be accessed directly