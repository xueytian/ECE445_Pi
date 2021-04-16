#!/usr/bin/env python3
import argparse
import pi
import serial
import time

ser = serial.Serial('/dev/USB0', 9600, timeout=1)
ser.flush()
time.sleep(0.1) #wait for serial to open
if ser.isOpen():
    print("Atmega is open right now")
    while True:
        if(ser.inWaiting>0):
            fromAtmega = ser.readline().decode('utf-8').rstrip()
            print("object detect signal:", fromAtmega)
            if(fromAtmega == '1'):
                # start object detection
                species = pi.object_detection()
                print("species: ",species)

                #if Squirrel detected
                if(species == 1):
                    ser.write(b"Squirrel\n")  #tell Atmega to load food
                #if bird detected
                elif(species == 2):
                    pi.insert_data(2, species)  # save bird data to web
                    ser.write(b"Bird\n")  #tell Atmega to load food
                    fromAtmega = ser.readline().decode('utf-8').rstrip()
                    if(fromAtmega == "food_shortage"):
                        pi.insert_data(1)
            ser.flushInput()
