class Employee(object):
    "Represents an employee in a company"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return '%s, %s' % (self.name, self.age)
        
    def __lt__(self, other):
        return self.age < other.age
    
john = Employee("John", 40)
bob = Employee("Bob", 30)
print john
print bob
print john < bob
print bob < john