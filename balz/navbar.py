import wx

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