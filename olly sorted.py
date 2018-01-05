#!/usr/bin/python
import time
from time import sleep
import sys
import json
import math, random
import os.path
import RPi.GPIO as GPIO
from threading import Thread, Event
import threading
import os,glob
import led
import stepper
import random
import pins
import gui
import ultrasonic

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

MENU = {}
#bottle_level= []

PUMP_SPEED = 0.056356667 # 100 ml / min = 0.056356667 oz / sec
NUM_BOTTLES = 7
e = threading.Event()


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
        self.senseevent.isSet()
        return True
      else:
        sef.senseeventis_clear()
        pass


#checks each liquid level
##def detect_level(bottle_level,threading.Event()):
##  for n in bottle_level:
##    x = 0
##    for d in range(MENU["no_of_drinks"]):
##      if ultrasonic.run_once(bottle_level[x]) > (MENU["process"][x]["amount"]):
##        x+=1
##        continue
##      else:
##        print("the bottle", bottle_level[x] , "doesn't have enough........","please fill", (MENU["process"][x]["ingredient"]) , "with it"  )
##        return 0
##
##def detect_level(bottle_level,e):


#cleans the mixing unit
def clean_cycle(delay,waste_water_pin,clean_water_pin):
  if not waste_water_pin == True:
    if water_level(clean_water_pin) >= 5:
      GPIO.output(clean_pin,True)
      print("cleaning")
      sleep(delay)
      GPIO.output(clean_pin,False)
      print("cleaned")
    else:
      print("fill the water to clean")
  else:
    print("clean the waste water compartment")

class water_level(threading.Thread):
  #checks water level
  def __init__(self,clean_water_pin):
    self.clean_water_pin= clean_water_pin
    self.water_levlevent = threading.Event
  def clean_water_level(self):
   while True:
     Water_test= Thread(target=ultrasonic_level,args=(self.clean_water_pin))
     water_test.join(timeout = 2)
     print (level)
     if level >= 5:
       self.water_levelevent.is_set()
     else:
       print("clean water is not enough")

def run(file):
    with open(file) as f:
      drinkData =json.loads(f.read())
      MENU.update(drinkData)
      print(MENU)
      time.sleep(0.25)
      clean.join()
      print("put the glass now")
      print (MENU['drink'])
      make_drink(MENU['drink'])
##      while True:
##        index =0
##        for x in range(MENU["no_of_operations"]):
##          time.sleep(0.25)
##          bottle_num = MENU['operation'][x]['bottle']
##          bottle=bottle_num+3
##          GPIO.output(bottle,True)
##          print("pouring bottle",bottle)
##          pour_time = get_pour_time(MENU['operation'][x]['amount'], total_prop = 12)
##          time.sleep(pour_time)
##          GPIO.output(bottle,False)
##          index+=1
##        break



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
  # print(sorted_recipe)
  # calculate time to pour most used ingredient
  total_proportion = 0
  for p in sorted_recipe:
    total_proportion += p['amount']
  drink_time = get_pour_time(sorted_recipe[0]['amount'], total_proportion)
  print('Drink will take ' + str(math.floor(drink_time)) + 's')

  # for each pour
  for i, pour in enumerate(sorted_recipe):
    if i == 0:
      # start pouring with no delay
      pour_thread = Thread(target=trigger_pour, args=([pour['bottle'], math.floor(drink_time)],ice))
      pour_thread.start()

    # for other ingredients
    else:
      # calculate the latest time they could start
      pour_time = get_pour_time(pour['amount'], total_proportion)
      latest_time = drink_time - pour_time
      # start each other ingredient at a random time between now and latest time
      delay = random.randint(0, math.floor(latest_time))
      pour_thread = Thread(target=trigger_pour, args=([pour['bottle'], math.floor(pour_time), delay]))
      pour_thread.start()

# pouring
def trigger_pour(bottle_num, pour_time, start_delay=0,ice=0):
  if bottle_num > NUM_BOTTLES:
    print('Bad bottle number')
    return
  print(threading.activeCount())
  print (threading.enumerate()) 
  print('Pouring bottle ' + str(bottle_num) + ' for ' + str(pour_time) + 's after a ' + str(start_delay) + 's delay')
  bottle_num+=1
  time.sleep(start_delay) # start delay
  GPIO.output(bottle_num,True)# start bottle pour
  time.sleep(pour_time) # wait
  GPIO.output(bottle_num,False)# end bottle pour

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



if __name__ == '__main__':
    GPIO.setwarnings(False)
    global file
    global ice
    os.chdir(".")
    for file in glob.glob("*.json"):
        print(file)
        file = input("select a file from given list: ")
        ice_input = input("Do you want Ice: ")
        if ice_input == "yes" or "y":
          ice = 1
        else:
          ice = 0
    sensing = threading.Thread(target = sense,args = (14,13,),name = "sense")
    sensing.start()
    level = threading.Thread(target = detect_level,args=(bottle_level,),name = "ultrasonic")
    level.start()
    clean = threading.Thread(target = clean_thread,name = "clean")
    clean.start()
    run(file)
    
