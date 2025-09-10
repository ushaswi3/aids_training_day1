def list_addelements(list):
    if not list:
        print("list is empty")
        return
    list=[]
    n=int(input("Enter the no.of elements:"))
    for i in range(n):
        ele=input()
        list+=[ele]
    print("List contains:",list)
list_addelements(list)
        

