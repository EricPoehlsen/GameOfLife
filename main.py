import tkinter as tk
from app import App

def main():
    app = tk.Tk()
    content = App(app)
    content.pack()
    app.mainloop()


if __name__ == "__main__":
    main()
