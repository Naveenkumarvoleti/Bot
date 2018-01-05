from tkinter import*
class MyCode:
    def __init__(self):
        self.lbox = Listbox(root, width=50)
        self.lbox.pack()
        menubar.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New Project')
        filemenu.add_command(label='Load Files...', command=self.OnLoad)
        filemenu.add_command(label='Exit', command=root.quit)
        root.config(menu=menubar)
        root.mainloop()
     
    def OnLoad(self):
        fileNames = askopenfilenames(filetypes=[('Split Files', '*')])
        print (fileNames)
root=Tk
root.mainloop()
MyCode(root)
