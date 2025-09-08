def grade(m):
    if(m>=40):
        if(m>=80):
            print("Distention")
        elif(m>70 and m<80):
            print("Grade A")
        elif(m>50 and m<70):
            print("Grade B")
        elif(m<50 and m>40):
            print("Grade c")
        elif(m==40):
            print("pass")
    else:
        print("Fail")

m=int(input("Enter the marks:"))
grade(m)