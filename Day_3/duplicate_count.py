def duplicate_count(list):
    duplicate=0
    n=int(input("Enter the no.of elements:"))
    for i in range(n):
        ele=input()
        list+=[ele]
    count={}
    for ele in list:
        if ele in count:
            count[ele]+=1
        else:
            count[ele]=1
        if(count[ele]!=1):
            duplicate+=1
    print("duplicate elements count:",duplicate)
list=[]
duplicate_count(list)
