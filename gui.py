from tkinter import*
import os,glob


win=Tk()
f=Frame(win)
b1=Button(f,text = "Let's Make Drink")
##b2=Button(f,text = "MENU")
##b3 = Button(f,text = "Configure")
l= Label(win,text="HI...")

v=StringVar()
v.set("Enter a recipe..")
e= Entry(win,textvariable=v)
e.pack()
v.get()
b1.pack()
##b2.pack(side = LEFT,padx=10,pady=20)
##b3.pack(side = RIGHT,padx= 10,pady =20)
l.pack()
f.pack()
def Readfile():
    os.chdir(".")
    for file in glob.glob("*.json"):
        print(file)
b1.configure(command =Readfile)
def display_menu():
    e.pack_forget()
    f.pack_forget()
    f.grid_forget()
    b4 = Button(win,text ="RICE")
    b5=Button(win,text ="CURRY")
    b6=Button(win,text="FRY")
    b4.pack(side=LEFT,padx= 10,pady=10)
    b5.pack(side= LEFT,padx = 10,pady=10)
    b6.pack(side= LEFT, padx= 10,pady=10)
    b5.configure(command= display_files)
    
def display_files():
    f.pack_forget()
    sb = Scrollbar(win,orient=VERTICAL)
    sb.pack(side=RIGHT,fill=Y)
    lb = Listbox(win, height=3)
    lb.pack()
    lb.insert(END,"first entry")
    lb.insert(END,"second entry")
    lb.insert(END,"third entry")
    lb.insert(END,"fourth entry")
    sb.configure(command=lb.yview)
    lb.configure(yscrollcommand=sb.set)
    
b1.configure(command= display_menu)

