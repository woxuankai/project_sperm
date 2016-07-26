#!/usr/bin/env python3
# -*- coding: utf-8 -*-

configfilepath = './config.json'
logfilepathtemplate = './logs/log_{}_{}.log'

failed_restart_delay = 60
fork_delay = 10



import time, logging, os
from getnodes import getnodes
from startnode import startnode, startnodetest
from path2absolute import path2abolutepath

if __name__ == '__main__':
	#config log file
	try:
		logger = logging.getLogger('daemon_logger')
		logger.setLevel(logging.DEBUG)
		stimenow = time.strftime('%Y_%m_%d_%X_%z', time.localtime())
		logfilepath = logfilepathtemplate.format('daemon',stimenow)
		logfilepath = path2abolutepath(logfilepath)
		logfile_handler = logging.FileHandler(logfilepath)
		#logfile_handler = logging.StreamHandler()
		formatter = logging.Formatter(\
'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		logfile_handler.setFormatter(formatter)
		logger.addHandler(logfile_handler)
	except Exception:
		logging.exception('failed to init logger')
		exit(-1)
	##start
	logger.info('start!')
	logger.info('...loading config file')
	try:
		configfilepath = path2abolutepath(configfilepath)
		allnodes = getnodes(configfilepath);
	except Exception:
		logger.exception('fail to load config file: ' + configfilepath)
		exit(-1)
	#one node, one process
	childpids = {};
	logger.info('...forking for node processes')
	nodes = allnodes.copy()
	while True:
		nodename,nodeinfo = nodes.popitem()
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
