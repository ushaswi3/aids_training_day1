class Emp():
    def __init__(self,name,salary):
        self.name=name
        self.salary=salary
    def display(self):
        print("Employee Details:")
        print("Name:",self.name,", Salary:",self.salary)

class Manager(Emp):
    def __init__(self, name, salary,department):
        super().__init__(name, salary)
        self.department=department
    def display(self):
        super().display()
        print("Department:",self.department)
e1=Manager('aa',70000,'IT')
e1.display()
