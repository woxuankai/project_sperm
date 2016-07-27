#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#non-blocck, returns pid
def daemon_start(nodeconfig):
	print(nodeconfig)
	return 123


import time, logging
def initlogger(loggername, logpath):
	logger = logging.getLogger(loggername)
	logger.setLevel(logging.DEBUG)
	stimenow = time.strftime('%Y_%m_%d_%X_%z', time.localtime())
	logfilepath = logpath.format(stimenow)
	logfile_handler = logging.FileHandler(logfilepath)
	#logfile_handler = logging.StreamHandler()
	formatter = logging.Formatter(\
'%(asctime)s - %(levelname)s - %(name)s : %(message)s')
	logfile_handler.setFormatter(formatter)
	logger.addHandler(logfile_handler)
	return logger

import time, logging, importlib, sys
import os, os.path
from getconfig import getconfig
if __name__ == '__main__':
	#slove path problems
	try:
		if len(sys.argv) < 2:
			raise NameError("need a config file")
		configfilepath = os.path.abspath(sys.argv[1])
		if not os.path.isfile(configfilepath):
			raise NameError
		basedir = os.path.dirname(configfilepath)
	except Exception:
		logging.exception("invalid config file path!")
		exit(-1)
	#load config file
	try:
		config = getconfig(configfilepath);
	except Exception:
		logging.exception('fail to load config file: ' + configfilepath)
		exit(-1)
	#check deamon config
	try:
		deamonconfig = config["deamon"]
		failed_restart_delay = deamonconfig["failed_restart_delay"]
		assert(failed_restart_delay >= 0)
		fork_delay = deamonconfig["fork_delay"]
		assert(fork_delay >= 0)
		start_delay = deamonconfig["start_delay"]
		assert(start_delay >= 0)
		logpath = deamonconfig["logpath"]
		logpath = os.path.join(basedir, logpath)
	except Exception:
		logging.exception("failed deamon config check")
		exit(-1)
	#start_delay
	time.sleep(start_delay)
	#init log system
	try:
		logger = initlogger('daemon',logpath)
	except Exception:
		logging.exception('failed to init daemon logger')
		exit(-1)
	#basedir, config, logger prepared now
	logger.info('deamon init done')
	#parse nodes
	try:
		allnodes = config['nodes']
	except Exception:
		logging.exception('no "nodes" area in config file')
		exit(-1)
	nodes_wait = allnodes.copy()#contains nodename:nodeconfig
	nodes_ready = {}#contains pid:names
	#one node, one process
	while True:
		for nodename in nodes_wait:
			time.sleep()
			logger.info('...forking for node <{}>'.format(nodename))
			try:
				pid = os.fork()
			except Exception:
				logger.exception('unable to fork')
			continue
			if pid == 0:
				#the child process
				try:
					nodeinfo["name"] = nodename
					nodeinfo["basedir"] = basedir
					startnode(nodeinfo)
				except Exception as e:
					nodelogger.exception('exception occurs in <{}>'.format(nodename))
					exit(-1)
			#shouldn't reach here
			nodelogger.error('process for <{}> exits now'.format(nodename))
			exit(-2)
		else:
			#the parent process
			logger.info('forked for <{}>'.format(nodename))
			childpids[pid] = nodename
			if len(nodes) <= 0:
				#every node has its process
				logger.info('all nodes have their own processs now')
				#wait for processes exit and restart them
				pid,status = os.wait()
				status = status/255
				exitchildname = childpids[pid]
				nodes[exitchildname] = allnodes[exitchildname]
				logger.error(\
'process for <{}> exited with status {}'\
.format(exitchildname,status))
				time.sleep(failed_restart_delay)
			else:
				#wait for some time, then continue to fork
				time.sleep(fork_delay)

	#forked one process per node
	#wait for every process to finish
	#while len(childpids) >= 1:
	#	pid,status = os.wait()
	#	exitchildname = childpids.pop(pid);
	#	print('process for node <{}> exited'.format(exitchildname))
	#	print('exit status indication: ',status)
	#child processes should never return
	#thus program shouldn't come here
	exit(0)
