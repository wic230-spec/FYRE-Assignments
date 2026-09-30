# William Cariveau, Brenton Schnider, Elliot Robbins
# The code is intended to find the baseline resistivity of the sensor we made in lab
# Code written on 9/30/26
# AI was used to turn the code from the test programs, as well as program5, into a program that performs our desired result. The code was debugged manually.
from machine import Pin, PWM, ADC
import time

# Pin assignments
BUTTON_PIN = "D5"  # Toggle button
LED_PIN = "A0"     # Status LED
SERVO_PIN = "D3"   # Servo motor
RAIN_PIN = "A3"    # Rain sensor (analog)

# Setup GPIO pins
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led = Pin(LED_PIN, Pin.OUT)
servo = PWM(Pin(SERVO_PIN), freq=50)

# Setup Rain Sensor ADC (0 - 3.3V range)
adc = ADC(Pin(RAIN_PIN))
adc.atten(ADC.ATTN_11DB)

def set_servo_angle(angle):
    # Standard 50Hz PWM pulse width range (0.5ms to 2.5ms)
    min_duty = 1638
    max_duty = 8192
    duty = min_duty + int(angle * (max_duty - min_duty) / 180)
    servo.duty_u16(duty)

def read_rain_sensor():
    raw_val = adc.read_u16()
    voltage = (raw_val / 65535) * 3.3
    return raw_val, voltage

system_on = False
last_button = 1
current_angle = 80

last_sample_time = time.ticks_ms()
rain_start_time = None  # Tracks continuous 0V duration

# Initial state: LED OFF, Servo at 10°
led.value(0)
set_servo_angle(80)

print("System ready. Press D5 button to turn light ON/OFF...")

while True:
    current_button = button.value()

    # Detect button click (toggle system ON/OFF)
    if last_button == 1 and current_button == 0:
        system_on = not system_on
        print("System Power Toggled:", "ON" if system_on else "OFF")
        time.sleep(0.2)  # Debounce delay

    last_button = current_button

    if system_on:
        # 1. Turn status light ON
        led.value(1)

        raw, voltage = read_rain_sensor()

        # 2. Print recorded voltage every 1 second
        if time.ticks_diff(time.ticks_ms(), last_sample_time) >= 1000:
            last_sample_time = time.ticks_ms()
            print("Recorded Voltage: {:.2f}V".format(voltage))
            if rain_start_time is not None:
                elapsed = time.ticks_diff(time.ticks_ms(), rain_start_time)
                print("Rain continuous for: {}s".format(elapsed // 1000))

        # 3. Rain Detection Logic
        if voltage <= 0:  # Rain detected (~0V)
            if rain_start_time is None:
                rain_start_time = time.ticks_ms()

            elapsed_rain_time = time.ticks_diff(time.ticks_ms(), rain_start_time)

            # Rotate to 0° ONLY after 0V is sustained for 3 seconds (3000 ms)
            if elapsed_rain_time >= 2700:
                if current_angle != 0:
                    print("Rain sustained for 3s ({:.2f}V)! Rotating servo to 90°.".format(voltage))
                    set_servo_angle(0)
                    current_angle = 0

        else:  # Voltage > 0V (Dry condition)
            # Immediately reset timer and return motor to 90°
            if rain_start_time is not None or current_angle != 0:
                if current_angle != 80:
                    print("Voltage rose above 0V ({:.2f}V). Immediately returning servo to 0°.".format(voltage))
                rain_start_time = None
                set_servo_angle(80)
                current_angle = 80

    else:
        # System OFF: Light OFF, reset timer, return motor to 10°
        led.value(0)
        rain_start_time = None
        if current_angle != 80:
            set_servo_angle(80)
            current_angle = 80

    time.sleep(0.05)  # Fast sampling loop for instant recovery when dry
