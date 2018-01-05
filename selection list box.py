
from tkinter import *
from tkinter import ttk

win=Tk()
f=Frame(win)
b1=Button(f,text = "Let's Make Drink..")
l= Label(win,text="HI...")
v=StringVar()
v.set("Enter a recipe..")
e= Entry(win,textvariable=v)
e.pack()
v.get()
b1.pack()
l.pack()
f.pack()
def display_files():
    main = Tk()
    main.title("Multiple Choice Listbox")
    main.geometry("+50+150")
    frame = ttk.Frame(main, padding=(3, 3, 12, 12))
    frame.grid(column=0, row=0, sticky=(N, S, E, W))

    valores = StringVar()
    valores.set("Whiskey Rum Gin orangeJuice Lemonade Soda")

    lstbox = Listbox(frame, listvariable=valores, selectmode=MULTIPLE, width=20, height=10)
    lstbox.grid(column=0, row=0, columnspan=2)

    def select():
        reslist = list()
        seleccion = lstbox.curselection()
        for i in seleccion:
            entrada = lstbox.get(i)
            reslist.append(entrada)
        for val in reslist:
            print(val)

    btn = ttk.Button(frame, text="Choices", command=select)
    btn.grid(column=1, row=1)
b1.configure(command= display_files)
