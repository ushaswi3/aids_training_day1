def exception_handling():
    try:
        div=a/b
        if(b!=0):
            print("Division:",div)
        else:
            raise ZeroDivisionError
    except ZeroDivisionError:
        print("The denominator is zero, Zero division error")
    else:
        print("Division completed successfully")
    finally:
        print("Thank you")
        
a=int(input("Enter num1:"))
b=int(input("Enter num2:"))
exception_handling()