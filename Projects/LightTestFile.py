# William Cariveau, Brenton Schnider, Elliot Robbins
# The code is intended to test if the light is burnt out and if the button will connect to it to execute the function
# Code written on 9/28/26
# AI was used to generate a test case to ensure the light works and is not burnt out by using a button as input


from machine import Pin
import time

# Pin setup (D5 = GPIO 8, A0 = GPIO 1)
button = Pin("D5", Pin.IN, Pin.PULL_UP)
led = Pin("A0", Pin.OUT)

led_state = False
last_button = 1

while True:
    current_button = button.value()

    # Detect exact moment the button is pressed (1 -> 0 transition)
    if last_button == 1 and current_button == 0:
        led_state = not led_state  # Toggle state
        led.value(led_state)       # Update LED
        time.sleep(0.2)            # Debounce delay to prevent double-clicks

    last_button = current_button
    time.sleep(0.01)
