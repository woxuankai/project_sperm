#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging
import os

def run(config, logger, cnt):
    logger.info('#{} hello, this is a test mod'.format(cnt))
    time.sleep(config['wait'])
    logger.info(str(config))
    logger.info('pid: {}'.format(os.getpid()))
    if 'exitcode' in config:
        exit(config['exitcode'])
    else:
        exit(0)


def fix(config, logger, exitcode):
    time.sleep(2)
    logger.info('hello, this is a fix for code{}'.format(exitcode))
    logger.info(str(config))
    if 'fixexitcode' in config:
        exit(config['fixexitcode'])
    else:
        exit(0)
