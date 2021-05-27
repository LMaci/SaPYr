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
        #self.tk.geometry("400x200")
        # LABELS
        minesS = Scale(self.tk, from_=5, to=30, orient=HORIZONTAL, label="Mine count")
        sizeS = Scale(self.tk, from_=5, to=30, orient=HORIZONTAL, label='Minefield size',command=lambda x: minesS.config(to=str((sizeS.get())*sizeS.get()/2)))
        sizeS.set(10)
        applyButton = Button(self.tk, height=2,bg="lime",text="GRAJ", command= lambda: self.startGame(sizeS.get(),minesS.get()))
        sizeS.pack()
        #sizeS.set(10)
        sizeS.pack(expand=True, fill="both")
        minesS.pack(expand=True, fill="both")
        # BUTTONS

        applyButton.pack(fill="x")
        print("OKNO")
        print(len(gc.get_objects()))

    def startGame(self,size,mines):
        game = Toplevel()
        game.geometry("500x500")
        print("SIZE: ",size,"\nMines: ",mines)
        self._SIZE = size
        self._MINE_COUNT = mines
        self._DEFUSED_MINES = 0
        self.generateMinefield(game)
        print(len(gc.get_objects()))

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
                    "discovered": False,
                    "obj": Button(gameWindow,height=1, width=2)
                }
                if x < self._SIZE and y < self._SIZE:
                    button["obj"].bind(LMB_CLICK, self.onClickWrapper(LMB_CLICK, x, y))
                    button["obj"].bind(RMB_CLICK, self.onClickWrapper(RMB_CLICK, x, y))
                    button["obj"].place(x=x*50,y=y*50,width=50,height=50)
                    #button["obj"].grid(row=y, column=x)
                    self.buttons[x][y] = button
        minecount = 0
        while minecount < self._MINE_COUNT:
            x = randint(0, self._SIZE - 1)
            y = randint(0, self._SIZE - 1)
            if self.buttons[x][y]["mine"] is False:
                self.buttons[x][y]["mine"] = True
                # print("Postawiono " + str(minecount+1) + " minę na: " + str(x) + " " + str(y))
                minecount += 1
                for row in range(3):
                    for column in range(3):
                        try:
                            self.buttons[x - 1 + row][y - 1 + column]["value"] += 1
                        except KeyError:
                            continue  # OUT OF BOUNDS
            else:
                print("Zdublowana mina: " + str(x) + " " + str(y))

        print("Minecount: " + str(minecount))

#MOUSE CLICKS LOGIC

    def onClickWrapper(self, click, x, y):
        if click == LMB_CLICK:
            return lambda Button: self.onLeftClick(self.buttons[x][y])
        elif click == RMB_CLICK:
            return lambda Button: self.onRightClick(self.buttons[x][y])

    def onLeftClick(self, button):
        print("LEWY")
        button["obj"]["state"] = DISABLED
        button["obj"].config(relief=SUNKEN)
        button["obj"].unbind("<Button-1>")
        button["obj"].unbind("<Button-3>")
        if button["mine"]:
            self.gameOver()
        else:
            button["obj"].config(text=button["value"])

    def onRightClick(self, button):
        print("PRAWY")
        if button["flagged"] is False:
            button["obj"].unbind("<Button-1>")
            button["obj"].config(text="P", bg="orange")
            button["flagged"] = True
            if button["mine"]:
                self._DEFUSED_MINES += 1
                print("ROZMINOWANY")
            else:
                print("PUDLO")
        elif button["flagged"] is True:
            button["obj"].bind(LMB_CLICK, self.onClickWrapper(LMB_CLICK, button["x"], button["y"]))
            button["obj"].config(text="", bg=window.cget("bg"))
            button["flagged"] = False
            if button["mine"]:
                self._DEFUSED_MINES -= 1
        print("DEFUSED: ", self._DEFUSED_MINES)

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

window = Tk()
window.title("SaPYr - Ustawienia gry")
window.geometry("300x150")
#window.resizable(False,False)
game = Game(window)
window.mainloop()