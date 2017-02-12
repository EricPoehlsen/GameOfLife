import tkinter as tk
import random


class App(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app)
        self.grid = tk.StringVar()
        self.time = tk.StringVar()
        self.percent = tk.StringVar()
        self.time.set("250")
        self.grid.set("25")
        self.percent.set("0.35")
        self.canvas = tk.Canvas(self)
        self.play = 0
        self.rows = int(self.grid.get())
        self.cols = int(self.grid.get())
        self.step = int(self.time.get())
        self.array = self.createArray(self.rows, self.cols)
        self.showContent()

    def showContent(self):
        self.makeMenu()

        self.canvas.config(width=500, height=500)
        self.canvas.pack()

    def makeMenu(self):
        frame = tk.Frame(self)
        play_button = tk.Button(
            frame,
            text="Start",
            width=6
        )
        play_button.bind("<Button-1>", self.toggleGame)
        play_button.pack(side=tk.LEFT, anchor=tk.W)

        grid_label = tk.Label(frame, text="Dimensions: ")
        grid_label.pack(side=tk.LEFT, anchor=tk.W)

        grid_entry = tk.Entry(
            frame,
            width=5,
            textvariable=self.grid,
        )
        grid_entry.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)

        time_label = tk.Label(
            frame,
            text="Time per cycle:",
        )
        time_label.pack(side=tk.LEFT, anchor=tk.W)

        time_entry = tk.Entry(
            frame,
            width=5,
            textvariable=self.time,
        )
        time_entry.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)

        percent_label = tk.Label(
            frame,
            text="Fraction alive: ",
        )
        percent_label.pack(side=tk.LEFT, anchor=tk.W)

        percent_entry = tk.Entry(
            frame,
            width=5,
            textvariable=self.percent,
        )
        percent_entry.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)

        frame.pack(fill=tk.X)

    def drawArray(self):
        self.canvas.delete(tk.ALL)
        x_dim = self.canvas.winfo_reqwidth() / self.rows
        y_dim = self.canvas.winfo_reqheight() / self.cols

        for row in range(self.rows):
            for col in range(self.cols):
                alive = self.array[col][row]

                if alive:
                    color = "#009900"
                else:
                    color = "#ffffff"

                self.canvas.create_rectangle(
                    col * x_dim,
                    row * y_dim,
                    col * x_dim + x_dim,
                    row * y_dim + y_dim,
                    fill=color
                )
        self.update_idletasks()

    def updateArray(self):
        def checkAlive(row, col):
            left = col - 1
            top = row - 1
            right = col + 1
            down = row + 1

            if left < 0: left = self.cols - 1
            if top < 0: top = self.rows - 1
            if right >= self.cols: right = 0
            if down >= self.rows: down = 0

            neighbors = (
                self.array[left][row]
                + self.array[left][top]
                + self.array[col][top]
                + self.array[right][top]
                + self.array[right][row]
                + self.array[right][down]
                + self.array[col][down]
                + self.array[left][down]
            )

            was_alive = self.array[col][row]

            if was_alive and 2 <= neighbors <= 3:
                alive = 1
            elif neighbors > 2 and not was_alive:
                alive = 1
            else:
                alive = 0
            return alive

        new_array = []
        for col in range(self.cols):
            line = []
            for row in range(self.rows):
                line.append(checkAlive(row, col))
            new_array.append(line)

        self.array = new_array
        self.drawArray()

    def toggleGame(self, event):
        if self.play == 1:
            self.play = 0
            event.widget.config(text="Start")
        else:
            try:
                self.rows = int(self.grid.get())
                self.cols = int(self.grid.get())
                self.step = int(self.time.get())
                self.play = 1
                event.widget.config(text="Stop")
                self.array = self.createArray(self.cols, self.rows)
            except ValueError:
                pass

            self.cycle()

    def cycle(self):
        self.updateArray()
        if self.play:
            self.after(self.step, self.cycle)

    def createArray(self,cols, lines):
        array = []
        for line in range(lines):
            line = []
            for col in range(cols):
                value = random.random()
                try:
                    perc_string = self.percent.get()
                    perc_string = perc_string.replace(",", ".")
                    percent = float(perc_string)
                    if 1 < percent <= 100:
                        percent /= 100
                except ValueError:
                    percent = 0.35

                if value >= percent:
                    value = 0
                else:
                    value = 1

                line.append(value)
            array.append(line)
        return array

