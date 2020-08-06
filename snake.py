import wx
from random import randint

class Snake:
    def __init__(self, px, py, d):
        self.x = []
        self.y = []
        self.x.append(randint(10, ((px/d)-10)) * d)
        self.y.append(randint(10, ((py/d)-10)) * d)
        self.d = d

    def Add(self, dir):
        if dir == "W":
            self.x.append(self.x[-1])
            self.y.append(self.y[-1] - self.d)
        elif dir == "S":
            self.x.append(self.x[-1])
            self.y.append(self.y[-1] + self.d)
        elif dir == "D":
            self.x.append(self.x[-1] + self.d)
            self.y.append(self.y[-1])
        elif dir == "A":
            self.x.append(self.x[-1] - self.d)
            self.y.append(self.y[-1])

    def Move(self, dir):
        if len(self.x) == 1:
            self.MoveHead(dir)
        else:
            self.x.pop()
            self.y.pop()
            self.x.insert(0, self.x[0])
            self.y.insert(0, self.y[0])
            self.MoveHead(dir)

    def MoveHead(self, dir):
        if dir == "W":
            self.y[0] = self.y[0] - self.d
        elif dir == "S":
            self.y[0] = self.y[0] + self.d
        elif dir == "D":
            self.x[0] = self.x[0] + self.d
        elif dir == "A":
            self.x[0] = self.x[0] - self.d


class Food:
    def __init__(self, px, py, d):
        self.x = randint(10, ((px/d)-10)) * d  + (d/2)
        self.y = randint(10, ((py/d)-10)) * d  + (d/2)

    def Update(self, px, py, d, sx, sy):
        self.x = randint(10, ((px/d)-10)) * d  + (d/2)
        self.y = randint(10, ((py/d)-10)) * d  + (d/2)

        if (self.x in sx) and (self.y in sy):
            self.Update(px, py, d, sx, sy)


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent, size=(800, 600))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        self.timer.Start(150)
        self.timerSwitch = False


        self.key = ["W", "A", "S", "D"][randint(0, 3)]
        self.d = 20
        self.px = self.GetSize().GetWidth()
        self.py = self.GetSize().GetWidth()

        self.snake = Snake(self.px, self.py, self.d)
        print(self.snake.x)
        print(self.snake.y)
        self.food = Food(self.px, self.py, self.d)
        print(self.food.x, self.food.y)

    def OnTimer(self, e):
        if self.timerSwitch:
            self.timer.Stop()
            wx.MessageBox(message=str("Score " + str(len(self.snake.x)-1)))
        else:
            sx = self.snake.x
            sy = self.snake.y

            # выход за рамки панели
            if (sx[0] >= self.px) or (sx[0] <= 0) or (sy[0] >= self.py) or (sy[0] <= 0):
                self.timerSwitch = True

            # cтолкновение головы с телом
            for i in range(1, len(self.snake.x)):
                if (sx[0] == sx[i]) and (sy[0] == sy[i]):
                    self.timerSwitch = True


            # проверка на съедение еды
            if (sx[0] == self.food.x - (self.d / 2)) and (sy[0] == self.food.y - (self.d / 2)):
                self.food.Update(self.px, self.py, self.d, self.snake.x, self.snake.y)
                print(self.food.x, self.food.y)
                self.snake.Add(self.key)

            self.snake.Move(self.key)

            self.Refresh(True)


    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.DrawCircle(self.food.x, self.food.y, self.d/2)


        for i in range(len(self.snake.x)):
            if i == 0:
                dc.Brush = wx.Brush(wx.Colour(0, 0, 0))
            else:
                dc.Brush = wx.Brush(wx.Colour(200, 200, 200))
            dc.DrawRectangle(self.snake.x[i], self.snake.y[i], self.d, self.d)


    def OnKey(self, event):
        ch = chr(event.GetUnicodeKey()).upper()
        if (self.key == "W" and ch == "S") or\
            (self.key == "S" and ch == "W") or\
            (self.key == "A" and ch == "D") or\
            (self.key == "D" and ch == "A"):
            pass
        else:
            self.key = chr(event.GetUnicodeKey()).upper()


class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Main")
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()