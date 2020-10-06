from random import randint

class Circle:
    def __init__(self):
        self.x = []
        self.y = []
        self.count = 0

    def Add(self, a):
        x = randint(0, 5)
        if x not in a:
            a.append(x)
            self.x.append(x * 63 + 8 * (x+1) + 31)
            self.y.append(39)
            self.count += 1
            print("Added new CIRCLE")

    def Move(self):
        for i in range(self.count):
            self.y[i] += 71

    def Destroy(self, id):
        print('REACHED!!!')
        self.x.pop(id)
        self.y.pop(id)
        self.count -= 1
        return True