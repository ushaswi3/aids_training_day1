def count_digits(n):
    count=0
    if n==0:
        count=1
    else:
        while n!=0:
            n=n//10
            count+=1
    print("Number of digits:", count)

num=int(input("Enter the number:"))
count_digits(num)
