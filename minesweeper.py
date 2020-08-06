import wx
import random
from datetime import datetime

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        # САЙЗЕРЫ
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.gsizer = wx.GridSizer(10, 10, 1, 1)
        self.csizer = wx.BoxSizer(wx.HORIZONTAL)

        [self.gsizer.Add(wx.Button(self, size=(50, 50), id=i), flag=wx.EXPAND) for i in range(100)]
        self.BindCells()

        ## РАЗМЕРНОСТЬ
        self.text_dmns = wx.StaticText(self, label="Dimension")
        self.x = wx.TextCtrl(self, value = "10", size=(30, 20))
        self.y = wx.TextCtrl(self, value = "10", size=(30, 20))
        self.x.Bind(wx.EVT_TEXT, self.xentry)
        self.y.Bind(wx.EVT_TEXT, self.yentry)

        self.dmns = wx.BoxSizer(wx.HORIZONTAL)
        self.dmns.Add(self.x)
        self.dmns.Add(5, 0, 0)
        self.dmns.Add(self.y)

        self.settings = wx.Button(self, label="settings", size=(309, 25))

        self.settings.Bind(wx.EVT_BUTTON, self.OnSet)



        # УРОВНИ
        self.text_difficult = wx.StaticText(self, label="SetMines")
        self.difficult = wx.ComboBox(self, value = "1", choices="1 2 3 4 5 6 7".split())

        self.difficult.Bind(wx.EVT_TEXT, self.SetMines)



        self.csizer.Add(self.text_dmns)
        self.csizer.Add(5, 0, 0)
        self.csizer.Add(self.dmns)
        self.csizer.Add(20, 0, 0)
        self.csizer.Add(self.text_difficult)
        self.csizer.Add(5, 0, 0)
        self.csizer.Add(self.difficult)

        self.sizer.Add(self.settings, flag=wx.CENTER)
        self.sizer.Add(0, 10, 0)
        self.sizer.Add(self.csizer, flag=wx.CENTER)
        self.sizer.Add(0, 5, 0)
        self.sizer.Add(self.gsizer, flag=wx.CENTER)

        self.sizer.Hide(self.csizer)
        #self.display = wx.StaticText(self, label="LOL")
        #self.sizer.Add(self.display)

        self.SetSizer(self.sizer)

        self.SetMines(self)
        self.SetCells()



    firstTurn = True
    Mines = {}
    MinesCount = 0

    cells = []
    left = []
    right = []
    top = []
    bottom = []
    edges = []
    flags = {}

    textColour = wx.Colour(150, 150, 150, 100)

    def OnBut(self, event):
        cell = event.EventObject

        self.OnCell(cell)


    def OnCell(self, cell):
        #sleep(0.01)
        if self.Mines[cell.Id]:
            if self.firstTurn:
                self.Mines[cell.Id] = False

                for i in range(self.gsizer.GetItemCount()):
                    d = random.randint(0, self.gsizer.GetItemCount()-1)
                    if not self.Mines[d]:
                        self.Mines[d] = True
                        break
            self.firstTurn = False

        if self.isBomb(cell):
            self.TheEnd()
        else:
            self.isBombAround(cell)


    def isBomb(self, cell):
        cell.Disable()
        if self.Mines[cell.Id]:
            cell.SetBackgroundColour(wx.Colour(178, 34, 34))
            return True
        else:
            cell.SetBackgroundColour(wx.Colour(170, 170, 170))

            return False

    def isBombAround(self, cell):
        id = cell.Id
        y = 0
        x = 0
        count = 0

        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j] == id:
                    y = i
                    x = j
                    break

        if id in self.right:
            for i in [self.Mines[self.cells[y-1][x]],
            self.Mines[self.cells[y+1][x]],
            self.Mines[self.cells[y][x-1]],
            self.Mines[self.cells[y-1][x-1]],
            self.Mines[self.cells[y+1][x-1]]]:
                if i: count += 1
        elif id in self.left:
            for i in [self.Mines[self.cells[y-1][x]],
            self.Mines[self.cells[y+1][x]],
            self.Mines[self.cells[y][x+1]],
            self.Mines[self.cells[y-1][x+1]],
            self.Mines[self.cells[y+1][x+1]]]:
                if i:
                    count += 1

        elif id in self.top:
            for i in [self.Mines[self.cells[y+1][x]],
            self.Mines[self.cells[y][x+1]],
            self.Mines[self.cells[y][x-1]],
            self.Mines[self.cells[y+1][x+1]],
            self.Mines[self.cells[y+1][x-1]]]:
                if i:
                    count += 1

        elif id in self.bottom:
            for i in [self.Mines[self.cells[y-1][x]],
            self.Mines[self.cells[y][x+1]],
            self.Mines[self.cells[y][x-1]],
            self.Mines[self.cells[y-1][x-1]],
            self.Mines[self.cells[y-1][x+1]]]:
                if i:
                    count += 1

        elif id == 0:
            for i in [self.Mines[self.cells[y+1][x]],
            self.Mines[self.cells[y][x+1]],
            self.Mines[self.cells[y+1][x+1]]]:
                if i:
                    count += 1

        elif id == (self.gsizer.GetCols()-1):
            for i in [self.Mines[self.cells[y+1][x]],
            self.Mines[self.cells[y][x-1]],
            self.Mines[self.cells[y+1][x-1]]]:
                if i:
                    count += 1

        elif id == (self.gsizer.GetItemCount()-1):
            for i in [self.Mines[self.cells[y-1][x]],
            self.Mines[self.cells[y][x-1]],
            self.Mines[self.cells[y-1][x-1]]]:
                if i:
                    count += 1
        elif id == (self.gsizer.GetItemCount()-self.gsizer.GetCols()):
            for i in [self.Mines[self.cells[y-1][x]],
            self.Mines[self.cells[y][x+1]],
            self.Mines[self.cells[y-1][x+1]]]:
                if i:
                    count += 1

        else:
            for i in [self.Mines[self.cells[y-1][x]],
            self.Mines[self.cells[y+1][x]],
            self.Mines[self.cells[y][x+1]],
            self.Mines[self.cells[y][x-1]],
            self.Mines[self.cells[y-1][x-1]],
            self.Mines[self.cells[y-1][x+1]],
            self.Mines[self.cells[y+1][x+1]],
            self.Mines[self.cells[y+1][x-1]]]:
                if i:
                    count += 1
        if count == 0:
            self.GoAround(id, x, y)
        else:
            cell.SetLabel(str(count))

    def GoAround(self, id, x, y):
        if id in self.right:
            for i in [self.FindWindowById(self.cells[y - 1][x]),
                      self.FindWindowById(self.cells[y + 1][x]),
                      self.FindWindowById(self.cells[y][x - 1]),
                      self.FindWindowById(self.cells[y - 1][x - 1]),
                      self.FindWindowById(self.cells[y + 1][x - 1])]:
                if i.IsEnabled():
                    self.OnCell(i)
        elif id in self.left:
            for i in [self.FindWindowById(self.cells[y - 1][x]),
                      self.FindWindowById(self.cells[y + 1][x]),
                      self.FindWindowById(self.cells[y][x + 1]),
                      self.FindWindowById(self.cells[y - 1][x + 1]),
                      self.FindWindowById(self.cells[y + 1][x + 1])]:
                if i.IsEnabled():
                    self.OnCell(i)

        elif id in self.top:
            for i in [self.FindWindowById(self.cells[y + 1][x]),
                      self.FindWindowById(self.cells[y][x + 1]),
                      self.FindWindowById(self.cells[y][x - 1]),
                      self.FindWindowById(self.cells[y + 1][x + 1]),
                      self.FindWindowById(self.cells[y + 1][x - 1])]:
                if i.IsEnabled():
                    self.OnCell(i)

        elif id in self.bottom:
            for i in [self.FindWindowById(self.cells[y - 1][x]),
                      self.FindWindowById(self.cells[y][x + 1]),
                      self.FindWindowById(self.cells[y][x - 1]),
                      self.FindWindowById(self.cells[y - 1][x - 1]),
                      self.FindWindowById(self.cells[y - 1][x + 1])]:
                if i.IsEnabled():
                    self.OnCell(i)
        elif id == 0:
            for i in [self.FindWindowById(self.cells[y + 1][x]),
                      self.FindWindowById(self.cells[y][x + 1]),
                      self.FindWindowById(self.cells[y + 1][x + 1])]:
                if i.IsEnabled():
                    self.OnCell(i)
        elif id == (self.gsizer.GetCols() - 1):
            for i in [self.FindWindowById(self.cells[y + 1][x]),
                      self.FindWindowById(self.cells[y][x - 1]),
                      self.FindWindowById(self.cells[y + 1][x - 1])]:
                if i.IsEnabled():
                    self.OnCell(i)

        elif id == (self.gsizer.GetItemCount() - 1):
            for i in [self.FindWindowById(self.cells[y - 1][x]),
                      self.FindWindowById(self.cells[y][x - 1]),
                      self.FindWindowById(self.cells[y - 1][x - 1])]:
                if i.IsEnabled():
                    self.OnCell(i)

        elif id == (self.gsizer.GetItemCount() - self.gsizer.GetCols()):
            for i in [self.FindWindowById(self.cells[y - 1][x]),
                      self.FindWindowById(self.cells[y][x + 1]),
                      self.FindWindowById(self.cells[y - 1][x + 1])]:
                if i.IsEnabled():
                    self.OnCell(i)

        else:
            for i in [self.FindWindowById(self.cells[y - 1][x]),
                      self.FindWindowById(self.cells[y + 1][x]),
                      self.FindWindowById(self.cells[y][x + 1]),
                      self.FindWindowById(self.cells[y][x - 1]),
                      self.FindWindowById(self.cells[y - 1][x - 1]),
                      self.FindWindowById(self.cells[y - 1][x + 1]),
                      self.FindWindowById(self.cells[y + 1][x + 1])]:
                if i.IsEnabled():
                    self.OnCell(i)

    def SetMines(self, evt):
        self.firstTurn = True
        self.MinesCount = int(self.difficult.GetValue())


        self.MinesCount = int(((10+self.MinesCount*5)/100)*self.gsizer.GetItemCount())
        for i in range(self.gsizer.GetItemCount()):
            cell = self.FindWindowById(i)
            cell.Enable(True)
            cell.SetLabel('')
            cell.SetBackgroundColour(wx.Colour(220, 220, 220))
            #self.FindWindowById(i).SetBackgroundColour(wx.Colour(190, 190, 190))

        a = []
        for i in range(self.gsizer.GetItemCount()):
            self.Mines[i] = False
        while len(a) != self.MinesCount:
            d = random.randint(0, self.gsizer.GetItemCount()-1)
            if d in a:
                continue
            else:
                self.Mines[d] = True
                a.append(d)
        a.clear()
        self.SetCells()
        self.BindCells()


    def SetCells(self):
        self.cells.clear()
        self.right.clear()
        self.left.clear()
        self.top.clear()
        self.bottom.clear()
        self.edges.clear()
        for i in range(self.gsizer.GetRows()):
            self.cells.append([])

        c = 0
        for i in range(self.gsizer.GetItemCount()):
            if i != 0 and i % (self.gsizer.GetCols()) == 0:
                c += 1
            self.cells[c].append(i)

        for i in range(1, self.gsizer.GetRows()-1):
            self.left.append(self.cells[i][0])
            self.right.append(self.cells[i][-1])

        self.top = self.cells[0][1:-1]
        self.bottom = self.cells[-1][1:-1]
        self.edges = [self.cells[0][0], self.cells[0][-1],  self.cells[-1][0], self.cells[-1][-1]]
        for i in range(self.gsizer.GetItemCount()):
            self.flags[i] = False

    def xentry(self, x):
        x = self.x.GetValue()
        if x.isdigit():
            x = int(x)
            if 10 <= x <= 20:
                self.gsizer.Clear(True)
                self.gsizer.Layout()
                self.gsizer.SetCols(x)
                self.gsizer.Layout()
                for i in range(x * self.gsizer.GetRows()):
                    self.gsizer.Add(wx.Button(self, size=(40, 40), id=i), flag=wx.EXPAND)
                self.gsizer.Layout()
                self.BindCells()
                self.Layout()
                self.SetMines(self)
                self.SetCells()
                self.firstTurn = True

    def yentry(self, y):
        y = self.y.GetValue()
        if y.isdigit():
            y = int(y)
            if 10 <= y <= 20:
                self.gsizer.Clear(True)
                self.gsizer.Layout()
                self.gsizer.SetRows(y)
                self.gsizer.Layout()
                for i in range(y * self.gsizer.GetCols()):
                    self.gsizer.Add(wx.Button(self, size=(40, 40), id=i), flag=wx.EXPAND)
                self.gsizer.Layout()
                self.BindCells()
                self.Layout()
                self.SetMines(self)
                self.SetCells()
                self.firstTurn = True
    s = True
    def OnRight(self, evt):

        while self.s:
            for i in range(self.gsizer.GetItemCount()):
                if self.Mines[i]:
                    self.s = False

        cell = evt.EventObject
        id =  cell.Id
        if self.flags[id]:
            cell.Bind(wx.EVT_BUTTON, self.OnBut)
            cell.SetBackgroundColour(wx.Colour(200, 200, 200))
            self.flags[id] = False
            if self.Mines[id]:
                self.MinesCount += 1
        else:
            evt.EventObject.Unbind(wx.EVT_BUTTON)
            cell.SetBackgroundColour(wx.Colour(100, 210, 100))
            self.flags[id] = True
            if self.Mines[id]:
                self.MinesCount -= 1
                if self.MinesCount == 0:
                    self.Congr()
        print(self.MinesCount)


    def BindCells(self):
        for i in range(self.gsizer.GetItemCount()):
            cell = self.FindWindowById(i)
            cell.Bind(wx.EVT_BUTTON, self.OnBut)
            cell.Bind(wx.EVT_RIGHT_DOWN, self.OnRight)
            #cell.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
            #cell.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
            cell.SetWindowStyle(wx.BORDER_NONE)
            cell.SetBackgroundColour(wx.Colour(220, 220, 220))
            cell.SetFont(wx.Font(15, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))


    def TheEnd(self):
        for i in self.Mines.keys():
            if self.Mines[i]:
                self.isBomb(self.FindWindowById(i))
        wx.MessageBox(message='Game End')
        self.CellDeactivate()

    def Congr(self):
        for i in self.Mines.keys():
            if self.Mines[i]:
                self.isBomb(self.FindWindowById(i))
        wx.MessageBox(message='Congratc')
        self.CellDeactivate()

    def CellDeactivate(self):
        for i in range(self.gsizer.GetItemCount()):
            self.FindWindowById(i).Unbind(wx.EVT_BUTTON)

    def OnEnter(self, event):
        if not self.flags[event.EventObject.Id]:
            event.EventObject.SetBackgroundColour(wx.Colour(190, 190, 190))

    def OnLeave(self, event):
        if event.EventObject.GetLabel() == "":
            if not self.flags[event.EventObject.Id]:
                event.EventObject.SetBackgroundColour(wx.Colour(220, 220, 220))

    def OnSet(self, event):
        if self.sizer.IsShown(self.csizer):
            self.sizer.Hide(self.csizer)
        else:
            self.sizer.Show(self.csizer)
        self.sizer.Layout()

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 800))
        self.panel = MyPanel(self)

        #self.SetIcon(wx.Icon("homeicon.png"))



class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Another")
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()