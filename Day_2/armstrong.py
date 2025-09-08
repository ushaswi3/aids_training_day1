def armstrong(n):
    temp=n
    digits=0
    while(temp>0):
        digits=digits+1
        temp=temp//10

    temp=n
    total=0
    while(temp>0):
        d=temp%10
        total=total+d**digits
        temp=temp//10
    if(total==n):
        print(n," is an armstrong number")
    else:
        print(n,"is not an armstrong number")
        
num=int(input("Enter the number:"))
armstrong(num)

