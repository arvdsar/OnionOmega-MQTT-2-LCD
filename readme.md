

Example command line for using lcd.py from the original library:
python lcd.py -a 0x3f --line1="Test 1" --line2="Test 2"

To use the MQTT to LCD Display code:
Copy the config.ini to myconfig.ini and update myconfig.ini with
your MQTT Broker IP address, username and password.
Edit mqtt2lcd.py and implement your MQTT topics to listen for.

python mqtt2lcd.py


Currently a very early version, just for trying the library and learning GIT too. 


