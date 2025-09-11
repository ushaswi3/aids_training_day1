class BankAccount():
    def __init__(self,balance):
        self.__balance=balance
    def deposit(self,amount):
        self.__balance+=amount
        print("Deposit ₹",self.__balance)

    def withdraw(self,amount):
        self.__balance-=amount
        print("withdraw ₹",self.__balance)

    def get_balance(self):
        print("Current balance:",self.__balance)

ba=BankAccount(0)
ba.deposit(5000)
ba.withdraw(2000)




