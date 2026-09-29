import serial
import time
import string
import pynmea2

port = "/dev/serial0"

ser = serial.Serial(port, baudrate=9600, timeout=0.5)

while True:
    newdata = ser.readline().decode('utf-8', errors='ignore')

    if newdata.startswith("$GPRMC"):
        try:
            newmsg = pynmea2.parse(newdata)
            lat = newmsg.latitude
            lng = newmsg.longitude

            gps = "Latitude = " + str(lat) + " and Longitude = " + str(lng)
            print(gps)

        except pynmea2.ParseError:
            continue
