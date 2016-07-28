#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os, os.path, importlib, logging, time, sys, atexit
#non-blocck, returns daemon pid
def daemon_start(nodeconfig):
	#	assert common config
	nodename = nodeconfig.pop('nodename')
	nodetype = nodeconfig.pop('nodetype')
	start_delay = nodeconfig.pop('start_delay')
	restart_delay = nodeconfig.pop('restart_delay')
	max_retry = nodeconfig.pop('max_retry')
	assert(start_delay >= 0)
	assert(restart_delay >= 0)
	assert(type(max_retry) == int)
	logpath = nodeconfig.pop('logpath')
	logsuffixformat = nodeconfig.pop('logsuffixformat')
	logformat = nodeconfig.pop('logformat')
	pidfile = nodeconfig.pop('pidfile')
	dpidfile = nodeconfig.pop('dpidfile')
	stdin = nodeconfig.pop('stdin')
	stdout = nodeconfig.pop('stdout')
	stderr = nodeconfig.pop('stderr')

	#	set log system
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
	#	able to record logs now
	#	first fork
	##	does not handle error, which will be handled by parent process
	pid = os.fork()
	if pid != 0:
		#	the parent(run) process
		return pid
	#	the child(daemon) process
	###	have to record and handle errors oneself
	##	daemonize process
	##	decouple from parent environment
	try:
		os.chdir("/tmp")
		os.setsid()
		os.umask(0)
	except :
		logger.exception('failed to decouple from parent environment')
		exit(1)
	##	second fork
	try:
		pid = os.fork()
	except :
		logger.exception('failed to do second fork')
		exit(1)
	if pid != 0:
		###	the second parent process
		exit(0)
	##	redirect standard file descriptors
	try:
		sys.stdout.flush()
		sys.stderr.flush()
		si = open(stdin, 'r')
		so = open(stdout, 'a+')
		se = open(stderr, 'a+')
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	except :
		logger.exception('failed to redirect standard file descriptors')
		exit(1)
	##	write ppidfile
	#atexit.register(self.delpid)
	#pid = str(os.getpid())
	#file(pidfile,'w+').write("%s\n" % pid)
	#	import mod and handler function
	try:
		mod = importlib.import_module("mod_"+nodetype)
		handler_run = getattr(mod, "run")
	except :
		logger.exception('failed to load mod to run node')
		exit(1)
	#	wait a moment
	try:
		time.sleep(start_delay)
	except :
		logger.exception('failed to do start delay')
	#	fork for work process
	if max_retry >= 0:
		max_retry = max_retry + 1
	while max_retry != 0:
		if max_retry > 0:
			max_retry = max_retry - 1
		try:
			pid = os.fork()
		except :
			logger.exception('failed to fork')
		if pid == 0:
			#	the child process
			handler_run(nodeconfig,logger)
			logger.info('work func return')
			exit(0)
		#	parent process
		# successfully forked
		logger.info('forked for node')
		#wait
		pid, status = os.wait()
		exitcode = int(status>>8)
		logger.info('work process exited with {}'.format(exitcode))
		if exitcode == 0:
			break
		logger.info('wait and restart worker: {} left'.format(max_retry))
		try:
			time.sleep(restart_delay)
		except:
			logger.exception('failed to do restart delay')
			exit(1)
	## out of the loop
	logger.info('exit daemon process now')
	exit(0)
