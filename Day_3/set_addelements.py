#to add elements in a set runtime

def add_elements(s):
    if not s:
        print("set is empty")
    
    n=int(input("Enter the no.of elements:"))
    for i in range(n):
        ele=input()
        s.add(ele)
    print("set contains:",s)
my_set=set()
add_elements(my_set)
        

