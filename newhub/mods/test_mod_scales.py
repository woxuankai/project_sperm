#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import serial
import sys
if __name__ == '__main__':	
	while True:	
		ser = serial.Serial(sys.argv[1], 9600)
		ser.write('ST,GS,+  4.876kg\r\n'.encode('utf-8'))
		ser.close()
		time.sleep(0.5)
		print('sent')
