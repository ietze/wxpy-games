import wx
from random import randint

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        self.but = wx.Button(self, label="Press me!", size=(50, 50), pos=(400, 360))
        self.but.Bind(wx.EVT_BUTTON, self.OnClick)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.d = []
        self.flag = False

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer.Start(1)

    def OnClick(self, evt):
        self.flag = True

    def OnTimer(self, e):
        for b in self.d:
            if self.GetSize().GetHeight() <= b.y + b.rad or b.y - b.rad <= 0:
                b.yDir = -b.yDir
            if self.GetSize().GetWidth() <= b.x + b.rad or b.x - b.rad <= 0:
                b.xDir = -b.xDir
            b.x += b.xDir
            b.y += b.yDir
        self.Refresh(True)


    def OnPaint(self, e):
        dc = wx.PaintDC(self)

        if self.flag:
            x   = randint(1, 500)
            y   = randint(1, 500)
            rad = randint(5, 30)
            xDir= randint(-5, 5)
            yDir= randint(-5, 5)
            clr = wx.Colour(randint(1, 250), randint(1, 250), randint(1, 250))

            newCircle = ball(wx.PaintDC(self), x, y, rad, xDir, yDir, clr)

            self.d.append(newCircle)
            self.flag = False

        if len(self.d) > 0:
            for b in self.d:
                dc.SetBrush(wx.Brush(b.clr))
                dc.DrawCircle(b.x, b.y, b.rad)

class ball:
    def __init__(self, obj, x, y, rad, xDir, yDir, clr):
        self.obj = obj
        self.x = x
        self.y = y
        self.rad = rad
        self.xDir = xDir
        self.yDir = yDir
        self.clr = clr


class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title, size=(900, 580))
        self.panel = MyPanel(self)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Main")
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()