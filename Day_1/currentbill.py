cnum=input("Consumer number:")
cname=input("Consumer name:")
pmr=int(input("Enter present month readings:"))
lmr=int(input("Enter last month readings:"))
total_units=pmr-lmr
result=total_units*3.80
print("Consumer number:",cnum,"\nConsumner name:",cname)
print("Currntbill:",round(result,2))

message=f"Customer number:{cnum} Customer name:{cname}!  Your currentbill is {result}"
print(message)