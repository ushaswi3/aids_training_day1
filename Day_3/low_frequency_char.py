#to print low frequency element
def low_frequency(list):
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

    min_freq=min(count.values())
    low_freq=[k for k, v in count.items() if v==min_freq]
    print("Lowest frequency elements:", low_freq)
list=[]
low_frequency(list)


