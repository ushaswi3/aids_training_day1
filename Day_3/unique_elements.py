def unique_ele(list):
    unique=[]
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
        if(count[ele]==1):
            unique+=[ele]
    print("unique elements:",unique)
list=[]
unique_ele(list)
