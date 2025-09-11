'''to count total no.of vowels and consonats in a string'''

def vowels_consonants(s):
    c=v=0
    for i in range(0,len(s)):
        if(s[i].isalpha()):
            if(s[i] in ['a','e','i','o','u']):
                v+=1
            else:
                c+=1
    print(s," has consonats:",c," vowels:",v)
s=input("Enter the string:")
vowels_consonants(s)