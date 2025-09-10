def frequency_ele(list):
    ele_count=0
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
    print("Elements frequency:",count)
list=[]
frequency_ele(list)
