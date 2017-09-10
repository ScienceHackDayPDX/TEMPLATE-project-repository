This project was the result of the two-day [Science Hack Day PDX](http://portland.sciencehackday.org/) event. The objective was to display the [global temperature anomaly](https://www.ncdc.noaa.gov/monitoring-references/faq/anomalies.php) from the recorded years 1880 - 2017. Using [data](https://www.ncdc.noaa.gov/cag/time-series/global/globe/land/1/7/1880-2017.csv
) from NOAA we experimented with an Arduino Uno to manipulate the browser display of the data set.  

# Requirements
## Hardware
* Arduino Uno

## Software
* Arduino IDE
* python 2.7
* On your command line:
```  
# Use your package manager to
$ install pip

# then for Mac: 
$ brew install portaudio  

# then: 
$ sudo pip install flask requests serial pyaudio 
```

# Usage
* Clone this repository
* Connect your Arduino 
* Install the Arduino IDE to program the Arduino
* Discover your serial port name:
```
# Before connecting Arduino:
$ ls /dev/ >> ~/before.txt

# After connecting Arduino:
$ ls /dev/ >> ~/after.txt

# Find the new device:
$ diff ~/before.txt ~/after.txt

# On Mac OS, the device will be something like /dev/tty.usbmodem14611.
# On Linux, the device will be something like /dev/ttyACM0
```
* Update the `ser` variable on line 34 in `climate.py` with your serial port
* In your terminal:
```
$ cd climate
$ python climate.py
# Some systems need to run: $ python2 climate.py
```
* In the browser navigate to [localhost:5000](localhost:5000)
* Manipulate the Arduino to change the output in the browser
