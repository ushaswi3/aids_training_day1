snum=input("Student number:")
sname=input("Student name:")
m1=int(input("Marks in subject1:"))
m2=int(input("Marks in subject2:"))
m3=int(input("Marks in subject3:"))
#total marks
total=m1+m2+m3
#average marks
avg=(m1+m2+m3)/3
print("Student number:",snum,"\nStudent name:",sname,"\nMarks->subject1:",m1,"\tsubject2:",m2,"\tsubject3:",m3)
print("Total Marks:",total,"\nAverage Marks:",avg)