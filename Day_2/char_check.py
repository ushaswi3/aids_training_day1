def char_check(a):
    if(a.isalpha()):
        if(a.islower()):
            print("It is a lowercase alphabet")
        else:
            print("It is an uppercase alphabet")
    elif(a.isdigit()):
        print("It is a digit")
    else:
        print("It is a special character")
    if(len(a)!=1):
        print("Enter only one character")
a=input("Enter the character:")
char_check(a)



