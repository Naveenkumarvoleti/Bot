import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
class Led(object):

    def __init__(self, pin_number):

        self.pin_number = pin_number
        self.__setup_gpio__()

    def __setup_gpio__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.OUT)

    def clean_up(self):
        GPIO.cleanup(self.pin_number)

    def on_light(self):
        GPIO.output(self.pin_number, True)

    def off_light(self):
        GPIO.output(self.pin_number, False)

    def blink(self, drift_time=0.2):
        self.on_light()
        time.sleep(float(drift_time))
        self.off_light()
        time.sleep(float(drift_time))

    def blinkn(self, number_times):
        for i in range(0, int(number_times)):
            self.blink()

    def blink_non_stop(self):
        while True:
            self.blink()
