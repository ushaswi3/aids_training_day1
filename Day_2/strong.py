def factorial(n):
    fact=1
    for i in range(1, n + 1):
        fact=fact*i
    return fact

def strong(num):
    number= num
    total = 0
    while number>0:
        d=number%10
        total=total+factorial(d)
        number//=10
    return total==num

n = int(input("Enter a number: "))
if strong(n):
    print("Strong number")
else:
    print("Not a Strong number")
