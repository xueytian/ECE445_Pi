
import argparse
import pi
import serial
# from serial import Serial
import time

ser =  serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()
time.sleep(0.1)

while True:
    try:
        if (ser.in_waiting > 0):
            fromAtmega = ser.readline().decode('utf-8').rstrip()
            print("Object detect signal: ",fromAtmega)
#             species = pi.object_detection()
#             print("species: ",species)
            time.sleep(0.5)

    #                 if(fromAtmega == '1'):
                # start object detection
    #                      species = pi.object_detection()
    #                      print("species: ",species)
                #if bird detected
    #                  if(species == 2):
    #                      pi.insert_data(2, species)  # save bird data to web
    #                     ser.write(b"YES\n")  #tell Atmega to load food
    #                     fromAtmega = ser.readline().decode('utf-8').rstrip()
    #                     if(fromAtmega == "food_shortage"):
    #                         pi.insert_data(1)

    except UnicodeDecodeError:
        pass
