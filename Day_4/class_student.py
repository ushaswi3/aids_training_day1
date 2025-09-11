'''to create a student class with attributes name, roll, marks
atleast 2 students data
Task:
Create atleat 2 student objects with different details
call the display() method for each object'''
class Student():
    def __init__(self,name,roll_no,marks):
        self.name=name
        self.roll_no=roll_no
        self.marks=marks
    def display(self):
        print("Name:",self.name,", roll.no:",self.roll_no,", marks:",self.marks)
stu1=Student("aa",11,25)
stu1.display()
stu2=Student("bb",22,24)
stu2.display()
