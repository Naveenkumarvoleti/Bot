##import threading
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
 
class Sensor():#threading.Thread):
    
    def __init__(self,interval, gpio_trig, gpio_echo):    
        self.inter = interval
        self.trig = gpio_trig
        self.echo = gpio_echo	
        self.dist = 0        
        self.terminated = False
##        self.start()
    
    def run(self):
        while not self.terminated:
            GPIO.setup(self.gpio_trig, GPIO.OUT)
            GPIO.setup(self.gpio_echo, GPIO.IN)
            GPIO.output(gpio_trig, True)
            time.sleep(0.00001)
            
            GPIO.output(gpio_trig, False)
            StartTime = time.time()
            StopTime = time.time()
          
            while GPIO.input(gpio_echo) == 0:
                StartTime = time.time()
          
            while GPIO.input(gpio_echo) == 1:
                StopTime = time.time()

            TimeElapsed = StopTime - StartTime
            self.dist = (TimeElapsed * 34300) / 2
          
            time.sleep(self.inter)

    def get_dist(self):
        return self.dist

SensorA = Sensor(interval=1, gpio_trig=24, gpio_echo=23)

try:
    while True:
        print("Measured Distance = %.1f cm" % SensorA.get_dist())
except KeyboardInterrupt:
    GPIO.cleanup()
    SensorA.terminated = True
