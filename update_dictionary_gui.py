from tkinter import *
import glob,os
global fL 
fL = {}
global x
global y
win = Tk()
win.title("Olly")
f= Frame(win)
l= Label(win,text = "HI...")
b1= Button(f,text = "Let's Make Drink")
b1.pack()
##b2 = Button(f,text = "Bottle update")
##b2.pack()
l.pack()
f.pack()
global file
def Readfile():
    os.chdir(".")
    for file in glob.glob("*.json"):
        global data
        data = file
        print(file)
        
def display_menu():
    win1 = Tk()
    win1.title("Olly")
    b4 = Button(win1,text ="Select Drink")
    b5=Button(win1,text ="Bottle update")
    b6 =Button(win1,text = "Random")
    b4.pack(side=LEFT,padx= 10,pady=10)
    b5.pack(side= LEFT,pady=10)
    b6.pack(side =RIGHT,padx=10,pady=10)
    b5.configure(command= bottle_update)
    b4.configure(command = display_files)
    b6.configure(command = random_drink)
def commando(x, y):
 try:
    bottle_dict.update({x:int(y)})
 except ValueError:
    print(fL)
    
def display_files():
    win3=Tk()
    win3.title("Olly")
    sb = Scrollbar(win3,orient=VERTICAL)
    sb.pack(side=RIGHT,fill=Y)
    lb = Listbox(win3, height=3)
    lb.pack()
    lb.insert(END,"vesper")
    lb.insert(END,"second entry")
    lb.insert(END,"third entry")
    lb.insert(END,"fourth entry")
    sb.configure(command=lb.yview)
    lb.configure(yscrollcommand=sb.set)
    b6=Button(win3,text="select")
    b6.configure(command = lambda :run(lb.get(ACTIVE)))
    b6.pack()

    
def bottle_update():
    root = Tk()
    root.title("Olly")

    x = StringVar()  # Creating the variables that will get the user's input.
    y = StringVar()

    label_1 = Label(root, text="Enter ingredient name: ")
    label_2 = Label(root, text="select bottle, 1-6:")
    entry_1 = Entry(root, textvariable=x)
    entry_2 = Entry(root, textvariable=y)

    label_1.grid(row=1)
    label_2.grid(row=3)

    entry_1.grid(row=2, column=0)
    entry_2.grid(row=4, column=0)
    but = Button(root, text="select", command=lambda :commando(x.get(), y.get()))
    but.grid(row=5, column=0)
    root.mainloop()

def random_drink():
    global win4
    win4 =Tk()
    win4.title("select drink levels")
    l1=Label(win4,text = "GIN")
    l2=Label(win4,text = "VODKA")
    l3=Label(win4,text = "SODA")
    l4=Label(win4,text = "RUM")
    l5 = Label(win4,text = "Do you want ice")
    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)
    l3.grid(row=3, column=0)
    l4.grid(row=4, column=0)
    l5.grid(row=5, column = 0)
    butt = Button(win4,text = "MAKE",command = lambda : make_drink(amt1.get(),amt2.get(),amt3.get(),amt4.get()))
    butt.grid(row=6, column=2)

    slct = StringVar(win4)
    choices = {'Yes','No'}
    popupmenu = OptionMenu(win4,slct,*choices)
    amt1 = Scale(win4,from_ =0,to= 12,orient = HORIZONTAL,resolution = 1)
    amt1.grid(row=1, column=2)
    amt2 = Scale(win4,from_ =0,to= 12,orient = HORIZONTAL,resolution = 1)
    amt2.grid(row=2, column=2)
    amt3 = Scale(win4,from_ =0,to= 12,orient = HORIZONTAL,resolution = 1)
    amt3.grid(row=3, column=2)
    amt4 = Scale(win4,from_ =0,to= 12,orient = HORIZONTAL,resolution = 1)
    amt4.grid(row=4, column=2)
    popupmenu.grid(row = 5,column = 2)
def make_drink(p,q,r,s):
    win5 =Tk()
    win5.title("Olly")
    label = Label(win5,text= "Making...")
    label.pack()
b1.configure(command = display_menu)
win.mainloop()
