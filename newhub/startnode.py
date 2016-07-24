#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from thread_uploaddata import uploaddata
import serial, threading
from timestamp import disptimestamp
import time
def startnode(nodeinfo):
	time.sleep(nodeinfo['start_delay'])
	#a = 2/0
	#try:
	#	ser = serial.Serial(nodeinfo['devname'],nodeinfo['baudrate'])
	#except Exception as e:
	#	print('failed to open serial port!')
	#	raise e
	ser = serial.Serial(nodeinfo['devname'],nodeinfo['baudrate'])
	#successfully opened serial port, start to listen and report
	#flush input
	ser.flushInput()
	#ingore bad line
	data = ser.readline()
	timegap = nodeinfo['gap']
	while True:
		time.sleep(timegap)
		#now listen
		try:
			#flush input
			ser.flushInput()
			#ingore bad line
			data = ser.readline()
			#re_read
			data = ser.readline()
			data = data.decode('utf-8')
		except Exception as e:
			print('error occured while reading data from serial port')
			print('node: {}'.format(nodeinfo['nodename']))
			print('details:\n',e)
			continue
		disptimestamp()
		print('node id: ', nodeinfo['id'],' :data received')
		#start a new thread to upload data
		t = threading.Thread(target=uploaddata,args=(data,nodeinfo))
		t.start()
	#shouldn't come here if everything is ok
	#return 0

import time
def startnodetest(nodeinfo):
	data='	  5.6234				 '
	#start a new thread to upload data
	while True:
		t = threading.Thread(target=uploaddata,args=(data,nodeinfo))
		t.start()
		print("pretend received data")
		time.sleep(1)
