#Code for menu of the tank
#from os import CLD_KILLED
import time
import math
from pymata4 import pymata4
#from circuit2 import sonar_callback, sonar_report, sonar_setup
import matplotlib.pyplot as plt

arduino = pymata4.Pymata4()
distanceCm = 2
store = [0]
safeRange = [10,20]
safeTemp = [20,25]
levelCm = []
tempList = []


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
    time.sleep(0.1)

arduino.set_pin_mode_analog_input(0)

def return_temperature():

    V = arduino.analog_read(0)[0]

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

def plot_graph_30():
    global levelCm

    time = []
    for second in range(0,31):
        time.append(second)    

    if len(levelCm) < 31:
        return print("Graph can't be displayed: not enough values polled")
    else:
        last30Sec = levelCm[-31:]
        plt.plot(time,last30Sec,'k-',time,last30Sec,'co')
        plt.xlabel("Time (in seconds)")
        plt.ylabel("Liquid Level (in centimetres)")
        plt.axis([0,30,0,32])
        plt.title("Liquid level over the last 30 seconds")
        plt.show()

def plot_graph_60():
    global levelCm

    time = []
    for second in range(0,61):
        time.append(second)

    if len(levelCm) < 61:
        return print("Graph can't be displayed: not enough values polled")
    else:
        last60Sec = levelCm[-61:]
        plt.plot(time,last60Sec,'k-',time,last60Sec,'co')
        plt.xlabel("Time (in seconds)")
        plt.ylabel("Liquid Level (in centimetres)")
        plt.axis([0,60,0,32])
        plt.title("Liquid level over the last 60 seconds")
        plt.show()

def plot_graph_120():
    global levelCm

    time = []
    for second in range(0,121):
        time.append(second)

    if len(levelCm) < 121:
        return print("Graph can't be displayed: not enough values polled")
    else:
        last120Sec = levelCm[-121:]
        plt.plot(time,last120Sec,'k-',time,last120Sec,'co')
        plt.xlabel("Time (in seconds)")
        plt.ylabel("Liquid Level (in centimetres)")
        plt.axis([0,120,0,32])
        plt.title("Liquid level over the last 2 minutes")
        plt.show()

def plot_graph_temp():
    global tempList
    
    time = []
    for second in range(0,31):
        time.append(second)    

    if len(tempList) < 31:
        return print("Graph can't be displayed: not enough values polled")
    else:
        last30Sec = levelCm[-31:]
        plt.plot(time,last30Sec,'k-',time,last30Sec,'co')
        plt.xlabel("Time (in seconds)")
        plt.ylabel("Temperature (in degrees)")
        plt.axis([0,30,0,40])
        plt.title("Temperature over the last 30 seconds")
        plt.show()

def temp_alerts(temp):
    global safeTemp
    if temp < safeTemp[0]:
        print("The current temperature is TOO COLD... increase temperature")
        time.sleep(5)
    elif temp > safeTemp[1]:
        print("The current temperature is TOO HOT... decrease temperature")     
        time.sleep(5)
def menu():

    while True:
        print("Welcome to the chemical tank ")
        print("1: View graphs")
        print("View volume")
        print("3: View temperature")
        print("4: Change parameters")
        print("q: Quit the program")
        user = input()
        
        if user == "1":
            while True:
                print("What graph would you like to view?")
                print("1: Water volume")
                print("2: Temperature in the last 30 seconds")
                print("q: return to main menu")
                view = input()

                if view == "1":
                    while True:
                        print("For what duration would you like to see information?")
                        print("1: 30 seconds")
                        print("2: 1 minute")
                        print("3: 2 minutes")
                        print("q: return to previous menu")
                        duration = input()
         
                        if duration == "1":
                            plot_graph_30()
                            break
                        elif duration == "2":
                            plot_graph_60()
                            break
                        elif duration == "3":
                            plot_graph_120()
                            break
                        elif duration == "q":
                            break
                        else:
                            print("Please select from 1, 2, or 3")
                    
                if view == "2":
                    plot_graph_temp()
        
        if user == "2":
            print("Control + c to return to main menu")
            while True:
                try:
                    print(sonar_report())
                except KeyboardInterrupt():
                    menu()

        if user == "3":
            print("Control + c to return to main menu")
            while True:
                try:
                    print(return_temperature())
                except KeyboardInterrupt():
                    menu()

        if user == "4":
            while True:
                print("Please select the parameter to change")
                print("1: Safe water volume range")
                print("2: Safe temperature range")
                print("q: return to main menu")
                parameter = input()

                if parameter == "1":
                    global safeRange
                    while True:
                        try:
                            while True:
                                print(f"Current lower bound is {safeRange[0]}")
                                print("Enter new lower bound")
                                lowBound = int(input())
                                if lowBound >= 5 and lowBound <= 15:
                                    safeRange[0] = lowBound
                                    break
                                else:
                                    print("Please input a value between 5 and 15")
                            while True:
                                print(f"Current upper bound is {safeRange[1]}")
                                print("Enter new upper bound")
                                upBound = int(input())
                                if upBound <= 25 and upBound >= 15:   
                                    safeRange[1] = upBound
                                    break
                                else: 
                                    print("Please input a value between 15 and 25")
                        
                        except ValueError:
                            print("Please input a number")
                        break
                
                if parameter == "2":
                    global safeTemp
                    while True:
                        try:
                            print(f"Current lower bound is {safeTemp[0]}")
                            print("Enter new lower bound")
                            lowTemp = int(input())
                            safeTemp[0] = lowTemp

                            while True:
                                print(f"Current upper bound is {safeTemp[1]}")
                                print("Enter new upper bound")
                                upTemp = int(input())
                                if upTemp > lowTemp:   
                                    safeTemp[1] = upTemp
                                    break
                                else: 
                                    print("Please input a value bigger than the lower bound")
                        
                        except ValueError:
                            print("Please input a number")
                        break

                if parameter == "q":
                    break
                        
        if user == "q":
            print("Exiting the program...")
            break
        
        
#Continuously run ultrasonic sensor until user wants information
while True:
    try:
        sonar_setup(arduino,4,5)
        levelCm.append(sonar_report())
        if len(levelCm) == 122:
            levelCm.pop(0)
        tempList.append(return_temperature())
        if len(tempList) == 62:
            tempList.pop(0)
        temp_alerts(return_temperature())
        

    #once the user wants to use the menu
    except KeyboardInterrupt:
        menu()


    
