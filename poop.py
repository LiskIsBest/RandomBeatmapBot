from pydantic import BaseModel

class Job(BaseModel):
    name: str
    hourly: int
    
class Pooper(BaseModel):
    name: str
    age: int
    job: Job
    
class Person(Pooper):
    gender: str
    age: int
    
# bob = Pooper(name="Bob", age=45, job=Job(name="amazon slave", hourly=28))
bob = Person(gender="male", name="bob", age=25, job=Job(name="amazon slave", hourly=15))

print(bob.age)