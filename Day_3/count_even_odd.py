def count_even_odd(list):
    even_count=0
    odd_count=0
    list=[]
    n=int(input("Enter the no.of elements:"))
    for i in range(n):
        ele=int(input())
        list+=[ele]
        if(ele%2==0):
            even_count+=1
        else:
            odd_count+=1
    print("even_count:",even_count)
    print("odd_count:",odd_count)
count_even_odd(list)

        

