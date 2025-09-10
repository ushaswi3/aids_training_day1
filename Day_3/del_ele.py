def del_ele(l):
    if not l:
        print("List is empty")
    
    n=int(input("Enter no. of elements: "))
    for i in range(n):
        ele=input()
        l.append(ele)
    print("List contains:", l)
    
    delete=input("Enter the element to delete: ")
    if delete in l:
        l=[ele for ele in l if ele!=delete] 
        print("Element", delete, "is deleted")
        print("Updated list:", l)
    else:
        print("Element", delete, "is not found")

my_list=[]
del_ele(my_list)
