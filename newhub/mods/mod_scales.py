#!/usr/bin/env python3
# -*- coding: utf-8 -*-


				nodelogger = logging.getLogger(nodename+'_logger')
				nodelogger.setLevel(logging.DEBUG)
				stimenow = time.strftime('%Y_%m_%d_%X_%z', time.localtime())
				logfilepath = logfilepathtemplate.format(nodename,stimenow)
				logfilepath = path2abolutepath(logfilepath)
				logfile_handler = logging.FileHandler(logfilepath)
				#logfile_handler = logging.StreamHandler()
				logfile_handler.setFormatter(formatter)
				nodelogger.addHandler(logfile_handler)
			except Exception:
				logger.exception('failed to init logger for {}'.format(nodename))
				exit(-1)
			nodelogger.info("I'm process for node: {}".format(nodename))
			try:
				nodeinfo['nodename'] = nodename
				startnode(nodeinfo)
				#startnodetest(nodeinfo)


def parsedata(data):
    return float(data[6:14].replace(' ',''))

import logging
from postdata import postdata
def uploaddata(data, nodeinfo):
	try:
		weight = parsedata(data)
	except Exception as e:
		logger.exception("error data format")
		return 0
	try:
		postdata(nodeinfo['srvaddr'], nodeinfo['id'] , weight)
	except Exception as e:
		logger.exception("failed to post: ",e)
	else:
		logger.info('node id: ', nodeinfo['id'],' :data posted')
	finally:
		return 0

import serial, threading
from timestamp import disptimestamp
import time

def startnode(nodeinfo):
	logger = logging.getLogger(nodeinfo['nodename']+'_logger')
	deamonlogger = 	logging.getLogger('deamon_logger')
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
			logger.exception('error occured while reading data from serial port')
			continue
		logger.info('node id: ', nodeinfo['id'],' :data received')
		#start a new thread to upload data
		t = threading.Thread(target=uploaddata,args=(data,nodeinfo))
		t.start()
	#shouldn't come here if everything is ok
	#return 0

import time
def startnodetest(nodeinfo):
	data='	  5.6234				 '
	logger = logging.getLogger(nodeinfo['nodename']+'_logger')
	deamonlogger = 	logging.getLogger('deamon_logger')
	time.sleep(nodeinfo['start_delay'])
	timegap = nodeinfo['gap']
	while True:
		time.sleep(timegap)
		#now listen
		try:
			pass
		except Exception as e:
			logger.exception('error occured while reading data from serial port')
			continue
		logger.info('node id: ', nodeinfo['id'],' :data received')
		#start a new thread to upload data
		t = threading.Thread(target=uploaddata,args=(data,nodeinfo))
		t.start()
