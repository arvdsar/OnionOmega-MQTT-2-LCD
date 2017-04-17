
#MQTT to LCD Display on Onion Omega
Example command line for using lcd.py from the original library:
python lcd.py -a 0x3f --line1="Test 1" --line2="Test 2"

I've updated the library (lcddriver.py) to write a string on line x starting at position y.
Find the sample code in mqtt2lcd.py and use it to create your own projects.

Copy the config.ini to myconfig.ini and update myconfig.ini with
your MQTT Broker IP address, username and password.

Run the application with:
python mqtt2lcd.py

A more specific version that I use for my own Domotica display can be found here:
https://github.com/arvdsar/OnionOmega-MQTT-2-LCD-For-Domotica


