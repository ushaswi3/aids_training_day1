def armstrong_1ton(n):
    print("Armstrong numbers between 1 to",n,"are:")
    for i in range(1,n+1):
        temp=i
        digits=0
        while(temp>0):
            digits=digits+1
            temp=temp//10

        temp=i
        total=0
        while(temp>0):
            d=temp%10
            total=total+d**digits
            temp=temp//10
        if(total==i):
            print(i,end=" ")

num=int(input("Enter the number:"))
armstrong_1ton(num)

