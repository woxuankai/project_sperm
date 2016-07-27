#!/usr/bin/env python3
# -*- coding: utf-8 -*-








import os, os.path, importlib, logging, time
#non-blocck, returns daemon pid
def daemon_start(nodeconfig):
	#assert common config
	nodename = nodeconfig['nodename']
	nodetype = nodeconfig['nodetype']
	start_delay = nodeconfig['start_delay']
	restart_delay = nodeconfig['restart_delay']
	assert(start_delay >= 0)
	assert(restart_delay >= 0)
	logpath = nodeconfig['logpath']
	logsuffixformat = nodeconfig['logsuffixformat']
	logformat = nodeconfig['nodeformat']
	pidfile = nodeconfig['pidfile']
	dpidfile = nodeconfig['dpidfile']
	#set log system
	logger = logging.getLogger(nodename)
	logger.setLevel(logging.INFO)
	stimenow = time.strftime(logsuffixformat, time.localtime())
	logfilepath = logpath.format(stimenow)
	logfile_handler = logging.FileHandler(logfilepath)
	#logfile_handler = logging.StreamHandler()
	formatter = logging.Formatter(logformat)
	logfile_handler.setFormatter(formatter)
	logger.addHandler(logfile_handler)
	logger.info('logger init finished')
	#able to record logs now
	pid = os.fork()
	if pid != 0:
		#the parent process
		return pid
	#the child(daemon) process
	#daemonize process





try:
                        pid = os.fork()
                        if pid > 0:
                                # exit first parent
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
       
                # decouple from parent environment
                os.chdir("/")
                os.setsid()
                os.umask(0)
       
                # do second fork
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit from second parent
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
       
                # redirect standard file descriptors
                sys.stdout.flush()
                sys.stderr.flush()
                si = file(self.stdin, 'r')
                so = file(self.stdout, 'a+')
                se = file(self.stderr, 'a+', 0)
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())
       
                # write pidfile
                atexit.register(self.delpid)
                pid = str(os.getpid())
                file(self.pidfile,'w+').write("%s\n" % pid)





	#import mod and handler function
	mod = importlib.import_module("mod_"+nodetype)
	handler_run = getattr(mod, "run")
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
