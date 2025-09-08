def perfect_num(n):
    for i in range(1,n+1):
        s=0
        for j in range(1,i):
            if(i%j==0):
                s=s+j
        if(i==s):
            print(i,end=" ")
n=int(input("Enter the number:"))
print("Perfect numbers between 1 to",n,"are:")
perfect_num(n)
    


        