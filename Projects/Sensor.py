# William Cariveau, Brenton Schnider, Elliot Robbins
# The code is intended to find the baseline resistivity of the sensor we made in lab
# Code written on 9/28/26
# AI was used to turn the code from program6 into one that could be used for the sensor we made.

from machine import ADC
import time

# Initialize ADC on pin A3
adc = ADC("A3")

def read_sensor():
    # Read 16-bit raw value (0 to 65535)
    raw_value = adc.read_u16()
    
    # Calculate voltage (0.0V to 3.3V)
    voltage = (raw_value / 65535) * 3.3
    
    return raw_value, voltage

# Example loop testing pin A3
while True:
    raw, voltage = read_sensor()
    print("Raw Value: {}, Voltage: {:.3f}V".format(raw, voltage))
    time.sleep(1)
