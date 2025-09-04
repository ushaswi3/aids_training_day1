def temp_c_f():
    c=int(input("enter the temp in celsius:"))
    f=((9/5)*c)+32
    return f
result=temp_c_f()
print("temperature in fahreinheit:",result)