'''to search all occurances of a characterin given string'''
def search_occurances(str,character):
    occurances=[]
    for i in range(len(str)):
        if str[i]==character :
            occurances+=[i]
    if occurances:
        print("Occurances of the  characters are:",occurances)
    else:
        print("character",character,"not found")
s=input("Enter the string:")
ch=input("Enter the charachter to search:")
search_occurances(s,ch)
