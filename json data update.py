from tkinter import*

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Yes", command = popup.destroy)
    B1.pack(side=LEFT,padx=40,pady=30)
    B2 = Button(popup, text="No", command = popup.destroy)
    B2.pack(side=RIGHT,padx=40,pady=30)
    popup.mainloop()
    
popupmsg("run")
