#GPIO pin testing
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pin = 17
GPIO.setup(pin,GPIO.IN,GPIO.PUD_UP)
prev = False
while True:
    button = GPIO.input(pin)
    
    if button != prev: 
        if button:
            print (pin , ", open")
        else:
            print(pin , ", pressed")
        prev = button
        
