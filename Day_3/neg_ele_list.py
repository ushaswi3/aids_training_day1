def neg_ele(list):
    neg=[]
    n=int(input("Enter the no.of elements:"))
    for i in range(n):
        ele=int(input())
        list+=[ele]
        if(ele < 0):
            neg+=[ele]
    print("list contains:",list)
    print("negative elemets:",neg)
my_list=[]
neg_ele(my_list)
        

