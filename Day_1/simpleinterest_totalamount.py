#simple interest  and total amount
p=int(input("Enter the principe amount:"))
t=int(input("Enter the no.of months:"))
r=int(input("Enter the rate of interest:"))

#simple interest
SI=(p*t*r)/100
print("Simple Interest:",SI)

#total amount
TA=p+SI
print("Total Amount:",TA)