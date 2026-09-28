# William Cariveau, Brenton Schnider, Elliot Robbins
# The code is intended to test to see if the motor will spin
# Code written on 9/28/26
# AI was used to turn the idea of how the program would work into actual execution

import time

# Servo setup on pin D3
servo = PWM("D3", freq=50)

def set_servo_angle(angle):
    # Convert 0-180 degrees to PWM duty cycle (1000 to 9000)
    min_duty = 1000
    max_duty = 9000
    duty = min_duty + (angle * (max_duty - min_duty) // 180)
    servo.duty_u16(duty)

print("Starting servo test... Press Ctrl+C to stop.")

while True:
    # Move to 0 degrees
    set_servo_angle(0)
    time.sleep(1)

    # Move to 90 degrees
    set_servo_angle(90)
    time.sleep(1)

    # Move to 180 degrees
    set_servo_angle(180)
    time.sleep(1)
