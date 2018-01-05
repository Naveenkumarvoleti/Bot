import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.scale = tk.Scale(self, orient="horizontal", 
                              from_=0, to=600, 
                              showvalue=False,
                              command=self._on_scale)
        self.scale_label = tk.Label(self, text="")
        self.scale.pack(side="top", fill="x")
        self.scale_label.pack(side="top")

    def _on_scale(self, value):
        value = int(value)
        minutes = value/60
        seconds = value%60
        self.scale_label.configure(text="%2.2d:%2.2d" % (minutes, seconds))

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True);
    root.mainloop()
