#!/usr/bin/env python3
# -*- coding: utf-8 -*-

configfilepath = './config.json'
logfilepathtemplate = './logs/log_{}'

failed_restart_delay = 60
fork_delay = 10

import os
def path2abolutepath(path, base_dir=os.path.dirname(__file__)):
	if path[0] != '/':
		return os.path.join(base_dir, path)
	else:
		return path

import time, logging
from getnodes import getnodes
from startnode import startnode, startnodetest

if __name__ == '__main__':
	logfile = logging.
	logging.info('start!')
	logging.info('...loading config file')
	try:
		configfilepath = path2abolutepath(configfilepath)
		allnodes = getnodes(configfilepath);
	except Exception:
		logging.critical('fail to load config file: ' + configfilepath)
		exit(-1)
	#one node, one process
	childpids = {};
	logging.info('...forking for node processes')
	nodes = allnodes.copy()
	while True:
		nodename,nodeinfo = nodes.popitem()
		try:
			pid = os.fork()
		except Exception:
			logging.critical('unable to fork')
			exit(-1)
		if pid == 0:
			#the child process
			logging.info("I'm process for node: {}".format(nodename))
			try:
				nodeinfo['nodename'] = nodename
				startnode(nodeinfo)
				#startnodetest(nodeinfo)
			except Exception as e:
				logging.error('exception occurs in node: {}'.format(nodename))
				exit(-1)
			#shouldn't reach here
			logging.error('process for node: {} exits now'.format(nodename))
			exit(-2)
		else:
			#the parent process
			logging.info('successfully forked for node: {}'.format(nodename))
			childpids[pid] = nodename
			if len(nodes) <= 0:
				logging.info('all nodes have their own processs now')
				#wait for processes exit and restart them
				pid,status = os.wait()
				exitchildname = childpids[pid]
				nodes[exitchildname] = allnodes[exitchildname]
				logging.error('process for node <{}> exited\
\nexit status indication: {}\
\nnode will restart soon'\
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
