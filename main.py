
#time imports
import time
import datetime

import os
import requests
domain = "192.168.1.11"

#serial
import serial


ser = serial.Serial(
        # Serial Port to read the data from
        port='/dev/ttyACM0',

        #Rate at which the information is shared to the communication channel
        baudrate = 115200,

        #Applying Parity Checking (none in this case)
        parity=serial.PARITY_NONE,

       # Pattern of Bits to be read
        stopbits=serial.STOPBITS_ONE,
     
        # Total number of bits to be read
        bytesize=serial.EIGHTBITS,

        # Number of serial commands to accept before timing out
        timeout=0.2
    )

#impoprt json
import json

#temperature imports
import board
import adafruit_dht
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

#display modules
import I2C_LCD_DRIVER
mylcd = I2C_LCD_DRIVER.lcd()
mylcd.lcd_clear()

#pi board setup
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#button pins
button4 = 25
button3 = 8
button2 = 7
button1 = 1
#button setup
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#relay pin setup
#water pump relay
relay1 = 6

#fan relay
relay2 = 13

#vacant relays
relay3 = 19
relay4  = 26
#all relay is LOW=ON HIGH = OFF

#setpins to output
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3, GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)

#inital OFF all relays
GPIO.output(relay1, GPIO.HIGH)
GPIO.output(relay2, GPIO.HIGH)
GPIO.output(relay3, GPIO.HIGH)
GPIO.output(relay4, GPIO.HIGH)

#leds setup
pumpLed = 21
fanLed = 20

GPIO.setup(pumpLed, GPIO.OUT)
GPIO.setup(fanLed, GPIO.OUT)
#inital OFF all leds
GPIO.output(pumpLed, GPIO.LOW)
GPIO.output(fanLed, GPIO.LOW)



try:
    x = requests.get('http://{}/sensor/request/control'.format(domain))
    command = x.json()
    if str(command['result'] == 'true'):
        OnID = command['sensor']['OnID']
        print("OnID is :{}".format(OnID))
    else:
        OnID = 0
        print("OnID set to default")
except Exception as e:
    
    print(e)
    print("check internet")
    
    


def manualOps():
    global curMenu
    mylcd.lcd_clear()
    #reading buttons
    #controlling relays
   
    mylcd.lcd_display_string("Manual Switching", 1, 2)
    mylcd.lcd_display_string("Water Pump: OFF" , 2, 0)
    mylcd.lcd_display_string("Fan: OFF" , 3,0)
    mylcd.lcd_display_string("Humidifier: OFF" , 4,0)
    
    
    while 1:
        #print('jare ako diri')
        #button1 and relay 1 water pump
        if GPIO.input(button1)==False:
            print("button1 pressed")
            #print(GPIO.input(relay1))
            if GPIO.input(relay1)==0:
                GPIO.output(relay1, GPIO.HIGH)
                GPIO.output(pumpLed, GPIO.LOW)
                print("Relay1 is OFF")
                mylcd.lcd_display_string("Water Pump: OFF" , 2, 0)
                time.sleep(1)
            else:
                GPIO.output(relay1, GPIO.LOW)
                GPIO.output(pumpLed, GPIO.HIGH)
                print("Relay1 is ON")
                mylcd.lcd_display_string("Water Pump:    " , 2, 0)
                mylcd.lcd_display_string("Water Pump: ON" , 2, 0)
                time.sleep(1)
        #button2
        if GPIO.input(button2)==False:
            print("button2 pressed")
            #print(GPIO.input(relay2))
            if GPIO.input(relay2)==0:
                GPIO.output(relay2, GPIO.HIGH)
                GPIO.output(fanLed, GPIO.LOW)
                print("Relay2 is OFF")
                mylcd.lcd_display_string("Fan: OFF" , 3,0)
                time.sleep(1)
            else:
                GPIO.output(relay2, GPIO.LOW)
                GPIO.output(fanLed, GPIO.HIGH)
                print("Relay2 is ON")
                mylcd.lcd_display_string("Fan:    " , 3,0)
                mylcd.lcd_display_string("Fan: ON" , 3,0)
                time.sleep(1)
            
            
        #button3
        if GPIO.input(button3)==False:
            print("button3 pressed")
            #print(GPIO.input(relay3))
            if GPIO.input(relay3)==0:
                GPIO.output(relay3, GPIO.HIGH)
                print("Relay3 is OFF")
                mylcd.lcd_display_string("Humidifier: OFF" , 4,0)
                time.sleep(1)
            else:
                GPIO.output(relay3, GPIO.LOW)
                print("Relay3 is ON")
                mylcd.lcd_display_string("Humidifier:    " , 4,0)
                mylcd.lcd_display_string("Humidifier: ON" , 4,0)
                time.sleep(1)
        #button4
        if GPIO.input(button4)==False:
            print("button4 pressed")
            curMenu = curMenu +1
            print(curMenu)
            time.sleep(0.5)
            break
            
def main():
    global curMenu
    global ph
    global arduinoSerial
    
    global phSet
    global tempSet
    global humSet
    
    global json_delay
    global OnID
    mylcd.lcd_clear()
    

    mylcd.lcd_display_string("Status ", 1, 2)   
    dailySec = dailyTimer * 24  * 3600

    postSec = postTimer
    pumpSec = pumpTimer
    
    humidifierSec = 5
    
    start = time.time()

    daily = readingJSON()    
    dailySec_old = int(daily['dailySec'])
    dailySec = dailySec_old
         
    water_state = "disable"
    x  = 0
    while 1:
        #x = x + 1
        #print(x)
#         readTemp()
        
        ph  = arduinoPH()
            #ph = float(arduinoSer)
        
        mylcd.lcd_display_string("{}\337C".format(temp_c), 3,0)
        mylcd.lcd_display_string("{}\337F".format(temp_f), 3,5)
        
        if len(str(ph)) < 4:
            mylcd.lcd_display_string(" P: {}".format(ph), 3,12)
        else:
            mylcd.lcd_display_string(" P:{}".format(ph), 3,12)
        
        if len(str(humidity)) < 3:
            mylcd.lcd_display_string("Humidity(%): {}".format(humidity), 4,0)
        else:
            mylcd.lcd_display_string("Humidity(%):{}".format(humidity), 4,0)
         
        
        
        y = requests.get('http://{}/sensor/get/override'.format(domain))
        OR = y.json()
        
        if OR['Override']['Override'] == '1':
            #get data from server 
            try:
                x = requests.get('http://{}/sensor/request/control'.format(domain))
                command2 = x.json()
                    
                #humidifier
                if command2['sensor']['Humidifier'] == "1":
                    GPIO.output(relay3, GPIO.LOW)
                    #print("humidifier is ON")
                else:
                    GPIO.output(relay3, GPIO.HIGH)
                    #print("humidifier is OFF")
                #fan
                if command2['sensor']['Fan'] == '1':
                    GPIO.output(relay2, GPIO.LOW)
                    GPIO.output(fanLed, GPIO.HIGH)
                    print("fan Relay is ON")
                else:
                    GPIO.output(relay2, GPIO.HIGH)
                    GPIO.output(fanLed, GPIO.LOW)
                    #print("fan Relay is OFF")
                
                #waterpump
                if command2['sensor']['waterpump'] == '1':
                    #turn on the pump relay
                    GPIO.output(relay1, GPIO.LOW)
                    GPIO.output(pumpLed, GPIO.HIGH)
                    
                else:
                    #turns off the pump realy
                    GPIO.output(relay1, GPIO.HIGH)
                    GPIO.output(pumpLed, GPIO.LOW)
                
                postingData()
                OnID = command2['sensor']['OnID']
                    
            except Exception as e:
                print("no internet")
                print(e)
        else:
            if temp_c > tempSet:
                GPIO.output(relay2, GPIO.LOW)
                GPIO.output(fanLed, GPIO.HIGH)
                #print("fan Relay is ON")
                
            else:
                GPIO.output(relay2, GPIO.HIGH)
                GPIO.output(fanLed, GPIO.LOW)
                #print("fan Relay is OFF")
                
            GPIO.output(relay1, GPIO.HIGH)
            GPIO.output(pumpLed, GPIO.LOW)
            
        
        if water_state == "disable":
            mylcd.lcd_display_string("Status", 1, 2)
            mylcd.lcd_display_string("Daily:  " , 2, 0)
            
            val = str(datetime.timedelta(seconds=dailySec))
            date2 = val.replace(" day,", "")
            date = date2.replace(" days,", "")
            
            mylcd.lcd_display_string( date  , 2 ,7)
        else:
            mylcd.lcd_display_string( "Pump is Ready     "  , 2 ,0)
            
        #print compate temps
        #print('{} {}'.format(tempSet, temp_c))
        
            
        #print(postSec)
        ### When 1 sec or more has elapsed...
        if time.time() - start > 1:
            start = time.time()
            postSec = postSec - 1
            
            #humidifier loop
            humidifierSec = humidifierSec - 1
            
            
            if OR['Override']['Override'] == '0':
                if(humidifierSec <= 0):
                    if(temp_c > humSet):
                        if GPIO.input(relay3)==0:
                            GPIO.output(relay3, GPIO.HIGH)
                            print("humidifier is OFF")
                        else:
                            GPIO.output(relay3, GPIO.LOW)
                            print("humidifier is ON")
                        humidifierSec = 5
            
                
            if(dailySec > 0 ):
                dailySec = dailySec - 1
                
                #save to json file
                dailyJSON(dailySec)
                
                #refresh lcd digits
                mylcd.lcd_display_string("Daily:              " , 2, 0)
                #mylcd.lcd_display_string("   " , 4, 13)

            ### This will be updated once per second
            print ("%s seconds remaining" % dailySec)
            
            #reafding
            
            if(ph < phSet):
#                 print(phSet)
#                 print(ph)
                if(water_state == "enable"):
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Pump Running!" , 2 , 2)
                    print(pumpSec)
                    #turn on the pump relay
                    GPIO.output(relay1, GPIO.LOW)
                    GPIO.output(pumpLed, GPIO.HIGH)
                    #wait for the duration
                    time.sleep(pumpSec)
                    #turns off the pump realy
                    GPIO.output(relay1, GPIO.HIGH)
                    GPIO.output(pumpLed, GPIO.LOW)
                    
                    water_state  = "disable"
                    dailySec = dailyTimer * 24  * 3600
                   
            ### Countdown finished, ending loop
            if dailySec <= 0:
                water_state = "enable"
                dailyJSON(dailySec)
                
            if postSec <=0:
                print("readings here")
                print("posting data")
                #after actions resetting timer
                postSec = postTimer
                
                
        postingData()
        #select operation button
        if GPIO.input(button4)==False:
            #print(GPIO.input(relay2))
            if curMenu < 3:
                curMenu = curMenu +1
            else:
                curMenu = 1
            print(curMenu)
            time.sleep(0.5)
            break
            
        
def setOther():
    global phSet
    global tempSet
    global humSet
    
    global curMenu
    
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Setup:", 1,2)
    setupNum = 1
    while 1:
        if setupNum == 1:
            mylcd.lcd_display_string("    ", 1,8)
            mylcd.lcd_display_string("Ph", 1,8)
        elif setupNum == 2:
            mylcd.lcd_display_string("    ", 1,8)
            mylcd.lcd_display_string("Temp", 1,8)
        else:
            mylcd.lcd_display_string("    ", 1,8)
            mylcd.lcd_display_string("Hum", 1,8)
            
        mylcd.lcd_display_string("Set point Ph: {}".format(round(phSet, 1)), 2,0)
        mylcd.lcd_display_string("Set point Temp: {}".format(round(tempSet,1)), 3,0)
        mylcd.lcd_display_string("Set point Hum: {}".format(round(humSet,1)), 4,0)
        
        
        #button1 adding button
        if GPIO.input(button1)==False:
            #print("button1 pressed")
            if setupNum == 1:
                phSet = phSet + 0.1
            if setupNum == 2:
                tempSet = tempSet + 0.1
            if setupNum == 3:
                humSet = humSet + 0.1
                
        #button2 adding button
        if GPIO.input(button2)==False:
            #print("button1 pressed")
            if setupNum == 1:
                if phSet > 0:
                    phSet = phSet - 0.1
            if setupNum == 2:
                if tempSet > 0:
                    tempSet = tempSet - 0.1
            if setupNum == 3:
                if humSet > 0:
                    humSet = humSet - 0.1
                
        #button3 selecting
        if GPIO.input(button3)==False:
            if setupNum < 3:
                setupNum = setupNum + 1
                time.sleep(0.3)
            else:
                setupNum = 1
                time.sleep(0.3)
            print(setupNum)
        
        #select operation button
        if GPIO.input(button4)==False:
            #print(GPIO.input(relay2))
            settings2JSON(phSet,tempSet,humSet)
            
            if curMenu < 4:
                curMenu = curMenu +1
            else:
                curMenu = 1
            print(curMenu)
            time.sleep(0.5)
            break
    
def setTimer():
    global dailyTimer
    global pumpTimer
    global postTimer
    global curMenu
    
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Timer Setup:", 1, 0)
    
    setting = 1
    
    settingData = re_settingJSON()
    
    dailyTimer = int(settingData['dailyTimer'])
    pumpTimer = int(settingData['pumpTimer'])
    postTimer = int(settingData['postTimer'])
    
    
    curdailyTimer = dailyTimer
    
    while 1:
        mylcd.lcd_display_string("Delay Pump(day):{}".format(dailyTimer), 2, 0)
        mylcd.lcd_display_string("Pump Timer(sec):{}".format(pumpTimer), 3, 0)
        mylcd.lcd_display_string("Post Timer(min):{}".format(postTimer), 4, 0)
        
        #save setting on the json file
        
        settingsJSON(dailyTimer,pumpTimer,postTimer )
        
        if curdailyTimer != dailyTimer:
            dailyJSON(dailyTimer * 24  * 3600)
        
        if setting == 1:
            mylcd.lcd_display_string("Timer Setup:      ", 1, 0)
            mylcd.lcd_display_string("Timer Setup:Delay", 1, 0)
        if setting == 2:
            mylcd.lcd_display_string("Timer Setup:      ", 1, 0)
            mylcd.lcd_display_string("Timer Setup:Pump", 1, 0)
        if setting == 3:
            mylcd.lcd_display_string("Timer Setup:      ", 1, 0)
            mylcd.lcd_display_string("Timer Setup:Post", 1, 0)
            
        #button1 adding button
        if GPIO.input(button1)==False:
            #print("button1 pressed")
            mylcd.lcd_clear()
            if(setting == 1):
                dailyTimer = dailyTimer + 1
                mylcd.lcd_display_string("Delay Pump(day):   ", 2, 0)
            if(setting == 2):
                pumpTimer = pumpTimer + 1
                mylcd.lcd_display_string("Pump Timer(sec):   ", 3, 0)
            if(setting == 3):
                postTimer = postTimer + 1
                mylcd.lcd_display_string("Post Timer(sec):   ", 4, 0)
                        
                
            
        #button2 subtrating button
        if GPIO.input(button2)==False:
            print("button2 pressed")
            if(setting == 1):
                dailyTimer = dailyTimer - 1
                mylcd.lcd_display_string("Delay Pump(day):   ", 2, 0)
            if(setting == 2):
                pumpTimer = pumpTimer - 1
                mylcd.lcd_display_string("Pump Timer(sec):   ", 3, 0)
            if(setting == 3):
                postTimer = postTimer - 1
                mylcd.lcd_display_string("Post Timer(sec):   ", 4, 0)
                
        #button3 selecting
        if GPIO.input(button3)==False:
            if setting < 3:
                setting = setting + 1
                time.sleep(0.3)
            else:
                setting = 1
                time.sleep(0.3)
            print(setting)
            
        
        if GPIO.input(button4)==False:
            mylcd.lcd_clear()
            if curMenu < 4:
                curMenu = curMenu +1
            else:
                curMenu = 1
            print(curMenu)
            time.sleep(0.5)
            break

#creating json file with daily sec as parameter
def dailyJSON(sec):
    # Data to be written
    data = {
        "dailySec": "{}".format(sec)
    }
     
    # Serializing json
    json_object = json.dumps(data, indent=4)
 
    # Writing to sample.json
    with open("/home/user/Desktop/allprojects/phsensor/Final70/data.json", "w") as outfile:
        outfile.write(json_object)
        
#reading json file from daily seconds
def readingJSON():
    
    with open('/home/user/Desktop/allprojects/phsensor/Final70/data.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        return json_object

#writing settings to a json file
def settingsJSON(dailyTimer,pumpTimer,postTimer ):

    settings = {
        "dailyTimer": "{}".format(dailyTimer),
        "pumpTimer": "{}".format(pumpTimer),
        "postTimer": "{}".format(postTimer)
    }
     
    # Serializing json
    json_object = json.dumps(settings, indent=4)
 
    # Writing to sample.json
    with open("/home/user/Desktop/allprojects/phsensor/Final70/settings.json", "w") as outfile:
        outfile.write(json_object)
#writing settings to a json file
        
def settings2JSON(phSet,tempSet,humSet):

    settings2 = {
        "phSet": "{}".format(phSet),
        "tempSet": "{}".format(tempSet),
        "humSet" : "{}".format(humSet)
    }
     
    # Serializing json
    json_object = json.dumps(settings2, indent=4)
    # Writing to sample.json
    with open("/home/user/Desktop/allprojects/phsensor/Final70/settings2.json", "w") as outfile:
        outfile.write(json_object)
        
def re_setting2JSON():
    
    with open('/home/user/Desktop/allprojects/phsensor/Final70/settings2.json', 'r') as openfile:
        # Reading from json file
        settings2 = json.load(openfile)
        return settings2
    
    
#reading setting from a json file
def re_settingJSON():
    
    with open('/home/user/Desktop/allprojects/phsensor/Final70/settings.json', 'r') as openfile:
        # Reading from json file
        settings = json.load(openfile)
        return settings



arduinoSerial = 0
def arduinoPH():
    global arduinoSerial
    global temp_c
    global temp_f
    global humidity
    
    
    def isfloat(num):
        try:
            float(num)
            return True
        except:
            return False
    
    olddata = ser.readline().decode()
    newdata = olddata.rstrip().lstrip()
    
    if newdata:
        all_data = newdata.split('-')
    else:
        all_data = [0] * 5
         
    newdata =  all_data[0]

    #print(all_data)
    if isfloat(all_data[1]):
        if all_data[1] != 0 :
           temp_c = float(round(float(all_data[1]), 2))
           temp_f = round(temp_c * (9 / 5) + 32 , 2)
        
    if isfloat(all_data[2]):
        if all_data[2] != 0 :
           humidity = float(round(float(all_data[2]), 2))           
    
    if newdata != '0.0' and newdata != '25.5' and newdata != 0:
        if isfloat(newdata):
            temp = float(round(float(newdata), 2))
            if temp < 10:
                arduinoSerial = float(round(float(newdata), 2))
    return (arduinoSerial)


def postingData():
    global temp_c
    global humidity
    global ph
    
    #humidifier state
    if GPIO.input(relay3) == 0:
        humState = "1"
    else:
        humState = "0"
        
    #fan state
    if GPIO.input(relay2) == 0:
        fanState = "1"
    else:
        fanState = "0"
    
    #water pump
    if GPIO.input(relay1) == 0:
        pumpState = "1"
    else:
        pumpState = "0"
    
    url = 'http://{}/sensor/post/data'.format(domain)
    myobj = {
        'Humidity': '{}'.format(humidity),
        'Temperature' : '{}'.format(temp_c),
        'Ph' : '{}'.format(ph),
        'Humidifier' : '{}'.format(humState),
        'Fan' : '{}'.format(fanState),
        'WaterPumpEnable' : '{}'.format(pumpState)
             }
    print(myobj)
    x = requests.post(url, json = myobj)

    #print(x.text)

#state of main menu
curMenu = 1

#time variables from json
settingData = re_settingJSON()
    
dailyTimer = int(settingData['dailyTimer'])
pumpTimer = int(settingData['pumpTimer'])
postTimer = int(settingData['postTimer'])


#time2 variables from json
settingData2= re_setting2JSON()
phSet = round(float(settingData2['phSet']) ,2)
tempSet = round(float(settingData2['tempSet']),2)
humSet = round(float(settingData2['humSet']),2)
#phSet = 3.0
#tempSet = 30.0

#temps and humidity
temp_c = temp_f = humidity = 0
#ph var
ph = 0

#infinite loop
while 1:
    
    #try:
#   readTemp()
    if curMenu ==1:
        main()
    if curMenu == 2:
        manualOps()
    if curMenu == 3:
        setTimer()
    if curMenu == 4:
        setOther()
    
    #select operation button
    if GPIO.input(button4)==False:
        #print(GPIO.input(relay2))
        if curMenu < 4:
            curMenu = curMenu +1
        else:
            mylcd.lcd_clear()
            curMenu = 1
        print(curMenu)
        time.sleep(0.5)
    
    #except:
#         os.system('python3 main.py')
    
    
    
 