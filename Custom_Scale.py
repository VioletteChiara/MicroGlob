from tkinter import *

class CustomScale(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self,0,weight=1)
        Grid.columnconfigure(self, 1, weight=100)
        Grid.columnconfigure(self, 0, weight=1)

        self.left_button = Button(self, text="<", command=self.decrease)
        self.left_button.grid(sticky="se", row=0, column=0)

        self.scale = Scale(self, **kwargs)
        self.scale.grid(sticky="nwse", row=0, column=1)


        self.right_button = Button(self, text=">", command=self.increase)
        self.right_button.grid(sticky="sw", row=0, column=2)

    def decrease(self):
        current_value = self.scale.get()
        if self.scale.cget('from')<self.scale.cget('to'):
            new_value = max(self.scale.cget('from'), current_value - 1)
        else:
            new_value = min(self.scale.cget('from'), current_value + 1)
        self.scale.set(new_value)

    def increase(self):
        current_value = self.scale.get()
        if self.scale.cget('from') < self.scale.cget('to'):
            new_value = min(self.scale.cget('to'), current_value + 1)
        else:
            new_value = max(self.scale.cget('to'), current_value - 1)
        self.scale.set(new_value)


