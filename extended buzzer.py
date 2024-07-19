import time 

from pymata4 import pymata4
myArduino = pymata4.Pymata4()

distanceCm = 2
store = [0]
levelCm = []

myArduino.set_pin_mode_digital_output(2)

def sonar_callback(data):
    value = data[distanceCm]
    store[0] = value

def sonar_report():
    pass
    #TODO add a return statement
    # return the distance measured by the ultrasonic in CM, for use in your code
    return store[0]

def sonar_setup(myBoard, triggerPin, echoPin):
    #Set the pin mode for a sonar device. Results will appear via the callback.

    #TODO try different values of timeout - what does this change?
    myBoard.set_pin_mode_sonar(triggerPin, echoPin, sonar_callback, timeout=200000)
    #what does sonar_callback do?

    #TODO try different values of sleep - what does this change?
    time.sleep(1)

def operating_extended_buzzer():
    last3Values = levelCm[-3:] 
 
    numberOfFullValues = 0

    for value in last3Values:
        if value > 3 and value < 6 or value > 7 and value < 10:
            numberOfFullValues += 1 
    print(numberOfFullValues)

    if numberOfFullValues == 3:
        myArduino.digital_pin_write(2,1)
        time.sleep(5)
        myArduino.digital_pin_write(2,0)

while True:
    try:
        sonar_setup(myArduino,13,12)
        
        levelCm.append(sonar_report())
        operating_extended_buzzer()
        print(sonar_report())

        if len(levelCm) == 122:
            levelCm.pop(0)
        

    #once the user wants to use the menu
    except KeyboardInterrupt:
        myArduino.shutdown()
 