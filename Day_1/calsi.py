#  with arguments and return type
def calsi(a, b, op):
    if op == "add":
        return a + b
    elif op == "sub":
        return a - b
    elif op == "mul":
        return a * b
    elif op == "div":
        if b != 0:
            return a / b
        else:
            return "Error! Division by zero."
    else:
        return "choose valid operation."

num1 = int(input("Enter num1: "))
num2 = int(input("Enter num2: "))
op = input("Enter operation (add, sub, mul, div): ")

result = calsi(num1, num2, op)
print("Result:", result)
