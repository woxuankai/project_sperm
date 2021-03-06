#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def parsedata(data):
    return float(data[6:14].replace(' ', ''))

# def run(nodeinfo, logger):
#   logger.info('hello, this is a scales mod')
#   #   opened serial port and test
#   try:
#       ser = serial.Serial(nodeinfo['devname'],nodeinfo['baudrate'])
#       #   flush input
#       ser.flushInput()
#       ser.close()
#       #   ingore bad line
#       #ser.readline()
#   except:
#       logger.exception('failed to open or init serial port')
#       exit(1)
#   try:
#       timeinterval = nodeinfo['interval']
#       srvaddr = nodeinfo['srvaddr']
#       scalesid = nodeinfo['scalesid']
#   except:
#       logger.exception('missing config para')
#       exit(1)
#   num = 0
#   while True:
#       num = num + 1
#       #listen and grab data
#       try:
#           time.sleep(timeinterval)
#           ser = serial.Serial(nodeinfo['devname'],nodeinfo['baudrate'])
#           #flush input
#           ser.flushInput()
#           #ingore bad line
#           data = ser.readline()
#           #re_read
#           data = ser.readline()
#           ser.close()
#           data = data.decode('utf-8')
#       except Exception as e:
#           logger.exception('failed to read data from serial port')
#           exit(1)
#       logger.info('#{} data received'.format(num))
#       #parse data
#       try:
#           weight = parsedata(data)
#       except Exception as e:
#           logger.exception('failed to parse data')
#           continue
#       #fork a new thread to post data
#       try:
#           pid = os.fork()
#       except:
#           logger.exception('failed to first fork')
#       if pid == 0:
#           #   the child process/the second parent process
#           #   do #2 fork
#           try:
#               pid = os.fork()
#           except:
#               logger.exception('failed to do #2 fork')
#               exit(1)#no one cares exit code here
#           if pid == 0:
#               #the second child process
#               try:
#                   postdata(srvaddr, scalesid, weight)
#               except:
#                   logger.exception('#{} failed to post'.format(num))
#                   exit(1)
#               logger.info('#{} data posted'.format(num))
#               exit(0)
#           #   the second parent process
#           exit(0)
#       #   the parent process
#       ##  wait for the second parent process exit
#       os.wait()
#   #end while
#   #shouldn't come here if everything is ok
#   logger.error('unexcept error: fun run in mod scales should not return')
#   return 0


import logging
import os
import time
from postdata import postdata
import serial


def run(nodeinfo, logger, cnt):
    logger.info('hello, this is a scales mod')
    try:
        devname = nodeinfo['devname']
        baudrate = nodeinfo['baudrate']
        srvaddr = nodeinfo['srvaddr']
        scalesid = nodeinfo['scalesid']
    except:
        logger.exception('not enough config parameters')
        exit(1)

    # listen and grab data
    try:
        ser = serial.Serial(devname, baudrate)
        # flush input
        ser.flushInput()
        # ingore bad line
        data = ser.readline()
        # re_read
        data = ser.readline()
        ser.close()
    except:
        logger.exception('failed to open or read from serial port')
        exit(1)
    logger.info('#{} data received'.format(cnt))

    # parse data
    try:
        data = data.decode('utf-8')
        weight = parsedata(data)
    except Exception as e:
        logger.exception('failed to decode or parse data')
        exit(1)
    # fork a new thread to post data
    try:
        result = postdata(srvaddr, scalesid, weight)
    except:
        logger.exception('#{} failed to post'.format(cnt))
        exit(1)
    logger.info('#{} data posted, result: {}'.format(cnt, str(result)))
    exit(0)
    return 0

import os
import os.path


def fix(nodeinfo, logger, exitcode):
    logger.info('this is func fix of scales mod')
    # get config
    try:
        devname = nodeinfo['devname']
        baudrate = nodeinfo['baudrate']
        srvaddr = nodeinfo['srvaddr']
        scalesid = nodeinfo['scalesid']
    except:
        logger.exception('not enough config parameters')
        exit(1)
    if not os.path.exists(devname):
        logger.error('not such device, failed to fix')
        exit(1)
    exit(0)
    return 0

import logging
import sys
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    logger.info('this is test for mod_scales')
    cnt = 9526
    config = {"devname": sys.argv[1],
              "baudrate": 9600,
              "scalesid": 2,
              "srvaddr": "http://211.83.111.245/biaoben/receive.php"}
    print('try to run it')
    try:
        run(config, logger, cnt)
    except:
        logger.exception('failed to run')
        print('try to fix it')
        fix(config, logger, 1)
    print('finished!')
