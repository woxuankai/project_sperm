#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, logging
from path2absolute import path2abolutepath
def initlogger(loggername, logpath='./logs/log_{}_{}.log') :
	logger = logging.getLogger(loggername)
	logger.setLevel(logging.DEBUG)
	stimenow = time.strftime('%Y_%m_%d_%X_%z', time.localtime())
	logfilepath = logfilepathtemplate.format(loggername,stimenow)
	logfilepath = path2abolutepath(logfilepath)
	logfile_handler = logging.FileHandler(logfilepath)
	#logfile_handler = logging.StreamHandler()
	formatter = logging.Formatter(\
'%(asctime)s - %(levelname)s - %(name)s : %(message)s')
	logfile_handler.setFormatter(formatter)
	logger.addHandler(logfile_handler)
	return logger

import time, logging, os, importlib, sys
import os.path
from getconfig import getconfig
from path2absolute import path2abolutepath
if __name__ == '__main__':
	#slove path problems
	if len(sys.argv) < 2
		print("usage: run.py config_file_path")
		return -1
	try:
		configfilepath = os.path.abspath(argv[1])
		if not configfilepath.isfile():
			raise NameError
		basedir = os.path.dirname(configfilepath)
	except Exception as e:
		logging.exception("invalid path: ", e)
		exit(-1)
	#config log file
	try:
		logger = initlogger('daemon')
	except Exception:
		logging.exception('failed to init logger')
		exit(-1)
	#load config file
	logger.info('...loading config file')
	try:
		config = getnodes(configfilepath);
	except Exception:
		logger.exception('fail to load config file: ' + configfilepath)
		exit(-1)
	#one node, one process
	allnodes = config
	childpids = {};
	nodes = allnodes.copy()
	while True:
		nodename,nodeinfo = nodes.popitem()
		logger.info('...forking for node processes')	
		try:
			pid = os.fork()
		except Exception:
			logger.exception('unable to fork')
			exit(-1)
		if pid == 0:
			#the child process
			##config log file
			try:
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
				logger.info('all nodes have their own processs now')
				#wait for processes exit and restart them
				pid,status = os.wait()
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
