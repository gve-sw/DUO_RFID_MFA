#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    while True:
        text = raw_input('Your Name: ')
        print("Now place tag next to the scanner to write")
        id, text = reader.write(text) 
        print("recorded")
        print(id)
        print(text)
        break
        
finally:
     GPIO.cleanup()
