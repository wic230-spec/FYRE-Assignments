# William Cariveau, Brenton Schnider, Elliot Robbins
# The code is intended to combine all of the tested functions, ensuring all of our code works thus far
# Code written on 9/28/26
# AI was used to combine the functions so that the motor rotates when the button is clicked
from machine import Pin, PWM
import time

# Pin setup (If string names fail, use GPIO numbers: D5 = 8, A0 = 1, D3 = 4)
button = Pin("D5", Pin.IN, Pin.PULL_UP)
led = Pin("A0", Pin.OUT)
servo = PWM("D3", freq=50)

def set_servo_angle(angle):
    # Convert 0-180 degrees to PWM duty cycle
    min_duty = 1000
    max_duty = 9000
    duty = min_duty + (angle * (max_duty - min_duty) // 180)
    servo.duty_u16(duty)

system_on = False
last_button = 1

# Start with LED off and motor at 0 degrees
led.value(0)
set_servo_angle(0)

while True:
    current_button = button.value()

    # Detect button press toggle (1 -> 0 transition)
    if last_button == 1 and current_button == 0:
        system_on = not system_on
        time.sleep(0.2)  # Debounce delay

    last_button = current_button

    # Control LED and motor based on toggle state
    if system_on:
        led.value(1)
        set_servo_angle(90)
    else:
        led.value(0)
        set_servo_angle(0)

    time.sleep(0.01)
