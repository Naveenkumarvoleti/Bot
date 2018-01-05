from tkinter import *
from tkinter import ttk
import glob,os
import threading


try:
      global win
      win = Tk()
      win.minsize(width=480, height=320)
      win.title("Olly")
      f= Frame(win)
      l= Label(win,text = "HI...")
      b1= Button(f,text = "Let's Make Drink")
      b1.pack()
    ##b2 = Button(f,text = "Bottle update")
    ##b2.pack()
      l.pack()
      f.pack()
      
      def progress_bar():
        root = Tkinter.Tk()
        fb = ttk.Frame()
        fb.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
        pb_vd = ttk.Progressbar(fb, orient='vertical', mode='determinate')
        pb_vd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)
        pb_vd.start(50)
        
      def Readfile():
          os.chdir(".")
          for file in glob.glob("*.json"):
              print(file)
              
      def display_menu():
          f.pack_forget()
          f.grid_forget()
          l.pack_forget()
          win.title("Olly")
          global b4
          global b5
          global b6
          global b7
          b4 = Button(win,text ="Select Drink")
          b5 = Button(win,text ="Bottle update")
          b6 = Button(win,text = "Create")
          b7=Button(win,text="single")
          b4.pack(side=TOP,padx= 10,pady=10)
          b5.pack(side= TOP,pady=10,padx=10)
          b6.pack(side =TOP,padx=10,pady=10)
          b7.pack(side =TOP,padx=10,pady=10)
          b5.configure(command= bottle_update)
          b4.configure(command = display_files)
          b6.configure(command = create_drink)
          b7.configure(command = seperate_drink)
      def commando(x,y):
          bottle_dict.update({x:int(y)})
          print(bottle_dict)

      def display_files():
          b4.pack_forget()
          b5.pack_forget()
          b6.pack_forget()
          b7.pack_forget()
          win.title("Olly")
          sb = Scrollbar(win,orient=VERTICAL)
          sb.pack(side=RIGHT,fill=Y)
          lb = Listbox(win, height=3)
          lb.pack()
          lb.insert(END,"vesper.json")
          lb.insert(END,"second entry")
          lb.insert(END,"third entry")
          lb.insert(END,"fourth entry")
          sb.configure(command=lb.yview)
          lb.configure(yscrollcommand=sb.set)
          b8=Button(win,text="select")
          b8.configure(command = lambda :run(lb.get(ACTIVE)))
          b8.pack()
##          b7=Button(win,text="back",command= display_menu)
##          b7.pack()


      def bottle_update():
          b4.pack_forget()
          b5.pack_forget()
          b6.pack_forget()
          b7.pack_forget()
          win.title("Olly")

          x = StringVar()  # Creating the variables that will get the user's input.
          y = StringVar()

          label_1 = Label(win, text="Enter ingredient name: ")
          label_2 = Label(win, text="select bottle, 1-6:")
          entry_1 = Entry(win, textvariable=x)
          entry_2 = Entry(win, textvariable=y)

          label_1.grid(row=1)
          label_2.grid(row=3)

          entry_1.grid(row=2, column=0)
          entry_2.grid(row=4, column=0)
          but = Button(win, text="select", command=lambda :commando(x.get(), y.get()))
          but.grid(row=5, column=0)
          
      def create_drink():
          b4.pack_forget()
          b5.pack_forget()
          b6.pack_forget()
          b7.pack_forget()
          win.title("select drink levels")
          l1=Label(win,text = "GIN")
          l2=Label(win,text = "VODKA")
          l3=Label(win,text = "SODA")
          l4=Label(win,text = "RUM")
          l5 = Label(win,text = "Do you want ice")
          l1.grid(row=1, column=0)
          l2.grid(row=2, column=0)
          l3.grid(row=3, column=0)
          l4.grid(row=4, column=0)
          l5.grid(row=5, column = 0)
          butt = Button(win,text = "MAKE",command = lambda : make(amt1.get(),amt2.get(),amt3.get(),amt4.get()))
          butt.grid(row=6, column=2)

          slct = StringVar(win)
          choices = {'Yes','No'}
          popupmenu = OptionMenu(win,slct,*choices)
          amt1 = Scale(win,from_ =0,to= 12,orient = HORIZONTAL,resolution = 1)
          amt1.grid(row=1, column=2)
          amt2 = Scale(win,from_ =0,to= 12,orient = HORIZONTAL,resolution = 1)
          amt2.grid(row=2, column=2)
          amt3 = Scale(win,from_ =0,to= 12,orient = HORIZONTAL,resolution = 1)
          amt3.grid(row=3, column=2)
          amt4 = Scale(win,from_ =0,to= 12,orient = HORIZONTAL,resolution = 1)
          amt4.grid(row=4, column=2)
          popupmenu.grid(row = 5,column = 2)

      def _on_scale(self, value):
              value = int(value)
              minutes = value/60
              seconds = value%60
              scale_label.configure(text="%2.2d:%2.2d" % (minutes, seconds))
              
      def seperate_drink():
              b4.pack_forget()
              b5.pack_forget()
              b6.pack_forget()
              b7.pack_forget()
              win.title("Olly")
              l6=Label(win,text="select drink")
              l7=Label(win,text="select amount")
              l8=Label(win,text="start time")
              selct = StringVar(win)
              amt5=Scale(win,from_=0,to= 12,orient=HORIZONTAL,resolution=1)
              amt6=Scale(win,from_=0,to= 600,orient=HORIZONTAL)
              selection= {"whiskey","rum","vodka","gin","soda","lilletblonde"}
              optionmenu = OptionMenu(win,selct,*selection)
              selct.set("select")
              optionmenu.grid(row=1,column=2)
              b9=Button(win,text="start process",command = lambda : single(selct.get(),amt5.get(),amt6.get()))
              b9.grid(row=5,column=2)
              l6.grid(row=1,column=1)
              amt5.grid(row=2,column=2)
              l7.grid(row=2,column=1)
              l8.grid(row=3,column=1)
              amt6.grid(row=3,column=2)
              scale_label = Label(win, text="")
              scale_label.grid(row=4,column=2)
      b1.configure(command = display_menu)
      win.mainloop()
except KeyboardInterrupt:
  print("cleaned everything")
