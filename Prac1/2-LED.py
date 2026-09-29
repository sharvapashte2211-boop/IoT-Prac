import RPi.GPIO as GPIO
import time
numTimes=int(input("Enter Total number of blinks:"))
speed = float(input("Enter length of each blink(seconds):"))
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # using board oin numbering
GPIO.setup(11,GPIO.OUT) #LED 1 ON PIN 11
GPIO.setup(13,GPIO.OUT) # LED 2 ON pin 13
def Blink(numTimes,speed):
    for i in range(numTimes):
        print("Iteration",(i+1))
        GPIO.output(11,True)
        GPIO.output(13,True)
        time.sleep(speed)
        GPIO.output(11,False)
        GPIO.output(13,False)
        time.sleep(speed)
Blink(numTimes,speed)
GPIO.cleanup()
print("Done")
