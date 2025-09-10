#to count occurances of a character in given string

def count_occurrences(str,char):
    count=0
    for ch in str:
        if ch==char:
            count+=1
    if count>0:
        print("Character", char, "occurs", count, "times")
    else:
        print("Character", char, "not found")

s=input("Enter the string: ")
ch=input("Enter the character to search: ")
count_occurrences(s,ch)

