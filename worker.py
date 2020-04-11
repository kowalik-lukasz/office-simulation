class Worker:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def display(self):
        print('I am a person', self)

    def great(self):
        print("How you doing'?", self)

w1 = Worker("Tom", 20)
w2 = Worker("Ben", 30)

w1.display()
w1.great()

w2.display()
w2.great()
