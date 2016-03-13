#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#for func disptimestamp() 
#from . import timestamp
#something wrong with "relative import" 
import timestamp

from urllib import request, parse
import json

#import sys
#sys.path.append("..")


#fetch config
#returns a json in dict if no error occurs
#better use "try...except..finally..." cause this func may throw errors (such as conn err)
def getconfig (addr):
	req = request.Request(addr)
	with request.urlopen(req) as f:
		if f.status >= 400:
			raise ConnectionError('HTTP ERR: ', f.status)
		res = f.read()
		resdict = json.loads(res.decode('utf-8'))
		return resdict


if __name__ == '__main__':
	config_serveraddr = "http://211.83.111.245/biaoben/get_setting.php"
	print('fetching config...')
	try:
		resdict = getconfig(config_serveraddr)
		print('config fetched! ')
		for head in resdict:
			print(head, ': ', resdict[head])
	except Exception as e:
		timestamp.disptimestamp() 
		print('  ERROR ! failed to fetch config! ')
		print('  err info: ', e)
	finally:
		print('download finished!')


		
