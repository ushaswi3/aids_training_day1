"""
A 3-day tech workshop collected attendee registrations separately for each day. 
You are given three lists (day1, day2, day3) of email addresses — 
lists may contain duplicates (people registering multiple times) and email case may vary (Upper/Lower).

Write a Python program that:
Cleans each day's list (normalizes case, removes duplicates).
Prints the total number of unique attendees across all days.
Prints the list of attendees who attended all three days.
Prints the list of attendees who attended exactly one day.
Prints pairwise overlap counts (day1 & day2, day2 & day3, day1 & day3).
Produces a final report with counts and sorted lists for each of the above outputs.
"""

def Cleans_list(day_l):
    s=set()
    for i in day_l:
        s.add(i.lower())
    return list(s)

def unique_Attendees(day1,day2,day3):
    days=[]
    days=day1+day2+day3
    print("total number of unique attendees across all days = ",len(set(days)))

def attended_3days(day1,day2,day3):
    a_3=set()
    a_3=set(day1)&set(day2)&set(day3)
    print("The list of attendees who attended all three days = ",list(a_3))

def attended_1only(day1,day2,day3):
    a_1_list=[]
    a_1=set()
    a_1=list(set(day1+day2+day3))
    for i in a_1:
        class_attended=day1.count(i)+day2.count(i)+day3.count(i)
        if(class_attended==1):
            a_1_list.append(i)
    print("The list of attendees who attended exactly one day = ",a_1_list)

def pairwise_overlap(day1,day2,day3):
    o_d12=list(set(day1)&set(day2))
    o_d23=list(set(day2)&set(day3))
    o_d13=list(set(day1)&set(day3))
    print("overlap counts\n(day1 & day2) = ",len(o_d12),"\n(day2 & day3) = ",len(o_d23),"\n(day1 & day3) = ",len(o_d13))


day1=['abc@gmail.com','aaa@gmail.com','bbb@gmail.com','ddd@gmail.com','DDD@gmail.com']
day2=['bca@gmail.com','aaa@gmail.com','eee@gmail.com','ddd@gmail.com','ddd@gmail.com']
day3=['cab@gmail.com','aaa@gmail.com','fff@gmail.com','ddd@gmail.com','eee@gmail.com','Cab@gmail.com']

day1=Cleans_list(day1)
day2=Cleans_list(day2)
day3=Cleans_list(day3)

unique_Attendees(day1,day2,day3)

attended_3days(day1,day2,day3)

attended_1only(day1,day2,day3)

pairwise_overlap(day1,day2,day3)