from tkinter import *

fL = {"gin" : 5}

def commando(x, y):
    for k,v in list(fL.items()):
            if v == int(y):
               del fL[k]
               print (fL)
    fL.update({x:int(y)})  # Please note that these x and y vars are private to this function.  They are not the x and y vars as defined below.
    print(fL)

root = Tk()
root.title("Spam Words")

x = StringVar()  # Creating the variables that will get the user's input.
y = StringVar()

label_1 = Label(root, text="Say a word: ")
label_2 = Label(root, text="Give it a value, 1-6:")
entry_1 = Entry(root, textvariable=x)
##entry_2 = Entry(root, textvariable=y)
slct = StringVar(root)
slct.set("select")
choices = {'1','2','3','4','5','6'}
popupmenu = OptionMenu(root,slct,*choices)
popupmenu.grid(row = 4)
label_1.grid(row=1)
label_2.grid(row=3)

entry_1.grid(row=2, column=0)
##entry_2.grid(row=4, column=0)

but = Button(root, text="Execute", command=lambda :commando(x.get(), slct.get()))  # Note the use of lambda and the x and y variables.
but.grid(row=5, column=0)

root.mainloop()
