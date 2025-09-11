'''You are asked to design a simple Payment System that can handle different payment methods.
Requirements:
Create a base class Payment with a method pay(amount).
Create three child classes that override the pay(amount) method:
CashPayment → print "Paid ₹<amount> in cash"
CardPayment → print "Paid ₹<amount> using credit/debit card"
UPIPayment → print "Paid ₹<amount> using UPI"
Task:
Create a list of payment objects (CashPayment, CardPayment, UPIPayment).
Loop through them and call pay(1000).
Each object should print a different message.

payments = [CashPayment(), CardPayment(), UPIPayment()]
 
for p in payments:
    p.pay(1000)
Output:
 
cpp
Copy code
Paid ₹1000 in cash
Paid ₹1000 using credit/debit card
Paid ₹1000 using UPI'''

class Payment():
    def pay(self,amount):
        print("Amount:",amount)
    
class CashPayment(Payment):
    def pay(self,amount):
        print("Paid ₹",amount," in cash")

class CardPayment(Payment):
    def pay(self,amount):
        print("Paid ₹",amount," using credit/debit card")

class UPIPayment(Payment):
    def pay(self,amount):
        print("Paid ₹",amount," using UPI")

payments = [CashPayment(), CardPayment(), UPIPayment()]
 
for p in payments:
    p.pay(1000)



