from random import randint

class Blocks:
    def __init__(self):
        self.count = 0
        self.x = []
        self.y = []
        self.text = []

    def Add(self, text):
        xs = []
        for _ in range(randint(2, 4)):
            x = randint(0, 5)
            if x not in xs:
                xs.append(x)
                self.x.append(x * 63 + 8 * (x+1))
                self.y.append(8)
                self.text.append(str(text))
                self.count += 1
        return xs

    def Move(self):
        if len(self.y) != 0:
            for i in range(len(self.y)):
                self.y[i] = self.y[i] + 71

    def CheckZero(self, id):
        if self.text[id] == "1":
            self.x.pop(id)
            self.y.pop(id)
            self.text.pop(id)
            self.count -= 1
        else:
            self.text[id] = str(int(self.text[id]) - 1)

    def isEnd(self):
        for i in range(self.count):
            if self.y[i] > 470:
                return True
        return False