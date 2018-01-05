from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
CW = 1
CCW = 0

class stepper():

    def __init__(self,dir_pin,step_pin):
        self.dir_pin= dir_pin
        self.step_pin= step_pin
        self.__setup_gpio__()

    def __setup_gpio__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)

    def forward(self,delay,spr):
        GPIO.output(self.dir_pin, CW)
        for x in range(spr):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)
        self.stop()

    def backward(self,delay,spr):
        GPIO.output(self.dir_pin, CCW)
        for x in range(spr):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)
        self.stop()

    def stop(self):
        GPIO.output(self.step_pin, GPIO.LOW)

    def both(self,delay,spr):
        self.forward(delay,spr)
        sleep(0.0028)
        self.backward(delay,spr)
        sleep(0.0028)
        self.stop()
        
start = stepper(dir_pin = 11, step_pin = 9)

