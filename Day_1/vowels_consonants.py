def vowels_consonants(a):
    if a.isalpha():  
        if a in ['a', 'e', 'i', 'o', 'u']:  
            print("Vowel")
        else:
            print("Consonant")
    else:
        print("Not a character")


n = input("Enter the character: ")
vowels_consonants(n)
