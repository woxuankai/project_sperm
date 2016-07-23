#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parsedata(data):
    return float(data[6:14].replace(' ',''))

from postdata import postdata
def uploaddata(data, nodeinfo):
	try:
		weight = parsedata(data)
	except Exception as e:
		print("error data format")
		return 0
	try:
		postdata(nodeinfo['srvaddr'], nodeinfo['id'] , weight)
	except Exception as e:
		print("failed to post: ",e)
	else:
		print('node id: ', nodeinfo['id'],' :data posted')
	finally:
		return 0
