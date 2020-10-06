import wx
from balz.blocks import Blocks
from balz.balls import Balls
from balz.circle import Circle

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