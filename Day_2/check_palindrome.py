def palindrome(n):
    temp=n
    rev=0
    while n>0:
        digit=n%10
        rev=rev*10+digit
        n//=10
    if(temp==rev):
        print(temp," is a palindrome")
    else:
        print(temp," is not a palindrome")

num=int(input("Enter the number:"))
palindrome(num)

