from tkinter import *
from random import randint
import gc

LMB_CLICK = "<Button-1>"
RMB_CLICK = "<Button-3>"


class Config:
    def __init__(self, tk):
        self.tk = tk
        self.setup()

    def setup(self):
        self.tk.title("Settings")

        mines_scale = Scale(self.tk, from_=5, to=30, orient=HORIZONTAL, label="Mine count")
        size_scale = Scale(self.tk, from_=5, to=30, orient=HORIZONTAL, label='Minefield size',
                           command=lambda x: mines_scale.config(to=str((size_scale.get()) * size_scale.get() / 2.5)))
        size_scale.set(10)
        apply_button = Button(self.tk, height=2, bg="lime", text="START",
                              command=lambda: self.start(size_scale.get(), mines_scale.get()))
        size_scale.pack(expand=True, fill="both")
        mines_scale.pack(expand=True, fill="both")

        apply_button.pack(fill="x")
        print(len(gc.get_objects()))

    def start(self, size, mines):
        new_game = Toplevel(self.tk)
        game = Game(new_game, size, mines)


class Game:
    def __init__(self, tk, size, mines):
        self.size = size
        self.mines = mines
        self.tk = tk
        self._DEFUSED_MINES = 0
        self._tiles_remaining = size*size-mines
        self.mine_list = []
        self.buttons = dict({})
        self.start_game(size, mines)

    def start_game(self, size, mines):
        self.tk.geometry(str(size*30)+"x"+str(size*30))
        self.tk.resizable(False, False)
        self.tk.title("SaPYr - Saper with Python")
        print("SIZE: ", size, "\nMines: ", mines)
        self.generate_minefield(self.tk)
        print(len(gc.get_objects()))

    def generate_minefield(self, game_window):
        val = 0
        for x in range(self.size):
            for y in range(self.size):
                if y == 0:
                    self.buttons[x] = {}
                button = {
                    "x": x,
                    "y": y,
                    "value": val,
                    "flagged": False,
                    "mine": False,
                    "obj": Button(game_window, height=1, width=2)
                }
                if x < self.size and y < self.size:
                    button["obj"].bind(LMB_CLICK, self.on_click_wrapper(LMB_CLICK, x, y))
                    button["obj"].bind(RMB_CLICK, self.on_click_wrapper(RMB_CLICK, x, y))
                    button["obj"].place(x=x*30, y=y*30, width=30, height=30)
                    self.buttons[x][y] = button
        _minecount = 0
        while _minecount < self.mines:
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            if self.buttons[x][y]["mine"] is False:
                self.buttons[x][y]["mine"] = True
                _minecount += 1
                self.mine_list.append(str(x)+str(y))
                for row in range(3):
                    for column in range(3):
                        try:
                            self.buttons[x - 1 + row][y - 1 + column]["value"] += 1
                        except KeyError:
                            continue  # OUT OF BOUNDS
            else:
                print("Zdublowana mina: " + str(x) + " " + str(y))

# # # # # # # # # # # #
# MOUSE CLICKS EVENTS
# # # # # # # # # # # #
    def on_click_wrapper(self, click, x, y):
        if click == LMB_CLICK:
            return lambda Button: self.on_left_click(self.buttons[x][y])
        elif click == RMB_CLICK:
            return lambda Button: self.on_right_click(self.buttons[x][y])

    def on_left_click(self, button):
        if button["obj"]["state"] == "disabled":
            return
        button["obj"]["state"] = DISABLED
        button["obj"].config(relief=SUNKEN)
        button["obj"].unbind("<Button-1>")
        button["obj"].unbind("<Button-3>")
        if button["mine"]:
            self.game_over()
        else:
            self._tiles_remaining -= 1
            button["obj"].config(text=button["value"])
            self.game_victory()

        if button["value"] == 0:
            for j in range(-1, 2):
                if 0 <= button["y"]+j < self.size:
                    for i in range(-1, 2):
                        if 0 <= button["x"] + i < self.size:
                            if (i == 0 and j == 0) or \
                                    self.buttons[int(button["x"])+i][int(button["y"])+j]["obj"]["state"] == "disabled":
                                continue
                            self.on_left_click(self.buttons[int(button["x"]) + i][int(button["y"]) + j])

    def on_right_click(self, button):
        if button["flagged"] is False:
            button["obj"].unbind("<Button-1>")
            button["obj"].config(text="P", bg="orange")
            button["flagged"] = True
            if button["mine"]:
                self._DEFUSED_MINES += 1
                self.game_victory()
        elif button["flagged"] is True:
            button["obj"].bind(LMB_CLICK, self.on_click_wrapper(LMB_CLICK, button["x"], button["y"]))
            button["obj"].config(text="", bg=self.tk.cget("bg"))
            button["flagged"] = False
            if button["mine"]:
                self._DEFUSED_MINES -= 1

# # # # # # # # # # # #
# WIN/LOSE CONDITIONS
# # # # # # # # # # # #
    def game_victory(self):
        if self._tiles_remaining == 0 and self._DEFUSED_MINES == self.mines:
            for x, y in self.mine_list:
                self.buttons[int(x)][int(y)]["obj"].unbind("<Button-3>")
                self.buttons[int(x)][int(y)]["obj"].config(bg="lime")
            win = Toplevel(self.tk)
            win.title("VICTORY!")
            l1 = Label(win, text="Victory! :)").pack()
            win.geometry("300x150")
            restart = Button(win, text="Restart", height=2, width=6).pack()

    def game_over(self):
        for x in range(self.size):
            for y in range(self.size):
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


root = Tk()
root.geometry("300x150")
root.resizable(False, False)
config = Config(root)
root.mainloop()
