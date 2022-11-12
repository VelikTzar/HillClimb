import tkinter as tk
from tkinter import messagebox


class Messagebox:
    def __init__(self, text):
        self.window = tk.Tk()
        self.window.wm_withdraw()
        self.messagebox = tk.messagebox.askquestion('Play again', text)
        self.game = game

        if self.messagebox == 'yes':
            self.window.destroy()
        else:
            tk.messagebox.showinfo('Return', 'You will now return to the application screen')



