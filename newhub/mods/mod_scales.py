#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parsedata(data):
    return float(data[6:14].replace(' ',''))

import logging, os, time
from postdata import postdata
import serial

def run(nodeinfo, logger):
	logger.info('hello, this is a scales mod')
	#	opened serial port and test
	try:
		ser = serial.Serial(nodeinfo['devname'],nodeinfo['baudrate'])
		#	flush input
		ser.flushInput()
		#	ingore bad line
		#ser.readline()
	except:
		logger.exception('failed to open or init serial port')
		exit(1)
	try:
		timeinterval = nodeinfo['interval']
		srvaddr = nodeinfo['srvaddr']
		scalesid = nodeinfo['scalesid']
	except:
		logger.exception('missing config para')
		exit(1)
	num = 0
	while True:
		num = num + 1
		#listen and grab data
		try:
			time.sleep(timeinterval)
			#flush input
			ser.flushInput()
			#ingore bad line
			data = ser.readline()
			#re_read
			data = ser.readline()
			data = data.decode('utf-8')
		except Exception as e:
			logger.exception('failed to read data from serial port')
			exit(1)
		logger.info('#{} data received'.format(num))
		#parse data
		try:
			weight = parsedata(data)
		except Exception as e:
			logger.exception('failed to parse data')
			continue
		#fork a new thread to post data
		try:
			pid = os.fork()
		except:
			logger.exception('failed to first fork')
		if pid == 0:
			#	the child process/the second parent process
			#	do #2 fork
			try:
				pid = os.fork()
			except:
				logger.exception('failed to do #2 fork')
				exit(1)#no one cares exit code here
			if pid == 0:
				#the second child process
				try:
					postdata(srvaddr, scalesid, weight)
				except:
					logger.exception('#{} failed to post'.format(num))
					exit(1)
				logger.info('#{} data posted'.format(num))
				exit(0)
			#	the second parent process
			exit(0)
		#	the parent process
		##	wait for the second parent process exit
		os.wait()
	#end while
	#shouldn't come here if everything is ok
	logger.error('unexcept error: fun run in mod scales should not return')
	return 0
