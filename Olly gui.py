from tkinter import *
import tkinter.ttk
import glob,os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from threading import Thread, Event
import threading
import json
import time
import math,random
from sys import exit
import sys
import stepper
from led import Led
import os.path
from pins import*
from ultra import ultrasonic




GPIO.setwarnings(False)
MENU = {}
bottle_level= []
PUMP_SPEED = 0.056356667 # 100 ml / min = 0.056356667 oz / sec
NUM_BOTTLES = 6

first_clean = 0

global DRINK_SIZE
DRINK_SIZE=12

ultrasonicDictionary = [14,15,16,17,18,27] # contains ultrasonic sensor echo pin numbers
readingDict=[]
lock=threading.Lock()

bottle_dict={
             "gin"            : 1,
             "vodka"          : 2,
             "rum"            : 3,
             "soda"           : 4,
             "lilletblonde"   : 5,
             "whiskey"        : 6,
             }
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
              
def cleanCycle(clean_mode,delay):
    popup.destroy()
    if GPIO.input(wasteWaterPin) !=True:
        print("cleaning")
        if ultrasonic(water_pin)> minCleanWater:
          print("cleaning is running")
          GPIO.output(clean_pin,True)
          stepper_motion(clean_mode,delay,clean_speed)
          GPIO.output(clean_pin,False)
          GPIO.output(clean_out,True)
        else:
          print("water is not enough")
          print("water level", ultrasonic(water_pin))
    else:
        popupmsg("waste water is full",cleanCycle("backward",15,))
  
def levelSensing(ultrasonicDictionary):
  print("sensing")
  for u in ultrasonicDictionary:
      reading=ultrasonic(u)
      if reading < requiredWaterLevel:
          print("Drink is not enough, checkreading: " + str(reading))
          pour_thread.acquire()
          
      else:
          print(reading)
          pour_thread.release()
          

def diagnosticCycle(dictionary):
    for u in dictionary:
        for x in range(10):
            print("move the sensor")
            time.sleep(2)
            reading=ultrasonic(u)
            readingDict.append(u)
        avg=sum(readingDict)/float(len(readingDict))
        if all(x==readingDict[0] for x in items)==True:
            print("sensor failed or not working")
        else:
            print("sensor is working")
            
#stepper start stop and motion
def stepper_motion(mode,delay,speed,spr=100):
  close_time=round(time.time()+delay)
  while time.time() < close_time:
    if mode=="continues":
      stepper.start.forward(speed,spr)
    elif mode== "both":
      stepper.start.both(speed,spr)
    elif mode== "backward":
      stepper.start.backward(speed,spr)
  ##  time.sleep(delay)
    stepper.start.stop()

#mixing Drink
def mixing(mode,ice=0):
##    gpio_high_low(mix_pin,mix_delay)
    print(mode)
    if mode == 1:
      print("mixing with two way")# mixing two way
      GPIO.output(mix_pin,True)
      stepper_motion("continues",mix_delay,mode1_speed,spr = 100)
      GPIO.output(mix_pin,False)
      
    elif mode == 2:
      print("mixing with one way")# mixing conitnuous fast
      GPIO.output(mix_pin,True)
      stepper_motion("both",mix_delay,mode2_speed,spr = 100)
      GPIO.output(mix_pin,False)
      
    elif mode == 3:                     # mixing continous fast
      print("mixing fast")
      GPIO.output(mix_pin,True)
      stepper_motion("backward",mix_delay,mode3_speed,spr = 100)
      GPIO.output(mix_pin,False)
      
    elif mode == 4:
      print("layering drink")
      GPIO.output(mix_pin,True)
      stepper_motion("backward",mix_delay,mode4_speed,spr = 100)
      GPIO.output(mix_pin,False)
    else:
      print("the mixing mode is not avilable")
    if ice==1:
      time.sleep(0.5)
      ice_crushing(crushing_time = 10)

# ice crushing
def ice_crushing(crushing_time):
  print("crushing ice")
  GPIO.output(ice_pin,True)
  stepper_motion("continues",crushing_time,crushing_speed)
  GPIO.output(ice_pin,False)
  

#get pour time
def get_pour_time(size,pour_prop, total_prop):
  return ((size * (pour_prop/total_prop)) / PUMP_SPEED)

# making Drink

def make_drink(drink_name,ice = 0,size=12):

  # check that drink exists in menu
  if not drink_name in MENU:
    print('drink "' + drink_name + '" not in menu')
    return

  # get drink recipe
  recipe = MENU[drink_name]
##  print(drink_name + ' = ' + str(recipe))

  # sort drink ingredients by proportion amount
  sorted_recipe = sorted(recipe, key=lambda p: p['amount'], reverse=True)

  # calculate time to pour most used ingredient
  total_proportion = 0
  for p in sorted_recipe:
    total_proportion += p['amount']
  drink_time = get_pour_time(size,sorted_recipe[0]['amount'], total_proportion)
  print('Drink will take ' + str(math.floor(total_proportion)) + 's\n')
  # for each pour
  if not lock.acquire(False):
      for i, pour in enumerate(sorted_recipe):
          if pour['ingredient'] in bottle_dict:
              position= bottle_dict[pour['ingredient']]
              if position == 1:
                    bottle_num = 9
              elif position == 2:
                    bottle_num = 10
              elif position == 3:
                    bottle_num = 12
              elif position == 4:
                    bottle_num = 13
              elif position == 5:
                    bottle_num = 15
              elif position == 6:
                    bottle_num = 16
    ##          print(drink_time)
             
              else:
                  print("there is no"+ pour['ingredient']+".  update bottle list\n")
    ##      progress_bar["value"] = 50
          if i == 0:
            pour_time = get_pour_time(size,pour['amount'], total_proportion)
            # start pouring with no delay
            pour_thread = Thread(target=trigger_pour, args=([bottle_num, math.floor(pour_time)]))
            pour_thread.start()
            pour_thread.join()
          # for other ingredients
          else:
            # calculate the latest time they could start
            pour_time = get_pour_time(size,pour['amount'], total_proportion)
            latest_time = drink_time - pour_time
            # start each other ingredient at a random time between now and latest time
            start_delay = 2#random.randint(0, math.floor(latest_time))
            pour_thread = Thread(target=trigger_pour, args=([bottle_num, math.floor(pour_time), start_delay]))
            pour_thread.start()
            pour_thread.join()
      mixing_thread=threading.Thread(target=mixing,args=(random.randint(1,3),))
      mixing_thread.start()
      mixing_thread.join()
      time.sleep(1)
      if MENU["ice"]!=0 and ice !=0:
          ice_thread=threading.Thread(target = ice_crushing,args=(10,))
          ice_thread.start()
          ice_thread.join()
      popupmsg("Do you want to clean the glass",cmd=popup.destroy())
  else:
      print("interrupted")
##  pour_event.set()

def trigger_pour(bottle_num, pour_time, start_delay=0):
  print('Pouring bottle for ' + str(pour_time) + 's after a ' + str(start_delay) + 's delay\n\n')
  print(bottle_num)
  time.sleep(start_delay) # start delay
  GPIO.output(bottle_num,True)# start bottle pour
  time.sleep(pour_time) # wait
  GPIO.output(bottle_num,False)# end bottle pour


##
##def wait_upto():
##  while 
            

def run(file,ice,size):
    win.destroy()
    with open(file) as f:
      drinkData =json.loads(f.read())
      MENU.update(drinkData)
      time.sleep(0.25)
      popupmsg("place the glass",1)
      print("place the glass")
      popup.destroy()
      GPIO.wait_for_edge(glassPin,GPIO.RISING)
      popup.destroy()
      popupmsg("glass is placed",Type=1,cmd=popup.destroy())
      popup.destroy()
      print (MENU['drink'])
      global drink
      drink = MENU['drink']
      make_drink(drink,ice,size)
      time.sleep(2)

def single(name,amount,delay):
      position= bottle_dict[name]
      if position == 1:
            bottle_num = 9
      elif position == 2:
            bottle_num = 10
      elif position == 3:
            bottle_num = 12
      elif position == 4:
            bottle_num = 13
      elif position == 5:
            bottle_num = 15
      elif position == 6:
            bottle_num = 16
      trigger_pour(bottle_num,get_pour_time(amount,DRINK_SIZE),delay)

def make(p,q,r,s,t):
      while True:
        index =0
        for x in range(MENU["no_of_operations"]):
          time.sleep(0.25)
          bottle_num = MENU['operation'][x]['bottle']
          bottle=bottle_num+3
          GPIO.output(bottle,True)
          print("pouring bottle",bottle)
          pour_time = get_pour_time(MENU['operation'][x]['amount'], total_prop = 12)
          time.sleep(pour_time)
          GPIO.output(bottle,False)
          index+=1
        break
      
global win
win = Tk()
win.attributes("-zoomed",True)
##win.minsize(width=480, height=320)
##win.config(menu=blank_menu)
win.title("Olly")
f= Frame(win)
l= Label(win,text = "HI...")
b1= Button(f,text = "Let's Make Drink")
##b2 = Button(f,text = "Bottle update")
##b2.pack()
l.pack()
f.pack()
global file

level=threading.Timer(5.0,levelSensing,args=(ultrasonicDictionary,)).start()

def popupmsg(msg,Type=0,bT="ok",cmd=None):
    global popup
    popup = Tk()
    popup.wm_title("ERROR")
    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    if Type == 1:
        b1=Button(popup,text=bT,command= popup.destroy)
        b1.pack()
    else:
        B1 = Button(popup, text="Yes", command = lambda :cmd)
        B1.pack()
        B2 = Button(popup, text="NO", command = popup.destroy)
        B2.pack()
    popup.mainloop()
              
try:
      def interrupt1(channel):
            lock.acquire()
            print("lid opened..please close the lid")
##            GPIO.wait_for_edge(20,GPIO.RISING)
##            time.sleep(60)
            lock.release()
            
      def interrupt2(channel):
            print("place the glass")
            lock.acquire()
##            GPIO.wait_for_edge(21,GPIO.RISING)
##            time.sleep(60)
            lock.release()
            
      GPIO.add_event_detect(LidPin,GPIO.FALLING,callback=interrupt1,bouncetime=300)
      GPIO.add_event_detect(wasteWaterPin,GPIO.FALLING,callback=lambda :popupmsg("waste water is full",Type=1,bt="retry",cmd=popup.destroy()),bouncetime=300)
##      GPIO.add_event_detect(glassPin,GPIO.FALLING,callback=interrupt2,bouncetime=300)

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
        b6 = Button(win,text = "Create Drink")
        b7=Button(win,text="single Drink")
        b4.pack(side=TOP,padx= 10,pady=10)
        b5.pack(side= TOP,pady=10,padx=10)
        b6.pack(side =TOP,padx=10,pady=10)
        b7.pack(side =TOP,padx=10,pady=10)
        b5.configure(command= bottle_update)
        b4.configure(command =display_files)
        b6.configure(command = create_drink)
        b7.configure(command = seperate_drink)
          
      def commando(x,y):
          for k,v in list(bottle_dict.items()):
            if v == int(y):
               del bottle_dict[k]
          bottle_dict.update({x:int(y)})
          print(sorted(bottle_dict.items(), key=lambda x: x[1]))
          
          
      def display_files():
          b4.pack_forget()
          b5.pack_forget()
          b6.pack_forget()
          b7.pack_forget()
          win.title("Olly")
          l6=Label(win,text="Select Drink file")
          l5 = Label(win,text = "Do you want ice : ")
          l6.pack()
##          sb = Scrollbar(win,orient=VERTICAL)
##          sb.pack(side=RIGHT,fill=Y)
          slct = StringVar(win)
          slct.set("select")
          choices = {'Yes','No'}
          popupmenu = OptionMenu(win,slct,*choices)
          lb = Listbox(win,width=15,height=2)
          lb.pack(side=TOP,pady=2)
          os.chdir(".")
          for file in glob.glob("*.json"):
            files=file
            lb.insert(END,files)
##          sb.config(command=lb.yview)
##          lb.configure(yscrollcommand=sb.set)
          b8=Button(win,text="MAKE DRINK")
          amt=Scale(win,from_=1,to= 12,orient=HORIZONTAL,resolution=1)
          b8.configure(command = lambda :run(lb.get(ACTIVE),slct.get(),amt.get()))
          l6=Label(win,text="Enter drink size")
          l6.pack()
          amt.pack()
          l5.pack()
          popupmenu.pack()
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
          z=list(sorted(bottle_dict.keys())) 
          label_1 = Label(win, text="Enter ingredient name: ")
          label_2 = Label(win, text="select bottle, 1-6:")
          label_3 = Label(win,text=z)
          entry_1 = Entry(win, textvariable=x)
##          entry_2 = Entry(win, textvariable=y)
          slct = StringVar(win)
          slct.set("select")
          choices = {'1','2','3','4','5','6'}
          popupmenu = OptionMenu(win,slct,*sorted(choices))
          popupmenu.grid(row = 4,column=2)
          label_1.grid(row=1,column=2)
          label_2.grid(row=3,column=2)
          label_3.grid(row=6,column=2)

          entry_1.grid(row=2, column=2)
##          entry_2.grid(row=4, column=0)
          but = Button(win, text="Update", command=lambda :commando(x.get(), slct.get()))
          but.grid(row=5, column=2)
          but1=Button(win,text="Main menu")
          but1.grid(row=10,column=10)
          but1.configure(command=back_menu)
          
      def back_menu():
##            but.grid_forget()
##            but1.grid_forget()
##            label_1.grid_forget()
##            label_2.grid_forget()
##            label_3.grid_forget()
##            popupmenu.grid_forget()
##            entry_1.grid_forget()
            win.title("Olly")
            b4 = Button(win,text ="Select Drink")
            b5 = Button(win,text ="Bottle update")
            b6 = Button(win,text = "Create Drink")
            b7=Button(win,text="single Drink")
            b4.pack(side=TOP,padx= 10,pady=10)
            b5.pack(side= TOP,pady=10,padx=10)
            b6.pack(side =TOP,padx=10,pady=10)
            b7.pack(side =TOP,padx=10,pady=10)
            b5.configure(command= bottle_update)
            b4.configure(command =display_files)
            b6.configure(command = create_drink)
            b7.configure(command = seperate_drink) 
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
          l1.grid(row=1)
          l2.grid(row=2)
          l3.grid(row=3)
          l4.grid(row=4)
          l5.grid(row=5)
          butt = Button(win,text = "MAKE",command = lambda : make(amt1.get(),amt2.get(),amt3.get(),amt4.get(),slct.get()))
          butt.grid(row=6)
          slct = StringVar(win)
          slct.set("Yes")
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
              optionmenu = OptionMenu(win,selct,*bottle_dict.keys())
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
      b1.pack()
      b1.configure(command = display_menu)
      time.sleep(20)
##      b1.invoke()
      win.mainloop()
except KeyboardInterrupt:
  print("cleaning everything")
  GPIO.cleanup()
