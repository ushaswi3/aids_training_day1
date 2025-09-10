#to print the second largest in list

def second_largest(l):
    if(len(l)<2):
        print("List should contain atleast 2 elements")
        return
    u_list=list(set(l))
    if(len(u_list)<2):
        print("no second largest, all elements are same")
        return
    u_list.sort()
    print("Second largest is: ",u_list[-2])

n=int(input("Enter number of elements: "))
my_list=[]
for i in range(n):
    ele=int(input("Enter element: "))
    my_list.append(ele)

second_largest(my_list)
    