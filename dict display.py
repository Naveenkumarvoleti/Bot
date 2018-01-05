from tkinter import *

data = {'parakeet': ['fly', 'bird'], 'dog': 'animal', 'cat': 'feline'}
x=[]
root = Tk()
x=list(data.keys())
Label(root, text = x ).grid(row=1,ipadx = 10,ipady = 50)
    
mainloop()
