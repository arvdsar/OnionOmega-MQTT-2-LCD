#The MIT License (MIT)
#
#Copyright (c) [2016] [David "Fires" Stein] [http://davidstein.cz]
#
#Based on RPI I2C backpack from Michael Horne at http://www.recantha.co.uk/blog/?p=4849
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#Updated 17-4-2017 - Alexander van der Sar [http://www.vdsar.net]
#Write MQTT messages to LCD display
#Based on the Onion Omega Fire i2c LCD library of David Stein
#at [http://davidstein.cz/onion-omega-firei2clcd-lib/]
#
#Implements updated lcddriver.py which contains function to start writing the string
#from position. lcd_display_string_position();

import paho.mqtt.client as mqtt  #import the client1
import time
import lcddriver   
import configparser
config = configparser.ConfigParser()
config.read('myconfig.ini')


#from time import * 
lcd = lcddriver.lcd(0x3F)  
lcd.backlightOn() 

#initialize values at start of program. Contains the values received via MQTT
content = {
    'energy/solar/actual': '0',
    'energy/solar/totalactual': '0',
}


def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id  "+str(client)
    print(m)

def on_message(client1, userdata, message):
    print("message received  "  ,str(message.payload.decode("utf-8")))
    print("Topic: ",str(message.topic))
    content[message.topic] = message.payload #Put values from MQTT into the content Array.
    print "Solar Actual: ", content['energy/solar/actual']



#Screen definition 1 - Example of how you can write text on specific positions on the lcd
#For more examples on a complete layout of multiple screens you can check my other repository at
#https://github.com/arvdsar/OnionOmega-MQTT-2-LCD-For-Domotica

def screen_1():
    
    #write A: on Line 1
    lcd.lcd_display_string("A: ",1); 
    
    #write value of energy/solar/actual on line 1 starting at position 9 - length of value of energy/solar/actual
    lcd.lcd_display_string_position(content['energy/solar/actual'],1,9-len(content['energy/solar/actual'])); 
    
    #write "W   C:" on line 1 starting at position 9
    lcd.lcd_display_string_position("W   C:",1,9);
    
    #write value of energy/solar/totalactual on line 1 starting at position 20 - length of value of energy/solar/actual 
    lcd.lcd_display_string_position(content['energy/solar/totalactual'],1,20-len(content['energy/solar/totalactual']));
    
    #Write a W at line 1 position 20
    lcd.lcd_display_string_position("W",1,20); 

 
  
broker_address=config['DEFAULT']['Broker']
client1 = mqtt.Client("P1")    		#create new instance
client1.on_connect= on_connect      #attach function to callback
client1.on_message=on_message       #attach function to callback
#config['DEFAULT']['User'] is a value from the myconfig.ini
client1.username_pw_set(username=config['DEFAULT']['User'],password=config['DEFAULT']['Password'])

time.sleep(1)
client1.connect(broker_address)      #connect to broker
client1.loop_start()    #start the loop
client1.subscribe("energy/#")
#client1.subscribe("home/outdoor/#")

client1.publish("python","SomeText_to_Publish")
while 1:
	screen_1() 	   #(Re)Build screen 1		
	time.sleep(5); #wait 5 seconds

client1.disconnect()
client1.loop_stop()
                 
