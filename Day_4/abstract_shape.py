'''Create an abstract class Shape that defines:
 
An abstract method area() (no implementation).
Create two child classes that inherit from Shape:
Rectangle → has attributes length, breadth, and implements area().
Circle → has attribute radius, and implements area().
Task:
Define the abstract class Shape using the abc module.
Implement Rectangle and Circle classes by providing their own version of area().
Create one object of Rectangle and one of Circle, then display their areas.
 
from abc import ABC, abstractmethod
 
# Abstract class
class Shape(ABC):
 
    @abstractmethod           # Abstract method
    def area(self):
        pass'''

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self,length, breadth):
        self.length=length
        self.breadth=breadth
    def area(self):
        ar=2*(self.length+self.breadth)
        print("Rectangle Area:",ar)

class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius
    def area(self):
        a=3.14*(self.radius)*(self.radius)
        print("Circle area:",a)

rec=Rectangle(2,5)
rec.area()
cir=Circle(4)
cir.area()
        
    