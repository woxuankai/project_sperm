#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, sys
import os, os.path
from getconfig import getconfig
from daemon import daemon_start
if __name__ == '__main__':
	#slove path problems
	logging.basicConfig(level=logging.DEBUG)
	try:
		if len(sys.argv) < 4:
			raise NameError("not enough arguments")
		configfilepath = os.path.abspath(sys.argv[1])
		node2start = sys.argv[2]
		if not os.path.isfile(configfilepath):
			raise NameError("not a config file")
		basedir = os.path.dirname(configfilepath)
		modpath = os.path.join(basedir,"./mods")
		assert(os.path.isdir(modpath))
		sys.path.append(modpath)
	except Exception:
		logging.exception("usage: run.py config nodename|all start|stop")
		exit(-1)
	#load config file
	try:
		config = getconfig(configfilepath)
	except Exception:
		logging.exception('fail to load config file: ' + configfilepath)
		exit(-1)
	#check configs
	if node2start == 'all':
		for nodename in config:
			nodeconfig = config[nodename]
			nodeconfig['nodename'] = nodename
			try:
				daemon_start(nodeconfig)
			except Exception:
				logging.exception(\
'failed to start node daemon<{}>'.format(nodename))
			else:
				logging.info('node daemon {} started'.format(nodename))
	elif node2start in config:
		nodeconfig = config[node2start]
		nodeconfig['nodename'] = nodename
		try:
			daemon_start(nodeconfig)
		except Exception:
			logging.exception(\
'failed to start node daemon<{}>'.format(nodename))
		else:
			logging.info('node daemon {} started'.format(nodename))
	else:
		logging.error('no such nodename'+node2start)
		exit(-1)
	exit(0)
