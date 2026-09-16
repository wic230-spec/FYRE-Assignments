# William Cariveau, Brenton Schnider, Elliot Robbins
# The code is intended to record the voltage transmitted through a circuit board under varying conditions
# Code written on 9/16/26
#AI was used to turn the idea of how the program would work into actual execution

# This block records the voltage data.
from machine import ADC
import time

adc = ADC("A0")

print("START")

while True:
    value = adc.read_u16()
    voltage = (value / 65535) * 3.3

    print("{},{:.3f}".format(value, voltage))

    time.sleep(0.1)

# This block downloads the data and exports it to Excel
import serial
import os
import time

PORT = "COM7"
BAUD = 115200

filename = os.path.join(
    os.path.expanduser("~"),
    "Downloads",
    "output.csv"
)

print("Connecting to", PORT)

ser = serial.Serial(PORT, BAUD, timeout=2)

# ESP32 often resets when the serial connection opens
time.sleep(2)

print("Connected!")
print("Saving to:", filename)
print("Waiting for data...")

with open(filename, "w", newline="") as file:

    # CSV header
    file.write("ADC,Voltage\n")
    file.flush()

    try:
        while True:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if line:
                print("Received:", line)

                # Don't put the START message in the CSV
                if line != "START":
                    file.write(line + "\n")
                    file.flush()

    except KeyboardInterrupt:
        print("\nStopped.")

ser.close()
