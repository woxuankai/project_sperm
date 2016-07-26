#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
def getconfig(filepath):
	with open(filepath, 'r') as f:
		s = f.read()
	config = json.loads(s)
	return config

import logging, sys
if __name__=='__main__':
	if len(sys.argv) < 2 :
		configpath="./config.json"
		print("WARNNING : \
use default config file: ./config.json")
	else:
		configpath = sys.argv[1]
	try :
		nodes = getconfig(configpath)
		print("nodes :",nodes)
	except Exception as e:
		print('failed to load config file : ', e)
