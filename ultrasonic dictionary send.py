import RPi.GPIO as GPIO
import pins
from ultra import ultrasonic
ultrasonicDictionary = [14,15,16,17,18,27] # contains ultrasonic sensor echo pin numbers
readingDict=[]
requiredWaterLevel = 10
for u in ultrasonicDictionary:
    reading=ultrasonic(u)
    readingDict.append(reading)
    if reading < requiredWaterLevel:
        print("water is not enough, reading: "+ str(reading))
    else:
        print(reading)
        
def diagnosticCycle(dictionary):
    for u in dictionary:
        for x in range(10):
            reading=ultrasonic(u)
            readingDict.append(u)
        avg=sum(readingDict)/float(len(readingDict))
        if all(x==readingDict[0] for x in items)==True:
            print("sensor failed")
        else:
            print("sensor is working")
            
print (avg)
print(readingDict)
