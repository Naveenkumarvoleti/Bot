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
from pins import*
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
PUMP_SPEED = 0.056356667 # 100 ml / min = 0.056356667 oz / sec
NUM_BOTTLES = 7


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
  while (senseevent.wait() and levelsenseEvent.wait()):
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

def trigger_pour(bottle_num, pour_time, start_delay=0):
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

