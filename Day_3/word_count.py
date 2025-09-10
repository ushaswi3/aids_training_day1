'''to find total no.of words in a string'''

def word_count(s):
    words=s.split()
    print("Total number of words:", len(words))
str=input("Enter a string: ")
word_count(str)



