import wx

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
        self.currentScore.SetFont(wx.Font(45, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        for st in (self.maxBest, self.maxScore):
            st.SetForegroundColour(wx.Colour(170, 170, 170))
            st.SetFont(wx.Font(21, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        self.sizerScore.AddMany([(0, 2, 0, 0), (self.maxBest), (self.maxScore)])
        self.sizer.AddMany([(10, 0, 0, 0), (self.sizerScore), (120, 0, 0, 0), (self.currentScore, wx.EXPAND), (110, 0, 0, 0)])

        self.SetSizer(self.sizer)

    def IncrementScore(self):
        self.currentScore.SetLabel(str(int(self.currentScore.GetLabel())+1))