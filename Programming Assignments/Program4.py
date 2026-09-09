# This program was created in Arduino Lab for MicroPython
#incorperate modules to use functions
import machine as m
import time 

#creates object
#the green lights pin is 0
led = m.Pin(0, m.Pin.OUT)

#creates an infinite loop
while (True):
  led.value(1)
  time.sleep(0.25)
  led.value(0)
  time.sleep(0.25)
