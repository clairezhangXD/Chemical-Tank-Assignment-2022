import time

PASS = "ENG1013"

def security():
    ctr = 0
    while ctr!="TRUE": 
        if ctr==3:
            print("Wait 4 secs before trying again !!!")
            time.sleep(4)  
            ctr = 0
        
        elif ctr<3 :
            passwrd = input("Enter the password : ")
            ctr = pass_check(passwrd,ctr)

def pass_check(password,ctr) :
    if password == PASS:
        print("CORRECT PASSWORD")
        ctr="TRUE"
    else :
        ctr = ctr+1
        print("INCORRECT PASSWORD")
    return ctr

security()




    
        
    
