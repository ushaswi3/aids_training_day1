a= int(input("Enter a:"))
b=int(input("Enter b:"))

#swapping using temp 
print("a before swapping with temp:",a)
print("b before swapping with temp:",b)
temp=a
a=b
b=temp
print("a after swapping with temp:",a)
print("b after swapping with temp:",b)

#swapping without using temp
c= int(input("Enter c:"))
d=int(input("Enter d:"))
c,d=d,c
print("C after swapping:",c)
print("D after swapping:",d)