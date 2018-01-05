import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
mix_pin = 4             # runs solenoid which connects mixxing unit
cleanWaterPin = 20    # ultrasonic echo pin of clean water
wasteWaterPin = 21    # this is the input pi triggered when it touches water
glassPin=22 # glass place detection
ice_pin = 19            # runs solenoid which connects ice crushing unit
clean_pin = 14          # solenoid pin for cleaning
led1_pin = 17 # status led
led2_pin = 27 # status led
mix_pin = 19 #mixing gear solenoid
ice_pin = 14# ice gear solenoid
waterPathPin=2 # waste water path
LidPin=23
out_pins=[2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,27]
in_pins =[20,21,22,23,24,25]

for p in out_pins:
    GPIO.setup(int(p),GPIO.OUT)
for p in in_pins:
    GPIO.setup(int(p),GPIO.IN)

    
### json read
##with open('data.json')as f:
##    data=json.loads(f.read())
##    print(f)

requiredWaterLevel = 10
mode1_speed= 0.006
mode2_speed=0.003
mode3_speed = 0.006
mode4_speed=0.028
mix_delay= 10
crushing_speed=0.006
min_clean_water = 5
clean_speed=0.001

GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
##GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN,pull_up_down=GPIO.PUD_UP)
