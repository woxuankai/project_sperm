#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
def getnodes(filepath):
	with open(filepath, 'r') as f:
		s = f.read()
	nodes = json.loads(s)
	return nodes

import logging
if __name__=='__main__':
	configpath = input("input path of config file: ")
	try :
		nodes = getnodes(configpath)
		print("nodes :",nodes)
	except Exception as e:
		logging.critical('failed to load config file')
