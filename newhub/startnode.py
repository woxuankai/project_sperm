#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from thread_uploaddata import uploaddata
import serial, threading
def startnode(nodeinfo):
    #try:
    #    ser = serial.Serial(nodeinfo['devname'],nodeinfo['baudrate'])
    #except Exception as e:
    #    print('failed to open serial port!')
    #    raise e
    ser = serial.Serial(nodeinfo['devname'],nodeinfo['baudrate'])
    #successfully opened serial port, start to listen and report
    #flush input
    ser.flushInput()
    #ingore bad line
    data = ser.readline()
    while True:
        #now listen
        try:
            data = ser.readline()
            data = data.decode('utf-8')
        except Exception as e:
            print('error occured while reading data from serial port')
            print('node: {}'.format(nodeinfo['nodename']))
            print('details:\n',e)
            continue
        #start a new thread to upload data
        t = threading.Thread(target=uploaddata,args=(data,nodeinfo))
        t.start()
    #shouldn't come here if everything is ok
    #return 0
