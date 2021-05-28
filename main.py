from tkinter import *
from random import randint
import gc

LMB_CLICK = "<Button-1>"
RMB_CLICK = "<Button-3>"

class Game:
    buttons = dict({})
    _DEFUSED_MINES = 0
    _MINE_COUNT = 20
    _SIZE = 10

    def __init__(self,tk):
        self.tk = tk
        self.setup()

    def setup(self):
        self.tk.title("Settings")
        # LABELS
        minesS = Scale(self.tk, from_=5, to=30, orient=HORIZONTAL, label="Mine count")
        sizeS = Scale(self.tk, from_=5, to=30, orient=HORIZONTAL, label='Minefield size', command=lambda x: minesS.config(to=str((sizeS.get())*sizeS.get()/2)))
        sizeS.set(10)
        applyButton = Button(self.tk, height=2,bg="lime",text="START", command= lambda: self.startGame(sizeS.get(),minesS.get()))
        sizeS.pack(expand=True, fill="both")
        minesS.pack(expand=True, fill="both")

        # BUTTONS
        applyButton.pack(fill="x")
        print(len(gc.get_objects()))

    def startGame(self,size,mines):
        game = Toplevel()
        game.geometry(str(size*30)+"x"+str(size*30))
        game.resizable(False,False)
        game.title("SaPYr - Saper with Python")
        print("SIZE: ",size,"\nMines: ",mines)
        self._SIZE = size
        self._MINE_COUNT = mines
        self._DEFUSED_MINES = 0
        self.generateMinefield(game)
        print(len(gc.get_objects()))

#MOUSE CLICKS LOGIC

    def onClickWrapper(self, click, x, y):
        if click == LMB_CLICK:
            return lambda Button: self.onLeftClick(self.buttons[x][y])
        elif click == RMB_CLICK:
            return lambda Button: self.onRightClick(self.buttons[x][y])

    def cascade(self,x,y):
        print("X = ",x)
        print("Y = ",y)
        for i in [y-1, y, y+1]: #Y
            print("i = ",i)
            if i>=0:
                for j in [x-1, x, x+1]: #X
                    print("J = ",j)
                    if j>=0:
                        try:
                            self.onLeftClick(self.buttons[j][i])
                        except KeyError:
                            print(j," ",i," jest za planszą")
                            continue #OUT OF BOUNDS
                #print("X="+str(j) + " | Y=" + str(i))
             #   print(str(m) + " " + str(n))

    def onLeftClick(self, button):
        if button["obj"]["state"] == "disabled":
            return
        print("KLIKAM ",button["x"],button["y"]," o wartosci ",button["value"])
        button["obj"]["state"] = DISABLED
        button["obj"].config(relief=SUNKEN)
        button["obj"].unbind("<Button-1>")
        button["obj"].unbind("<Button-3>")
        if button["mine"]:
            self.gameOver()
        else:
            button["obj"].config(text=button["value"])

        if button["value"] == 0:
            for j in range(-1,2):
                if 0 <= button["y"]+j < self._SIZE:
                    for i in range(-1,2):
                        if 0 <= button["x"] + i < self._SIZE:
                            if (i==0 and j==0) or self.buttons[int(button["x"])+i][int(button["y"])+j]["obj"]["state"] == "disabled":
                                continue
                            self.onLeftClick(self.buttons[int(button["x"])+i][int(button["y"])+j])

    def onRightClick(self, button):
        if button["flagged"] is False:
            button["obj"].unbind("<Button-1>")
            button["obj"].config(text="P", bg="orange")
            button["flagged"] = True
            if button["mine"]:
                self._DEFUSED_MINES += 1
        elif button["flagged"] is True:
            button["obj"].bind(LMB_CLICK, self.onClickWrapper(LMB_CLICK, button["x"], button["y"]))
            button["obj"].config(text="", bg=window.cget("bg"))
            button["flagged"] = False
            if button["mine"]:
                self._DEFUSED_MINES -= 1

#GAME LOGIC

    def gameVictory(self):
        win = Toplevel(window)
        win.title("VICTORY!")
        l1 = Label(win, text="Victory!").pack()
        restart = Button(win, text="Restart", height=2, width=6).pack()
        print("OKNO")

    def gameOver(self):
        for x in range(self._SIZE):
            for y in range(self._SIZE):
                self.buttons[x][y]["obj"].config(text=self.buttons[x][y]["value"])
                if self.buttons[x][y]["mine"]:
                    if self.buttons[x][y]["flagged"]:
                        self.buttons[x][y]["obj"].config(text="P", bg="lime")
                    else:
                        self.buttons[x][y]["obj"].config(text="*", bg="red")
                self.buttons[x][y]["obj"]["state"] = DISABLED
                self.buttons[x][y]["obj"].config(relief=SUNKEN)
                self.buttons[x][y]["obj"].unbind("<Button-1>")
                self.buttons[x][y]["obj"].unbind("<Button-3>")

    def generateMinefield(self, gameWindow):
        val = 0
        for x in range(self._SIZE):
            for y in range(self._SIZE):
                if y == 0:
                    self.buttons[x] = {}
                button = {
                    "x": x,
                    "y": y,
                    "value": val,
                    "flagged": False,
                    "mine": False,
                    "obj": Button(gameWindow,height=1, width=2)
                }
                if x < self._SIZE and y < self._SIZE:
                    button["obj"].bind(LMB_CLICK, self.onClickWrapper(LMB_CLICK, x, y))
                    button["obj"].bind(RMB_CLICK, self.onClickWrapper(RMB_CLICK, x, y))
                    button["obj"].place(x=x*30,y=y*30,width=30,height=30)
                    self.buttons[x][y] = button
        _minecount = 0
        while _minecount < self._MINE_COUNT:
            x = randint(0, self._SIZE - 1)
            y = randint(0, self._SIZE - 1)
            if self.buttons[x][y]["mine"] is False:
                self.buttons[x][y]["mine"] = True
                _minecount += 1
                for row in range(3):
                    for column in range(3):
                        try:
                            self.buttons[x - 1 + row][y - 1 + column]["value"] += 1
                        except KeyError:
                            continue  # OUT OF BOUNDS
            else:
                print("Zdublowana mina: " + str(x) + " " + str(y))

        print("Minecount: " + str(_minecount))

window = Tk()
window.geometry("300x150")
window.resizable(False,False)
game = Game(window)
window.mainloop()