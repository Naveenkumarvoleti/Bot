#!/usr/bin/python
import time
from time import sleep
import sys
import json
import math, random
import os.path
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from threading import Thread, Event
import threading
import os,glob
import led
import stepper
##from pins import*
from ultrasonic import ultrasonic
global delay
# customizations
DRINK_SIZE = 12 # size of the cup to fill in ounces
# recipes below assume:
#   bottle 1 = Gin
#   bottle 2 = Vodka
#   bottle 3 = soda
#   bottle 4 = Lillet Blonde
#   bottle 5 = unused
#   bottle 6 = unused
#   bottle 7 = water
bottle_dict={
             "gin"            : 1,
             "vodka"          : 2,
             "rum"            : 3,
             "soda"           : 4,
             "lillitblonde"   : 5,
             "wine"           : 6
             }

GPIO.setwarnings(False)
MENU = {}
bottle_level= []
PUMP_SPEED = 0.056356667 # 100 ml / min = 0.056356667 oz / sec
NUM_BOTTLES = 7
first_clean = 0
min_clean_water = 5
create = {}


global mix_pin
global Clean_water_pin
global waste_water_pin
global ice_pin
global glass_pin
global e
global clean_event
global water_event
global levelsenceEvent

e = threading.Event()
water_event = e
clean_event = e
levelsenceEvent = e
mix_pin = 4 # runs solinoid which connects mixxing unit
clean_water_pin = 20 # ultasonic echo pin of clean water
waste_water_pin = 21  # this is the input pi triggered when it touches water
ice_pin = 19 # runs solenoid which connects ice crushing unit
clean_pin = 14 # solenoid pin for cleaning
ultrasonicArr = [1,2,3,4,5,6] # contains sensor pin numbers


#update bottle array
def bottle_update (MENU):
  index = 0
  for b in range(MENU["no_of_drinks"]):
    bottle_level.append(MENU[drink][index]["bottle"])
    index+=1
    print(bottle_level)


##checks each liquid level
def detect_level(bottle_level):
  for n in bottle_level:
    x = 0
    for d in range(MENU["no_of_drinks"]):
      if ultrasonic.run_once(bottle_level[x]) > (MENU["process"][x]["amount"]):
        x+=1
        continue
        bottle_levelevent.is_set()
      else:
        print("the bottle", bottle_level[x] , "doesn't have enough........","please fill", (MENU["process"][x]["ingredient"]) , "with it"  )
        bottle_levelevent.clear()
        
def all_bottle_level(array):
    i = 0
    for i in array:
      level = ultrasonic.run_once(i)
      if level <= 8:
        print("bottle ",i," ",level)
        eachlevel.set()
      else:
        print("bottle ",i," ",level," is not enough. please fill it")
        eachlevel.wait()
      i+=1
    levelsenseEvent.set()

##def detect_level(bottle_level,threading.Event()):

class sense(threading.Thread):
  def __init__(self,lid_pin,glass_pin):
    self.lid_pin=lid_pin
    self.glass_pin=glass_pin
    threading.Thread.__init__(self)
    self.senseevent = threading.Event()
  #sense glass wether placed or not
  def glass_sense(self):
      if GPIO.input(self.glass_pin) == True:
        print("glass is placed")
        led.run.off_light()
        return True
      else:
        print("place the glass")
        led.run.blink(drift_time= 1)

  #lid detection
  def lid_detect(self):
      if GPIO.input(self.lid_pin) == True:
        led.run2.off_light()
        print("Lid is closed\n")
        return True
      else:
        led.run2.on_light()
        print("lid is opened. please close the lid\n")

  def Both(self):
    while True:
      if glass_sense() and lid_detect() == True:
        self.senseevent.set()
        return True
      else:
        sef.senseevent.clear()
        pass

#making and crushing ice
def make_ice(ice_pin,delay,speed):
    stepper.start.stop()
    GPIO.output(ice_pin,True)
    stepper.start.forward(speed,spr= 200)
    time.sleep(delay)
    stepper.start.stop()
    GPIO.output(ice_pin,False)

#mixing Drink
def mixing(mode,speed=0.006,delay=10):
  if mode == 1:
    GPIO.output(mix_pin,True)
    stepper.start.Both(speed,spr = 100)
    print("mixing with two way")
    time.sleep(delay)
    stepper.start.stop()
    GPIO.output(mix_pin,False)
  elif mode == 2:
    GPIO.output(mix_pin,True)
    stepper.start.Forward(speed,spr = 100)
    print("mixing with one way")
    time.sleep(delay)
    stepper.start.stop()
    GPIO.output(mix_pin,False)
  elif mode == 3:
    pass
##    GPIO.output(mix_pin,True)
##    stepper.start.Both(spr = 100,speed)
##    print("mixing with two way")
##    time.sleep(delay)
##    stepper.start.stop()
##    GPIO.output(mix_pin,False)
  elif mode == 4:
    pass
##    GPIO.output(mix_pin,True)
##    stepper.start.Both(spr = 100,speed)
##    print("mixing with two way")
##    time.sleep(delay)
##    stepper.start.stop()
##    GPIO.output(mix_pin,False)

    
#get pour time
def get_pour_time(pour_prop, total_prop):
  return (DRINK_SIZE * (pour_prop / total_prop)) / PUMP_SPEED

# making Drink

def make_drink(drink_name):

  print('make_drink()')

  # check that drink exists in menu
  if not drink_name in MENU:
    print('drink "' + drink_name + '" not in menu')
    return

  # get drink recipe
  recipe = MENU[drink_name]
  print(drink_name + ' = ' + str(recipe))
  
  # sort drink ingredients by proportion amount
  sorted_recipe = sorted(recipe, key=lambda p: p['amount'], reverse=True)
  i = 0
  for key in sorted_recipe[i].keys():
    if key in bottle_dict.keys():
        bottle_num = bottle_dict[key]
        print (int(bottle_num))
        i+=1
  # calculate time to pour most used ingredient
  total_proportion = 0
  for p in sorted_recipe:
    total_proportion += p['amount']
  drink_time = get_pour_time(sorted_recipe[0]['amount'], total_proportion)
  print('Drink will take ' + str(math.floor(drink_time)) + 's')
  print(sorted_recipe)

  # for each pour
##  while (senseevent.wait() and levelsenseEvent.wait()):
  for i, pour in enumerate(sorted_recipe):
              
      if i == 0:
        # start pouring with no delay
        
        pour_thread = Thread(target=trigger_pour, args=([pour['bottle'], math.floor(drink_time)]))
        pour_thread.start()

      # for other ingredients
      else:
        # calculate the latest time they could start
        pour_time = get_pour_time(pour['amount'], total_proportion)
        latest_time = drink_time - pour_time
        # start each other ingredient at a random time between now and latest time
        start_delay = random.randint(0, math.floor(latest_time))
        pour_thread = Thread(target=trigger_pour, args=([pour['bottle'], math.floor(pour_time), start_delay]))
        pour_thread.start()
        
##      if not ice_pin == 1:
##        mixing(mode= random.randint(1,4))
##        print("mixing drink")

##      make_ice(ice_pin=6)
##      clean.join()
  
##class water_level(threading.Thread):
##  #checks water level
##  def __init__(self,clean_water_pin):
##    self.clean_water_pin= clean_water_pin
##    self.water_levelevent = threading.Event
      
def clean_water_level(clean_water_pin):

 while True:
   Water_test= Thread(target=ultrasonic_level,args=(clean_water_pin))
   water_test.join(timeout = 2)
   print (level)
   if level >= min_water_level or GPIO.input(pin_number):
     water_event.set()
     GPIO.output(pin,True)
   else:
     print("clean water is not enough")
     print("fill it now")
     water_event.clear()
     GPIO.output(pin,True)

     
##  def waste_water_level(waste_water_pin):
##    while True:
##      if GPIO.input(waste_water_pin):
##        event1 = threading.Event()

#checks each liquid level
# def level_detection(bottle_num):
#   v=0
#   for v in range(MENU["no_of_drinks"])
#     if bottle_num == 1:
#       ultrasonic.run_once(bottle1)#bottle 1
#       print ("bottle 1 level : ",level)
#     elif bottle_num == 2:
#       ultrasonic.run_once(bottle2)#bottle 2
#       print ("bottle 2 level : ",level)
#     elif bottle_num == 3:
#       ultrasonic.run_once(bottle3)#bottle 3
#       print ("bottle 3 level : ",level)
#     elif bottle_num == 4:
#       ultrasonic.run_once(bottle4)#bottle 4
#       print ("bottle 4 level : ",level)
#     elif bottle_num == 5:
#       ultrasonic.run_once(bottle5)#bottle 5
#       print ("bottle 5 level : ",level)
#     else bottle_num == 6:
#       ultrasonic.run_once(bottle6)#bottle 6
#       print ("bottle 6 level : ",level)
#     v+=1


#cleans the mixing unit
def clean_cycle(delay,min_clean_water,waste_water_pin,clean_water_pin):
  if not waste_water_pin == True:
    water_event.wait()
    GPIO.output(pin,False)
    GPIO.output(clean_pin,True)
    stepper.start.forward(delay,spr=200)
    print("cleaning")
    sleep(delay)
    stepper.start.stop()
    GPIO.output(clean_pin,False)
    print("cleaned")
    clean_event.set()
  else:
    print("clean the waste water compartment")
    GPIO.output(pin,True)
    
##  else:
##    print("clean the waste water compartment")
##    clean_event.wait()
##def bottle_pin():
##    
# pouring
def trigger_pour(bottle_num, pour_time, start_delay=0):
  if bottle_num > NUM_BOTTLES:
    print('Bad bottle number')
    return
  print(threading.activeCount())
  print (threading.enumerate()) 
  print('Pouring bottle ' + str(bottle_num) + ' for ' + str(pour_time) + 's after a ' + str(start_delay) + 's delay')
  bottle_num+=3
  time.sleep(start_delay) # start delay
  print(start_delay)
  GPIO.output(bottle_num,True)# start bottle pour
  time.sleep(pour_time) # wait
  GPIO.output(bottle_num,False)# end bottle pour
  print(pour_time)
  bottle_num=0
  
# file checking
def run(file):
    with open(file) as f:
      drinkData =json.loads(f.read())
      MENU.update(drinkData)
##      bottle_update(MENU)
      print(MENU)
      time.sleep(0.25)
      print("put the glass now")
      print (MENU['drink'])
      global drink
      drink = MENU['drink']
      make_drink(drink)
      time.sleep(2)
##      mixing(mode= random.randint(1,4))
##      print("mixing drink")
##      make_ice(ice_pin,delay,speed)

def make(p,q,r,s):
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
    

if __name__ == '__main__':
    GPIO.cleanup()
    global file
    global ice
##    os.chdir(".")
##    for data in glob.glob("*.json"):
##        print(data)
##        file = input("select a file from given list: ")
##        ice_input = input("Do you want Ice: ")
##        if ice_input == "yes" or "y":
##          ice = 1
##        else:
##          ice = 0
    
    sensing = threading.Thread(target = sense,args = (14,13,),name = "sense")
    sensing.start()

    clean = threading.Thread(target = clean_cycle,args = (delay,min_clean_water,waste_water_pin,clean_water_pin,),name = "clean")
    clean.start()
 
    level = threading.Thread(target = all_bottle_level,args=(ultrasonicArr,),name = "ultrasonic")
    level.start()
##
##    if not first_clean == 0:
##      bottle_levelevent.wait()
##      run(file)
##    else:
##      try:
##        clean.join()
##        print(threading.activeCount())
##        print (threading.enumerate()) 
##        clean_event.wait()
##        bottle_levelevent.wait()
##        run(file)
##      except KeyboardInterrupt:
##        clean.start()
##    GPIO.cleanup()

from tkinter import *
import glob,os
global fL 
fL = {}
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
        print(file)
        
def display_menu():
    win1 = Tk()
    win1.title("Olly")
    b4 = Button(win1,text ="Select Drink")
    b5=Button(win1,text ="Bottle update")
    b6 =Button(win1,text = "Create")
    b4.pack(side=LEFT,padx= 10,pady=10)
    b5.pack(side= LEFT,pady=10)
    b6.pack(side =RIGHT,padx=10,pady=10)
    b5.configure(command= bottle_update)
    b4.configure(command = display_files)
    b6.configure(command = create_drink)
    
def commando(x, y):
    bottle_dict.update({x:int(y)})
    print(bottle_dict)
    
def display_files():
    win3=Tk()
    win3.title("Olly")
    sb = Scrollbar(win3,orient=VERTICAL)
    sb.pack(side=RIGHT,fill=Y)
    lb = Listbox(win3, height=3)
    lb.pack()
    lb.insert(END,"vesper.json")
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

def create_drink():
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
    butt = Button(win4,text = "MAKE",command = lambda : make(amt1.get(),amt2.get(),amt3.get(),amt4.get()))
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
    
b1.configure(command = display_menu)
win.mainloop()
