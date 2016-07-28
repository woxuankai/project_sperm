#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import serial
if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	while True:		
		ser.write('ST,GS,+  4.876kg\r\n'.encode('utf-8'))
		time.sleep(0.5)
		print('sent')
