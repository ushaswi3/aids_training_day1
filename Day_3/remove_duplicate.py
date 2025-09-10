def remove_duplicate(l):
    if not l:
        print("List is empty")
        return
    
    dup=[]
    for i in l:
        if i not in dup:
            dup.append(i)
    print("List after removing duplicates:", dup)


n=int(input("Enter no of elements: "))
l=[]
for i in range(n):
    ele=input("Enter element: ")
    l.append(ele)
print("List contains:", l)
remove_duplicate(l)
