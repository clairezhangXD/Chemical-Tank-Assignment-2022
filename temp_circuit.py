import time
from pymata4 import pymata4
import math
arduino = pymata4.Pymata4()
arduino.set_pin_mode_analog_input(0)

def return_temperature():
    V = arduino.analog_read(0)[0]


    while True:
        V = arduino.analog_read(0)[0]
        if V == 0:
            V = V + 1
        else:
            pass
        V1 = 1023 - V
        V2 = (V1/1023)*5
        R = ((V2*10000/5))/(1-(V2/5))
        temperature = -21.21*math.log(R/1000) + 72.203
        time.sleep(1)
        return temperature