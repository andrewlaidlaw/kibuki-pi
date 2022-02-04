#!/usr/bin/env python

#Setup
import RPi.GPIO as GPIO
import time
from datetime import datetime

INPUT_PIN = 4
OUTPUT_START_PIN = 9
OUTPUT_END_PIN = 16
DELAY = 5

array1 = [9,10,11,12]
array2 = [13, 14, 15, 16]
array3 = [9,11,13,15]
array4 = [10,12,14,16]

current_array = 1

GPIO.setmode(GPIO.BCM)

now = datetime.now()
print("\nRunning Kibuki drop software\n============================")
print(now.strftime("%d/%m/%Y %H:%M:%S"))

print("\nSetting up outputs")

outputs = range(OUTPUT_START_PIN,OUTPUT_END_PIN+1)
for i in outputs:
    GPIO.setup(i,GPIO.OUT)
    GPIO.output(i,GPIO.HIGH)
    print("    Set pin " + str(i) + " as output")

print("\nSetting up input")

GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print("    Set pin " + str(INPUT_PIN) + " as input")

print("\n-- Ready to drop some Kibukis --\n")

# Define functions

def trigger(i):
    print("    Triggering " + str(i))
    GPIO.output(i,GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(i,GPIO.HIGH)
    print("    -- Done --")

def trigger_all():
    i = OUTPUT_START_PIN
    while i < OUTPUT_END_PIN + 1:
        trigger(i)
        i = i + 1

def trigger_array(array):
    print("Triggering on array " + str(array))
    for i in array:
        trigger(i)
    print("Triggered the full array")

# Main code section here, with logic to clean up after exiting

try:
    while True:
        if GPIO.input(INPUT_PIN) == GPIO.HIGH:
            if current_array == 1:
                trigger_array(array1)
            elif current_array == 2:
                trigger_array(array2)
            elif current_array == 3:
                trigger_array(array3)
            elif current_array == 4:
                trigger_array(array4)
            else:
                print("No more arrays to test")
                print("    Count now up to " + str(current_array))
            current_array = current_array + 1
            print("Waiting for " + str(DELAY) + " seconds...")
            time.sleep(DELAY)
            print("Ready to trigger again")
except KeyboardInterrupt:
    print("\nExiting after " + str(current_array - 1) + " kibuki drops")
except:
    print("Something went wrong and the program exited")
finally:
    GPIO.cleanup()