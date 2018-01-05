import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class ultrasonic():
    
    def __init__(self, pin_number):
        GPIO.setup(pin_number,GPIO.IN)
##        self.interval= interval
        self.stop= False

    def liquid_level(self):
        while not self.stop:
            TRIG=24
            GPIO.setup(TRIG,GPIO.OUT)
            GPIO.output(TRIG, True)
            time.sleep(0.001)
            GPIO.output(TRIG, False)
            while GPIO.input(self.pin_number)== 0:
                start_pulse= time.time()

            while GPIO.input(self.pin_number)== 1:
                stop_pulse= time.time()

                pulse_width = stop_pulse - start_pulse

                distance = pulse_width* 17150
                distance = round(distance/2)
                return distance
                print("level",distance)
        
    def run_once(self,pin_number):
        level = liquid_level(pin_number)
        return level
start=ultrasonic(pin_number=23)
while True:
    start.liquid_level()
