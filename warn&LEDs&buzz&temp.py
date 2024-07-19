
from pymata4 import pymata4
import time 
import math

myArduino = pymata4.Pymata4()

myArduino.set_pin_mode_analog_input(0)
myArduino.set_pin_mode_digital_output(3)
myArduino.set_pin_mode_digital_output(4)
myArduino.set_pin_mode_digital_output(5)
myArduino.set_pin_mode_digital_output(2)

def return_temperature():
    V = myArduino.analog_read(0)[0]

    while True:
        V = myArduino.analog_read(0)[0]
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

def console_alerts(data):
    #Defining the safe range
        if data >= 12 and data <= 20:
             return
    #Low range
        while data >= 21 and data <= 26:
            time.sleep(wait)
            print("The current chemical level is lower than the safe range..... ")
            break
    #High range
        while data >= 6 and data < 12:
            time.sleep(wait)
            print("The current chemical level is higher than the safe range..... ")
            break
    #Critical high range
        while data > 3 and data < 6:
            time.sleep(wait)
            print("The current chemcical level is CRITICALLY FULL, drain immediately..... ")
            break
    #Critical low range
        while data > 26 and data < 30:
            time.sleep(wait)
            print("The current chemical level is CRITICALLY LOW, refill immediately..... ")
            break
    #Full capacity
        while data <= 3:
            time.sleep(wait)
            print("TANK EXCEEDED CAPACITY..... ")
            break
    #Empty capacity
        while data >= 30:
            time.sleep(wait)
            print("TANK FULLY EMPTY..... ")
            break

def operating_leds(data):
    #yellow if low or high
    #high
    if data >= 6 and data < 12 :
        myArduino.digital_pin_write(3,1)
        myArduino.digital_pin_write(4,0)
        myArduino.digital_pin_write(5,0)
    #low
    elif data >= 21 and data <= 26:
        myArduino.digital_pin_write(3,1)
        myArduino.digital_pin_write(4,0)
        myArduino.digital_pin_write(5,0)

    #red if near empty or near full
    #near full
    elif data > 3 and data < 6:
        myArduino.digital_pin_write(3,0)
        myArduino.digital_pin_write(4,1)
        myArduino.digital_pin_write(5,0)

    #near empty, which will also sound a buzzer connected in parallel
    elif data > 26 and data < 30:
        myArduino.digital_pin_write(3,0)
        myArduino.digital_pin_write(4,1)
        myArduino.digital_pin_write(5,0)

    #blue if overfull
    elif data <= 3:
        myArduino.digital_pin_write(3,0)
        myArduino.digital_pin_write(4,0)
        myArduino.digital_pin_write(5,1)

    #otherwise, LEDs off
    else:
        myArduino.digital_pin_write(3,0)
        myArduino.digital_pin_write(4,0)
        myArduino.digital_pin_write(5,0)
    
#if the last 3 polled values are all either near empty or near full, then a louder buzzer will sound    
def operating_extended_buzzer():
    last3Values = levelCm[-3:] 
 
    numberOfFullValues = 0

    for value in last3Values:
        if value > 3 and value < 6 or value > 26 :
            numberOfFullValues += 1 

    if numberOfFullValues == 3:
        myArduino.digital_pin_write(2,1)
        time.sleep(5)
        myArduino.digital_pin_write(2,0)

distanceCm = 2
wait = 5
store = [0]

def sonar_callback(data):
    value = data[distanceCm]
    store[0] = value

def sonar_report():
    pass
    return store[0]

def sonar_setup(myBoard, triggerPin, echoPin):
    myBoard.set_pin_mode_sonar(triggerPin, echoPin, sonar_callback, timeout=200000)
    time.sleep(1)

levelCm = []

try:
    while True:
        
        sonar_setup(myArduino,13,12)
        operating_leds(sonar_report())
        console_alerts(sonar_report())
        operating_extended_buzzer()
        levelCm.append(sonar_report())

        if len(levelCm) == 122:
            levelCm.pop(0)
        
except KeyboardInterrupt:
    myArduino.shutdown()  





    
