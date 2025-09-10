'''A school stores student records as tuples in the format (roll_no, name, marks).
Write a Python program to:
Store the data of 5 students in a list of tuples.
Print the name of the student who scored the highest marks.
Print all students who scored more than 75 marks.'''

def student_records():
    records=[]
    n=5 
    
    for i in range(n):
        print("Enter details for student",i+1,":")
        roll_no=int(input("Roll number: "))
        name=input("Name: ")
        marks=int(input("Marks: "))
        records.append((roll_no,name,marks))
    print("Student records:")
    for rec in records:
        print(rec)
    
    max_marks=-1
    topper=""
    for rec in records:
        if rec[2]>max_marks:
            max_marks=rec[2]
            topper=rec[1]
    print("Student with highest marks:",topper)
    
    print("Students who scored more than 75 marks:")
    for rec in records:
        if rec[2]>75:
            print(rec[1], ":", rec[2])

student_records()

