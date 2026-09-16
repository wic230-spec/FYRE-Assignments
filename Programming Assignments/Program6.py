# William Cariveau, Brenton Schnider, Elliot Robbins
# The code is intended to rotate an arm about a motor 180 degrees
# Code written on 9/16/26
# AI was used to write the program from a carefully written prompt
# The code was manually debugged
from machine import Pin, PWM
import time

# Servo on D3
servo = PWM("D3", freq=50)

# Button on D7
button = Pin("D7", Pin.IN, Pin.PULL_UP)

# Start at 0 degrees
position = 0

def set_servo_angle(angle):
    # Convert 0-180 degrees to servo duty cycle
    min_duty = 1000
    max_duty = 9000
    duty = min_duty + (angle * (max_duty - min_duty) // 180)
    servo.duty_u16(duty)

set_servo_angle(0)

while True:
    # Button pressed
    if button.value() == 0:
        # Move 180 degrees
        if position == 0:
            position = 180
        else:
            position = 0

        set_servo_angle(position)

        # Wait for button release
        while button.value() == 0:
            time.sleep(0.01)

        # Small debounce delay
        time.sleep(0.05)
