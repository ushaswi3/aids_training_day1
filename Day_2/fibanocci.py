def fibonacci(n):
    a,b=0,1
    print("Fibonacci Series:",end=" ")
    for i in range(n):
        print(a,end=" ")
        a,b=b,a+b
num = int(input("Enter n: "))
fibonacci(num)
