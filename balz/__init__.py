import wx
from balz.infobar import InfoBar
from balz.board import Board
from balz.navbar import NavBar

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