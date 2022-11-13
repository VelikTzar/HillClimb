import tkinter as tk
from tkinter import messagebox


class Messagebox:
    def __init__(self, game, title, text):
        self.messagebox = None
        self.window = tk.Tk()
        self.window.wm_withdraw()
        self.game = game
        self.title = title
        self.text = text

    def run(self):
        self.messagebox = tk.messagebox.askquestion(self.title, self.text)
        if self.messagebox == 'yes':
            self.window.destroy()
        else:
            tk.messagebox.showinfo('')
            self.window.destroy()


class EscapeMessageBox(Messagebox):
    def __init__(self, game):
        self.title = 'Escape'
        self.text = 'Do you want to return to the main menu?'
        super().__init__(game, self.title, self.text)

    def run(self):
        self.messagebox = tk.messagebox.askquestion(self.title, self.text)
        if self.messagebox == 'yes':
            tk.messagebox.showinfo('Main menu', 'You will now go to the main menu')
            self.window.destroy()
            self.game.done = True
        else:
            tk.messagebox.showinfo('Return', 'You will now return to the game')
            self.window.destroy()


class OutcomeMessageBox(Messagebox):
    def __init__(self, game, title):
        self.title = title
        self.text = 'Do you want to play again?'
        super().__init__(game, self.title, self.text)


    def run(self):
        self.messagebox = tk.messagebox.askquestion(self.title, self.text)
        if self.messagebox == 'yes':
            tk.messagebox.showinfo('Return', 'You will now return to the game')
            self.window.destroy()
            self.game.done = True
            self.game.app.playing = True
        else:
            tk.messagebox.showinfo('Leave', 'You will now leave the game')
            self.window.destroy()
            self.game.done = True
            self.game.app.running = False


class LossMessageBox(OutcomeMessageBox):
    def __init__(self, game):
        self.title = 'You lost.'
        super().__init__(game, self.title)


class VictoryMessageBox(OutcomeMessageBox):
    def __init__(self, game):
        self.title = 'You won. Congratulations!'
        super().__init__(game, self.title)



