def perfect(n):
    total=0
    for i in range(1,n):
        if(n%i==0):
            total=total+i
    if(total==n):
        print(n,"perfect number")
    else:
        print(n,"Not a perfect number")

num=int(input("Enter the number:"))
perfect(num)

