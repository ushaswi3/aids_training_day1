def diagonal_pattern():
    for i in range(1,n+1):
        for j in range(1,n+1):
            if(i==j or i+j==n+1):
                print("$",end=" ")
            else:
                print("*",end=" ")
        print()
n=int(input("Enter the number:"))
diagonal_pattern()