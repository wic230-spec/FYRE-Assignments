from machine import Pin
import time

sensor1 = Pin(21, Pin.IN)
sensor2 = Pin(17, Pin.IN)

led1 = Pin(48, Pin.OUT)
led2 = Pin(9, Pin.OUT)

system_on = False
last_button = 0

while True:
    button = sensor1.value()
    sensor2_active = sensor2.value()

    # Detect ONE button click
    if button == 1 and last_button == 0:
        system_on = not system_on
        time.sleep(0.2)  # debounce

    last_button = button

    # LED 1 stays ON/OFF indefinitely
    if system_on:
        led1.value(1)
    else:
        led1.value(0)

    # LED 2 only works when system is ON
    # AND sensor 2 is active
    if system_on and sensor2_active == 1:
        led2.value(1)
    else:
        led2.value(0)

    time.sleep(0.01)
