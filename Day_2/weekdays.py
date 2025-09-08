def weekdays(n):
    if(n==1):
        print("sunday")
    elif(n==2):
        print("monday")
    elif(n==3):
        print("tuesday")
    elif(n==4):
        print("wednesday")
    elif(n==5):
        print("thursday")
    elif(n==6):
        print("friday")
    elif(n==7):
        print("saturday")
    else:
        print("choose valid week day")
n=int(input("Enter the week day:"))
weekdays(n)