import wx
import random
from time import sleep


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)



        self.textColour = wx.Colour(150, 150, 150, 100)
        self.butSize = 100
        self.mode = 0
        self.cSize = (150, 20)

        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.gridSizer = wx.GridSizer(3, 3, 4, 4)

        self.ctrlSizer = wx.BoxSizer(wx.VERTICAL)


        self.winnerDisplay = wx.StaticText(self, label="")
        self.winnerDisplay.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, False))
        self.winnerDisplay.SetForegroundColour(self.textColour)

        self.but1 = wx.Button(self, size=(self.butSize, self.butSize))
        self.but2 = wx.Button(self, size=(self.butSize, self.butSize))
        self.but3 = wx.Button(self, size=(self.butSize, self.butSize))
        self.but4 = wx.Button(self, size=(self.butSize, self.butSize))
        self.but5 = wx.Button(self, size=(self.butSize, self.butSize))
        self.but6 = wx.Button(self, size=(self.butSize, self.butSize))
        self.but7 = wx.Button(self, size=(self.butSize, self.butSize))
        self.but8 = wx.Button(self, size=(self.butSize, self.butSize))
        self.but9 = wx.Button(self, size=(self.butSize, self.butSize))

        self.buttons = [self.but1, self.but2, self.but3,
                        self.but4, self.but5, self.but6,
                        self.but7, self.but8, self.but9]

        for but in self.buttons:
            but.Bind(wx.EVT_BUTTON, self.OnClick)
            but.Disable()
            self.gridSizer.Add(but)
            but.SetFont(wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))


        self.modeSizer = wx.StaticBoxSizer(wx.StaticBox(self, label = "Mode"), wx.VERTICAL)
        self.modeSizer.GetStaticBox().SetForegroundColour(self.textColour)

        self.signSizer = wx.StaticBoxSizer(wx.StaticBox(self, label = "Sign"), wx.VERTICAL)
        self.signSizer.GetStaticBox().SetForegroundColour(self.textColour)

        self.PvP = wx.CheckBox(self, size=self.cSize, id = 1, label="Player vs Player")
        self.AI = wx.CheckBox(self, size=self.cSize, id = 2, label="Player vs Computer")
        self.Play = wx.Button(self, label = "PLAY", size=(20, 30))

        self.X = wx.CheckBox(self, size=self.cSize, label="X")
        self.O = wx.CheckBox(self, size=self.cSize, label="O")

        self.PvP.Bind(wx.EVT_CHECKBOX, self.OnMode)
        self.AI.Bind(wx.EVT_CHECKBOX, self.OnMode)
        self.Play.Bind(wx.EVT_BUTTON, self.OnPlay)
        self.Play.SetFocus()

        self.X.Bind(wx.EVT_CHECKBOX, self.OnSign)
        self.O.Bind(wx.EVT_CHECKBOX, self.OnSign)


        self.modeSizer.Add(self.PvP)
        self.modeSizer.Add(self.AI)
        self.signSizer.Add(self.X)
        self.signSizer.Add(self.O)
        self.ctrlSizer.Add(self.modeSizer)
        self.ctrlSizer.Add(self.signSizer)
        self.ctrlSizer.Add(self.Play, flag=wx.EXPAND)
        self.ctrlSizer.Add(0, 30, 0)
        self.ctrlSizer.Add(self.winnerDisplay, flag=wx.ALIGN_LEFT)

        self.mainSizer.Add(30, 0, 0)
        self.mainSizer.Add(self.gridSizer, flag = wx.ALIGN_CENTER)
        self.mainSizer.Add(30, 0, 0)
        self.mainSizer.Add(self.ctrlSizer, flag = wx.ALIGN_CENTER)
        self.SetSizer(self.mainSizer)

        self.turn = 0
        self.sign1 = ''
        self.sign2 = ''

    def RAI(self):
        sleep(0.5)
        while True:
            i = random.choice(self.buttons)
            if i.Label == "":
                i.Label = self.sign2
                i.Disable()
                break

    def OnClick(self, event):
        but = event.EventObject

        if self.mode == 1:
            if self.turn % 2 == 0:
                but.Disable()
                but.Label = self.sign1
            else:
                but.Disable()
                but.Label = self.sign2
        elif self.mode == 2:
            but.Disable()
            but.Label = self.sign1
            MyPanel.RAI(self)

        self.turn += 1
        MyPanel.Win(self, event)

    def OnPlay(self, event):
        if self.mode != 0 and self.sign1 != self.sign2:
            if self.Play.Label == "PLAY":
                MyPanel.ActivateBut(self)
                self.Play.Label = "REPEAT"
            elif self.Play.Label == "REPEAT":
                self.winnerDisplay.Label = ""
                self.turn = 0
                MyPanel.ActivateCheckBox(self)
                MyPanel.ResetButLabels(self)
                MyPanel.ActivateBut(self)

            if self.mode == 2 and self.sign1 == "O":
                MyPanel.RAI(self)
        print("mode:", self.mode)
        print("sign1:", self.sign1)
        print("sign2:", self.sign2)

    def Win(self, event):
        b = [[self.but1.Label, self.but2.Label, self.but3.Label],
              [self.but4.Label, self.but5.Label, self.but6.Label],
              [self.but7.Label, self.but8.Label, self.but9.Label]]

        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != ""\
            or b[0][i] == b[1][i] == b[2][i] != ""\
            or b[0][0] == b[1][1] == b[2][2] != ""\
            or b[2][0] == b[1][1] == b[0][2] != "":
                self.winnerDisplay.Label = "  " + event.EventObject.Label + " is winner"
                MyPanel.DeactivateBut(self)
                break

    def OnMode(self, event):
        if self.PvP.GetValue() != self.AI.GetValue():
            self.mode = event.EventObject.Id
        elif self.PvP.GetValue() == self.AI.GetValue():
            if event.EventObject == self.PvP:
                self.AI.SetValue(False)
            else:
                self.PvP.SetValue(False)
            self.mode = event.EventObject.Id
    def OnSign(self, event):
        if self.X.GetValue() != self.O.GetValue():
            self.sign1 = event.EventObject.Label
        elif self.X.GetValue() == self.O.GetValue():
            if event.EventObject == self.X:
                self.O.SetValue(False)
            else:
                self.X.SetValue(False)
            self.sign1 = event.EventObject.Label
        if self.sign1 == "X":
            self.sign2 = "O"
        else:
            self.sign2 = "X"

    def ActivateBut(self):
        for i in self.buttons:
            i.Enable(True)

    def DeactivateBut(self):
        for i in self.buttons:
            i.Disable()

    def ActivateCheckBox(self):
        self.PvP.Enable(True)
        self.AI.Enable(True)
        self.X.Enable(True)
        self.O.Enable(True)

    def DeactivateCheckBox(self):
        self.PvP.Disable()
        self.AI.Disable()
        self.X.Disable()
        self.O.Disable()

    def ResetButLabels(self):
        for i in self.buttons:
            i.SetLabel=""


class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title, size=(600, 400))
        self.panel = MyPanel(self)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Calculator")
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()