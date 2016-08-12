#!/usr/bin/env python3
# -*- coding: utf-8 -*-

logfiletimeformat='%Y-%m-%d-%H-%M-%S'

import os, os.path, importlib, logging, time, sys, atexit
#non-blocck, returns daemon pid
def daemon_start(nodeconfig):
    #   assert common config
    nodename = nodeconfig.pop('nodename')
    nodetype = nodeconfig.pop('nodetype')
    start_delay = nodeconfig.pop('start_delay')
    restart_delay = nodeconfig.pop('restart_delay')
    repeat_time = nodeconfig.pop('repeat_time')
    assert(start_delay >= 0)
    assert(restart_delay >= 0)
    assert(type(repeat_time) == int)
    logpath = nodeconfig.pop('logpath')
    logformat = nodeconfig.pop('logformat')
    pidfile = nodeconfig.pop('pidfile')
    dpidfile = nodeconfig.pop('dpidfile')
    stdin = nodeconfig.pop('stdin')
    stdout = nodeconfig.pop('stdout')
    stderr = nodeconfig.pop('stderr')

    #   set log system
    logger = logging.getLogger(nodename)
    logger.setLevel(logging.INFO)
    stimenow = time.strftime(logfiletimeformat, time.localtime())
    logpath = logpath+"log_{}_"+nodename+".log"
    logfilepath = logpath.format(stimenow)
    logfile_handler = logging.FileHandler(logfilepath)
    #logfile_handler = logging.StreamHandler()
    formatter = logging.Formatter(logformat)
    logfile_handler.setFormatter(formatter)
    logger.addHandler(logfile_handler)
    logger.info('logger init finished')
    #   able to record logs now
    #   first fork
    ##  does not handle error, which will be handled by parent process
    pid = os.fork()
    if pid != 0:
        #   the parent(run) process
        pid, status = os.wait()
        exitcode = int(status>>8)
        logger.info('parent of #2 fork exited with {}'.format(exitcode))
        return pid
    #   the child(daemon) process
    ### have to record and handle errors oneself
    ##  daemonize process
    ##  decouple from parent environment
    try:
        os.chdir("/tmp")
        os.setsid()
        os.umask(0)
    except :
        logger.exception('failed to decouple from parent environment')
        exit(1)
    logger.info('decoupled from parent environment')
    ##  second fork
    try:
        pid = os.fork()
    except :
        logger.exception('failed to do second fork')
        exit(1)
    if pid != 0:
        ### the parent process of #2 fork
        exit(0)
    logger.info('daemon process forked')
    ##  redirect standard file descriptors
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
    logger.info('daemonized')
    ##  write ppidfile
    #atexit.register(self.delpid)
    #pid = str(os.getpid())
    #file(pidfile,'w+').write("%s\n" % pid)
    #   import mod and handler function
    try:
        mod = importlib.import_module("mod_"+nodetype)
        handler_run = getattr(mod, "run")
        handler_fix = getattr(mod, "fix")
    except :
        logger.exception('failed to load mod or func')
        exit(1)
    logger.info('loaded function handler')
    #   wait a moment
    try:
        time.sleep(start_delay)
    except :
        logger.exception('failed to do start delay')
    logger.info('now fork for work process')
    #   fork for work process
    cnt = 0
    while cnt < repeat_time or repeat_time < 0:
        cnt = cnt + 1
        #fork for work func
        try:
            pid = os.fork()
        except :
            logger.exception('failed to fork for work func')

        ##the child process
        if pid == 0:
            logger.info('forked for work func')
            handler_run(nodeconfig, logger, cnt)
            logger.warning('work func return')
            exit(0)

        ##parent process
        pid, status = os.wait()
        exitcode = int(status>>8)
        logger.info('work process exited with {}'.format(exitcode))

        #handle problem
        if exitcode != 0:
            logger.info('try to fix problems')
            #fork for fix func
            try:
                pid = os.fork()
            except:
                logger.exception('failed to fork to fix problems')
            if pid == 0:
            #child
                handler_fix(nodeconfig, logger, exitcode)
                logger.warning('fix func return')
                exit(0)
            #parent
            pid, status = os.wait()
            exitcode = int(status>>8)
            logger.info('fix process exited with {}'.format(exitcode))
            if exitcode != 0:
                #failed to fix problem
                logger.error('failed to fix problems')
                break
            else:
                logger.info('successfully fixed problems')

        logger.info('#{}: wait and restart worker'.format(cnt))
        try:
            time.sleep(restart_delay)
        except:
            logger.exception('failed to do restart delay')
            break
    ## end of while
    logger.info('exit daemon process now')
    exit(0)

import sys, os, os.path
if __name__ == '__main__':
    modpath = os.path.abspath(sys.argv[0])
    modpath = os.path.dirname(modpath)
    modpath = os.path.join(modpath,"./mods")
    sys.path.append(modpath)
    nodeconfig={"nodetype":"test",\
"start_delay":2,\
"restart_delay":2,\
"repeat_time":5,\
"logpath":"./__pycache__/",\
"logformat":"%(asctime)s - %(levelname)s - %(name)s : %(message)s",\
"pidfile":"/temp/project_sperm_test0.pid",\
"dpidfile":"/temp/project_sperm_test0d.pid",\
"stdout":"/dev/null",\
"stdin":"/dev/null",\
"stderr":"/dev/null",\
\
"exitcode":1,"fixexitcode":0}
    nodeconfig['nodename'] = 'test0'
    daemon_start(nodeconfig)

#   "test0":
#   {
#       "nodetype":"test",
#       "start_delay":5,
#       "restart_delay":5,
#       "repeat_time":5,
#       "logpath":"/var/log/project_sperm/",
#       "logformat":"%(asctime)s - %(levelname)s - %(name)s : %(message)s",
#       "pidfile":"/temp/project_sperm_test0.pid",
#       "dpidfile":"/temp/project_sperm_test0d.pid",
#       "stdout":"/dev/null",
#       "stdin":"/dev/null",
#       "stderr":"/dev/null",
#
#       "exitcode":0
#   }
