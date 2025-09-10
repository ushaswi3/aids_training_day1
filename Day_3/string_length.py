def string_len_com_con():

    def string_length(str):
        count=0
        for i in str:
            count+=1
        print("Length of string:",count)
    str=input("Enter the string:")
    string_length(str)
    print()

    def compare(s1,s2):
        if(s1==s2):
            print("both strings are equal")
        else:
            print("strings are not equal")
    str1=input("string1:")
    str2=input("string2:")
    compare(str1,str2)
    print()

    def concatenate(s1,s2):
        concat=s1+s2
        print("Concatenation:",concat)
    concatenate(str1,str2)

string_len_com_con()



