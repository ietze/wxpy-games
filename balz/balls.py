from math import fabs, sqrt
from circle import Circle

class Balls:
    def __init__(self):
        self.currentCount = 0
        self.realCount = 1
        self.x, self.y = [225], [570]
        self.xDir, self.yDir = [0], [0]

        self.x0 = 225
        self.xStep = 0
        self.yStep = 0
        self.speed = 10
        self.endCount = 0
        self.increasedCount = 0

    def IncreaseCount(self):
        self.realCount += self.increasedCount
        self.increasedCount = 0
        self.currentCount = 0

    def Add(self):
        self.x.append(self.x0)
        self.y.append(570)
        self.xDir.append(self.xStep)
        self.yDir.append(self.yStep)

    def Move(self):
        for i in range(self.currentCount):
            self.x[i] += self.xDir[i]
            self.y[i] += self.yDir[i]

    def SetAngle(self, mousePos):
        x, y = mousePos
        x = fabs(self.x0-x)
        z = sqrt((x**2) + (y**2))
        self.xStep = self.speed*(fabs(x)/z)
        self.yStep = -self.speed*(y/z)
        if mousePos[0] > self.x0:
            self.xStep *= (-1)
        self.xDir[0] = self.xStep
        self.yDir[0] = self.yStep

    def isCollision(self, blocks, circle):
        for i in range(self.currentCount):
            if self.x[i] -5 <= 5 or self.x[i] + 5>= 440:
                self.xDir[i] *= (-1)
            if self.y[i] - 5<= 0:
                self.yDir[i] *= (-1)

            #print(self.y[i])
            if self.y[i] >= 580:
                #print(self.y[i])
                self.xDir[i] = 0
                self.yDir[i] = 0
                self.y[i] = 570
                self.x[i] -= self.xDir[i]
                self.endCount += 1
                #print(self.endCount)

            for k in range(blocks.count):
                if blocks.y[k] <=  self.y[i] <= blocks.y[k]+63 and blocks.x[k]+63 <=  self.x[i] <= blocks.x[k]+73:
                    self.xDir[i] *= (-1)
                    blocks.CheckZero(k)
                    break

                if blocks.x[k] <=  self.x[i] <= blocks.x[k]+63 and blocks.y[k]+63 <=  self.y[i] <= blocks.y[k]+73:
                    self.yDir[i] *= (-1)
                    blocks.CheckZero(k)
                    break

                if blocks.y[k] <=  self.y[i] <= blocks.y[k]+63 and blocks.x[k] - 10<=  self.x[i] <= blocks.x[k]:
                    self.xDir[i] *= (-1)
                    blocks.CheckZero(k)
                    break

                if blocks.x[k] <=  self.x[i] <= blocks.x[k]+63 and blocks.y[k] - 10 <=  self.y[i] <= blocks.y[k]:
                    self.yDir[i] *= (-1)
                    blocks.CheckZero(k)
                    break

            for k in range(circle.count):
                if circle.x[k]-20 <= self.x[i] <= circle.x[k]+ 20 and circle.y[k] -20 <= self.y[i] <= circle.y[k]+ 20:
                    if circle.Destroy(k):
                        self.increasedCount += 1
                    break


    def isEnd(self):
        if self.endCount >= self.realCount:
            self.x0 = self.x[0]
            self.x = [self.x0]
            self.y = [570]
            self.xDir = [0]
            self.yDir = [0]
            self.currentCount = 1
            self.endCount = 0
            return True
        else:
            return False