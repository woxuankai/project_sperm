#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import importlib
import sys
import time
import os
import signal
import errno

def initlogger(config_basic):
    leveldict = {
        'CRITICAL' : logging.CRITICAL,
        'ERROR'    : logging.ERROR,
        'WARNING'  : logging.WARNING,
        'INFO'     : logging.INFO,
        'DEBUG'    : logging.DEBUG,
        'NOTSET'   : logging.NOTSET}
    defaultlogformat = \
        '%(asctime)s - %(levelname)s - %(name)s : %(message)s'
    logging.info('...setting logger in main_job')
    logfilename = config_basic['filename'] # must specify one
    loglevel    = leveldict[config_basic.get('level','WARNING')]
    logformat    = config_basic.get('format',defaultlogformat)
    logging.info("filename: {}, level: {}".format(logfilename,loglevel))
    name = config_basic.get('name','default')
    name = 'main_job.' + name
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    filehandler = logging.FileHandler(logfilename)
    formatter = logging.Formatter(logformat)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    #prevent logger from propagating to parent
    logger.propagate = False
    ##set file handler to root so there will be no extra message in stderr
    #logging.getLogger('root').addHandler(filehandler)
    #set logging level to warning in prevention of too much 
    #logging.basicConfig(level = logging.WARNING)
    return logger

#def killwait(interval, maxcnt) -> bool:
#    """kill-wait loop until it die
#delay 

# Main job will fork a child to do main work and the sleep.
# When parent is awake but child still hasn't exited,
# it will try to kill the child process.
# Each kill happens between each wait(sec)
# and wait for at most maxwait times.
# Child process still not exit now?
# Parent process exits 1 then.
maxwait = 20
eachwait = 0.25

class main_job:
    def main_clean(self):
        pass

    # the main job to do
    def main_do(self):
        config = self.config
        logger = self.logger
        start_delay   = config['basic']['start_delay']
        repeat_time   = config['basic']['repeat_time']
        restart_delay = config['basic']['restart_delay']
        nodeconfig    = config['spec']
        mod = importlib.import_module(\
            "mod_" + config['basic']['nodetype'])
        handler_run = getattr(mod, "run")
        handler_fix = getattr(mod, "fix")
    
        logger.info('ready to start')
        #   wait a moment
        time.sleep(start_delay)
        
        logger.info('now fork for work process')
        #   fork for work process
        cnt = 0
        while cnt < repeat_time or repeat_time < 0:
            cnt = cnt + 1
            # fork for work func
            try:
                pid = os.fork()
                assert pid >= 0
            except Exception as e:
                logger.exception('failed to fork for work func')
                raise e
            # the child process
            if pid == 0:
                exitcode = 0
                logger = logging.getLogger(logger.name + '.' + hex(cnt))
                logger.info('forked for work process')
                try:
                    # don't care return value, if error happened, just raise it
                    handler_run(nodeconfig, logger, cnt)
                except:
                    logger.error('work function raised an exception')
                    exitcode = 1
                logger.info('exit work process')
                os._exit(exitcode)# ensure 1-2-4-8...will not happen

            # parent process
            #logger.info('#{}: sleep now'.format(cnt))
            try:
                time.sleep(restart_delay)
            except:
                logger.exception('failed to do restart delay')
                break
            pidwait, status = os.waitpid(pid, os.WNOHANG)
            if pidwait != pid:
                #child process still not finished???
                logger.warning('parent awake now, but child havn\'t exited')
                logger.info('try to kill it')
                for waitcnt in range(0, maxwait):
                    if pidwait != 0:
                        break
                    try:
                        os.kill(pid, signal.SIGTERM)
                    except Exception as e:
                        if type(e) == OSError and e.errno == errno.ESRCH:
                            break
                    time.sleep(eachwait)
                pidwait, status = os.waitpid(pid, os.WNOHANG)
            if pidwait == pid:
                exitcode = int(status >> 8)
                if exitcode != 0:
                    logger.warning('work process exited {}'.format(exitcode))
                else:
                    logger.info('work process exited 0')
            else:
                logging.error('failed to terminate work process')
                sys.exit(1)
        # end of while
        
        logger.info('exit daemon process now')
        exit(0)

    def start(self):
        self.main_clean()
        self.main_do()
    def stop(self):
        self.main_clean()
   
    def __init__(self, config):
        self.config = config
        self.logger = initlogger(config['basic'])
        
    def __enter__(self):
        self.start()
        
    def __exit__(self,exc_type, exc_val, exc_tb):
        self.stop()
        


#import sys
#import os
#import os.path
#if __name__ == '__main__':
#    modpath = os.path.abspath(sys.argv[0])
#    modpath = os.path.dirname(modpath)
#    modpath = os.path.join(modpath, "./mods")
#    sys.path.append(modpath)
#    nodeconfig = {"nodetype": "test",
#                  "start_delay": 2,
#                  "restart_delay": 2,
#                  "repeat_time": 5,
#                  "logpath": "./__pycache__/",
#                  "logformat": "%(asctime)s - %(levelname)s - %(name)s : %(message)s",
#                  "pidfile": "/temp/project_sperm_test0.pid",
#                  "dpidfile": "/temp/project_sperm_test0d.pid",
#                  "stdout": "/dev/null",
#                  "stdin": "/dev/null",
#                  "stderr": "/dev/null",
#\
#                  "exitcode": 1, "fixexitcode": 0}
#    nodeconfig['nodename'] = 'test0'
#    daemon_start(nodeconfig)
#
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
#
#
#
#
#            # fork for fix func
#            try:
#                pid = os.fork()
#            except:
#                logger.exception('failed to fork to fix problems')
#            if pid == 0:
#                # child
#                handler_fix(nodeconfig, logger, exitcode)
#                logger.warning('fix func return')
#                exit(0)
#            # parent
#            pid, status = os.wait()
#            exitcode = int(status >> 8)
#            logger.info('fix process exited with {}'.format(exitcode))
#            if exitcode != 0:
#                # failed to fix problem
#                logger.error('failed to fix problems')
#                break
#            else:
#                logger.info('successfully fixed problems')
#
