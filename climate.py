#!/usr/bin/env python
"""
duffel.py

Flask app for routing to Rail outputs on various hosts. Currently supports only
Amazon Cloud Drive. Requires https://github.com/yadayada/acd_cli is authorized
and set up as owner of shared directory.
"""
from flask import Flask, redirect, render_template, abort, request, Response
from werkzeug import Headers
from contextlib import closing
import json
import requests
import serial
import csv
import time
import random
import threading
import wave, sys, pyaudio
app = Flask(__name__)

# Change depending on device; discover serial port name by:
# Before connecting Arduino:
# `ls /dev/ >> ~/before.txt`
#
# After conencting Arduino:
# `ls /dev/ >> ~/after.txt`
#
# Find the new device:
# `diff ~/before.txt ~/after.txt`
#
# On Mac OS, the device will be something like /dev/tty.usbmodem14611.
# On Linux, the device will be something like /dev/ttyACM0
ser = serial.Serial('/dev/tty.usbmodem1411', 9600)

class KnobThread(threading.Thread):
    """ Gets knob value on separate thread. """
    def __init__(self):
        super(KnobThread, self).__init__()
        self.val = 0
        self.daemon = True
    def run(self):
        while True:
            val = ser.readline()
            self.val = int(val.strip().split(',')[0])

knob_thread = KnobThread()
knob_thread.start()


class MusicThread(threading.Thread):
    """ Gets knob value on separate thread. """
    def __init__(self):
        super(MusicThread, self).__init__()
        self.daemon = True
        # Bass drum taken from
        # http://bigsamples.free.fr/d_kit/bdkick/bt7a0d0.wav
        
        wf = wave.open('bdrum.wav')
        p = pyaudio.PyAudio()
        chunk = 1024
        self.chunks = []
        self.stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)
        data = wf.readframes(chunk)
        while data != '':
            self.chunks.append(data)
            data = wf.readframes(chunk)

    def run(self):
        while True:
            for chunk in self.chunks:
                self.stream.write(chunk)
            time.sleep(-.8 / 255 * knob_thread.val + 1)

music_thread = MusicThread()
music_thread.start()


# Global annual temperature anomaly data from 
# https://www.ncdc.noaa.gov/cag/time-series/global/globe/land/1/7/1880-2017.csv
year_to_anomaly = {
        1880: -0.33,
        1881: -0.36,
        1882: -0.55,
        1883: -0.34,
        1884: -0.68,
        1885: -0.51,
        1886: -0.21,
        1887: -0.40,
        1888: -0.23,
        1889: -0.30,
        1890: -0.18,
        1891: -0.42,
        1892: -0.33,
        1893: -0.16,
        1894: -0.31,
        1895: -0.29,
        1896: -0.18,
        1897: 0.01,
        1898: -0.39,
        1899: -0.23,
        1900: -0.18,
        1901: -0.05,
        1902: -0.43,
        1903: -0.39,
        1904: -0.51,
        1905: -0.20,
        1906: -0.19,
        1907: -0.50,
        1908: -0.31,
        1909: -0.31,
        1910: -0.12,
        1911: -0.37,
        1912: -0.50,
        1913: -0.36,
        1914: -0.16,
        1915: -0.06,
        1916: -0.22,
        1917: -0.19,
        1918: -0.35,
        1919: -0.16,
        1920: -0.16,
        1921: 0.05,
        1922: -0.16,
        1923: -0.31,
        1924: -0.07,
        1925: -0.33,
        1926: -0.26,
        1927: 0.05,
        1928: -0.10,
        1929: -0.32,
        1930: 0.07,
        1931: 0.19,
        1932: 0.11,
        1933: -0.10,
        1934: -0.08,
        1935: 0.02,
        1936: 0.31,
        1937: -0.02,
        1938: 0.10,
        1939: 0.07,
        1940: 0.19,
        1941: 0.25,
        1942: -0.09,
        1943: 0.06,
        1944: 0.17,
        1945: -0.11,
        1946: -0.05,
        1947: -0.02,
        1948: 0.03,
        1949: -0.15,
        1950: -0.32,
        1951: 0.06,
        1952: 0.15,
        1953: 0.02,
        1954: -0.12,
        1955: -0.18,
        1956: -0.26,
        1957: -0.20,
        1958: 0.01,
        1959: 0.09,
        1960: -0.11,
        1961: 0.00,
        1962: -0.00,
        1963: 0.20,
        1964: -0.15,
        1965: -0.14,
        1966: 0.16,
        1967: -0.12,
        1968: -0.17,
        1969: 0.09,
        1970: 0.06,
        1971: -0.10,
        1972: -0.09,
        1973: 0.18,
        1974: 0.04,
        1975: 0.09,
        1976: -0.24,
        1977: 0.17,
        1978: -0.08,
        1979: 0.04,
        1980: 0.18,
        1981: 0.19,
        1982: 0.17,
        1983: 0.32,
        1984: 0.05,
        1985: -0.12,
        1986: 0.06,
        1987: 0.55,
        1988: 0.50,
        1989: 0.29,
        1990: 0.19,
        1991: 0.49,
        1992: -0.15,
        1993: 0.19,
        1994: 0.34,
        1995: 0.54,
        1996: 0.38,
        1997: 0.56,
        1998: 1.11,
        1999: 0.65,
        2000: 0.50,
        2001: 0.75,
        2002: 0.99,
        2003: 0.57,
        2004: 0.45,
        2005: 0.93,
        2006: 0.88,
        2007: 0.73,
        2008: 0.80,
        2009: 0.64,
        2010: 1.11,
        2011: 0.98,
        2012: 0.99,
        2013: 0.81,
        2014: 0.77,
        2015: 0.99,
        2016: 1.13,
        2017: 1.20 
    }

@app.route('/')
def page_to_reload():
    """ Returns page that is refreshed every
        argument of content attribute in
        meta http-equiv="refresh".
    """
    val = knob_thread.val
    year = int(val * 138./256 + 1880)
    return (
"""<!DOCTYPE html>
<html>
<head><meta http-equiv="refresh" content=".2">
<style>
h1 {{color:white; font-family: Arial; font-size: 9em}}
</style>

</head>
<body bgcolor="{color}0000">
<h1>YEAR {year}</h1><br />
<h1>ANOMALY {anomaly}&#176; </h1>
</body>
</html>
"""
    ).format(color=('%x' % val),
                year=year,
                anomaly=year_to_anomaly[year])


if __name__ == '__main__':
    app.run(debug=True)

