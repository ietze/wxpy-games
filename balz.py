import wx
from random import randint
from math import fabs, sqrt

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

class Circle:
    def __init__(self):
        self.x = []
        self.y = []
        self.count = 0

    def Add(self, a):
        #if randint(1, 3) != 1:
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

class Blocks:
    def __init__(self):
        self.count = 0
        self.x = []
        self.y = []
        self.text = []

    def Add(self, text):
        xs = []
        for i in range(randint(2, 4)):
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

class InfoBar(wx.Panel):
    def __init__(self, parent):
        super(InfoBar, self).__init__(parent, size=(450, 65))
        self.parent = parent

        self.SetBackgroundColour(wx.Colour(38, 38, 38))

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerScore = wx.BoxSizer(wx.VERTICAL)

        self.maxBest = wx.StaticText(self, label = "BEST", size=(100, 30), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.maxScore = wx.StaticText(self, label = "0", size=(100, 30), style=wx.ALIGN_CENTER_HORIZONTAL)

        self.currentScore = wx.StaticText(self, label = "1", size=(100, 75))
        self.currentScore.SetForegroundColour(wx.Colour(200, 200, 200))
        #self.currentScore.SetBackgroundColour(wx.Colour(60, 60, 60))
        self.currentScore.SetFont(wx.Font(45, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        for st in (self.maxBest, self.maxScore):
            st.SetForegroundColour(wx.Colour(170, 170, 170))
            #st.SetBackgroundColour(wx.Colour(60, 60, 60))
            st.SetFont(wx.Font(21, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        self.sizerScore.AddMany([(0, 2, 0, 0), (self.maxBest), (self.maxScore)])
        self.sizer.AddMany([(10, 0, 0, 0), (self.sizerScore), (120, 0, 0, 0), (self.currentScore, wx.EXPAND), (110, 0, 0, 0)])

        self.SetSizer(self.sizer)

    def IncrementScore(self):
        self.currentScore.SetLabel(str(int(self.currentScore.GetLabel())+1))

class Board(wx.Panel):
    def __init__(self, parent):
        super(Board, self).__init__(parent, size=(450, 575))

        self.parent = parent

        self.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.dash = wx.Pen(wx.Colour(250, 250, 250), 5, wx.PENSTYLE_DOT)
        self.point = wx.Pen(wx.Colour(250, 250, 250), 1, wx.SOLID)

        self.mode = 0
        self.blocks = Blocks()
        self.balls = Balls()
        self.circle = Circle()
        self.xm, self.ym = 0, 0
        self.ct = 0
        self.iteration = 1
        self.blocks.Add(self.iteration)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetPen(self.point)

        for i in range(self.blocks.count):
            dc.SetBrush(wx.Brush(wx.Colour(100, 200, 200)))
            dc.DrawRectangle(self.blocks.x[i], self.blocks.y[i], 63, 63)
            dc.SetBrush(wx.Brush(wx.Colour(240, 240 ,240)))
            dc.DrawLabel(self.blocks.text[i], wx.Rect(self.blocks.x[i], self.blocks.y[i] + 20, 63, 63), wx.ALIGN_CENTER_HORIZONTAL)

        for i in range(self.circle.count):
            dc.SetBrush(wx.Brush(wx.Colour(200, 200, 50)))
            dc.DrawCircle(self.circle.x[i], self.circle.y[i], 20)

        dc.SetBrush(wx.Brush(wx.Colour(240, 240 , 240)))
        if self.mode == 0:              # waiting
            dc.DrawCircle(self.balls.x0, 570, 5)

        if self.mode == 1:              # aiming
            self.Aiming(event, dc)

        if self.mode == 2:              # action
            self.Action(event, dc)

        if self.mode == 3:              # blockmove
            self.BlockMove(event, dc)

    def Aiming(self, event, dc):
        dc.DrawCircle(self.balls.x0, 570, 5)
        dc.SetPen(self.dash)
        x0, y0 = self.balls.x0, 570
        x1, y1  = 2*x0 - self.xm, y0 - self.ym
        if y1 < 560:
            dc.DrawLine(x0, y0, x1, y1)
        else:
            dc.DrawLine(x0, y0, x1, 560)

    def Action(self, event, dc):
        self.ct += 1
        self.balls.Move()
        self.balls.isCollision(self.blocks, self.circle)

        if self.balls.realCount > self.balls.currentCount:
            if self.ct % 3 == 0:
                self.balls.Add()
                print("New Ball")
                self.balls.currentCount += 1

        if self.balls.isEnd():
            print("THE END")
            self.iteration += 1
            self.balls.IncreaseCount()
            self.SetMode(0)
            self.blocks.Move()
            self.circle.Move()
            if self.blocks.isEnd():
                self.parent.timer.Stop()
                wx.MessageBox(message="THE END")
            a = self.blocks.Add(self.iteration)
            self.circle.Add(a)
            self.parent.infoBar.IncrementScore()

        for i in range(self.balls.currentCount):
            dc.DrawCircle(self.balls.x[i], self.balls.y[i], 5)

    def BlockMove(self, event, dc):
        pass

    def SetMode(self, mode_id):
        self.mode = mode_id

class NavBar(wx.Panel):
    def __init__(self, parent):
        super(NavBar, self).__init__(parent, size=(450, 130))
        self.parent = parent

        self.SetBackgroundColour(wx.Colour(38, 38, 38))

        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        self.LeftDown = False

    def OnMotion(self, event):
        if self.LeftDown:
            self.parent.board.xm, self.parent.board.ym = event.GetPosition()

    def OnLeftUp(self, event):
        if self.parent.board.mode == 1:
            self.LeftDown = False
            self.parent.board.SetMode(2)
            self.parent.board.balls.SetAngle(event.GetPosition())

    def OnLeftDown(self, event):
        if self.parent.board.mode == 0:
            self.LeftDown = True
            #print(True)
            self.parent.board.SetMode(1)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self.infoBar = InfoBar(self)
        self.board = Board(self)
        self.navBar = NavBar(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddMany([(self.infoBar), (self.board), (self.navBar)])

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self)
        self.SetSizer(self.sizer)

        self.timer.Start(30)

    def OnTimer(self, event):
        self.board.Refresh()

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title, size=(465, 800), pos=(400, 50))
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Balz")
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()