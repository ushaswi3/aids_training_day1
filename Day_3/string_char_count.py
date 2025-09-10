def char_count(s):
    alpha_count=0
    digit_count=0
    schar_count=0
    for ch in s:
        if ch.isalpha():
            alpha_count+=1
        elif ch.isdigit():
            digit_count+=1
        else:
            schar_count+=1
    print("Alphabets count:",alpha_count)
    print("Digits count:",digit_count)
    print("Special characters count:",schar_count)

str = input("Enter string: ")
char_count(str)
