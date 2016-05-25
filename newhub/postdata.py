#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import timestamp
from urllib import request, parse
import json
import time

#function postdata
#send data (including id,time and weight)
#returns a json in dict if no error occurs while uploading
#better use "try...except..finally..." cause this func may throw errors (such as conn err)
def postdata (addr, id, weight):
	timenow = time.time()
	reqdata = parse.urlencode([
		('id', id),
		('weight', weight),
		('time', timenow)
	])
	req = request.Request(addr)
	with request.urlopen(req, data = reqdata.encode('utf-8')) as f:
		if f.status >= 400:
			raise ConnectionError('HTTP ERR: ', f.status)
		res = f.read()
		resdict = json.loads(res.decode('utf-8'))
		return resdict


if __name__ == '__main__':
	post_serveraddr = "http://211.83.111.245/biaoben/receive.php"
	sampleid = 2
	sampleweight = 36.234
	print('uploading sample data...')
	try:
		res = postdata(post_serveraddr, sampleid, sampleweight)
		print("returned :",res)
	except Exception as e:
		timestamp.disptimestamp() 
		print('  ERROR ! failed to post data! ')
		print('  id:', sampleid, 'weight:', sampleweight)
		print('  err info: ', e)
	finally:
		print('upload finished!')


		
