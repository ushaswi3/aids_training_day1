def sum_digits(n):
    s=0
    while(n>0):
        s+=n%10
        n//=10
    print("Sum of digits:",s)
num=int(input("Enter the number:"))
sum_digits(num)

