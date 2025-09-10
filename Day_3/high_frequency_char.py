#to print high frequency element
def high_frequency(list):
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

    max_freq=max(count.values())
    high_freq=[k for k, v in count.items() if v == max_freq]
    print("High frequency elements:", high_freq)
list=[]
high_frequency(list)


