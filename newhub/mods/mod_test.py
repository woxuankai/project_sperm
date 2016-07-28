#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
def run(config, logger):
	time.sleep(5)
	logger.info('hello, this is a test mod')
	logger.info(str(config))
	if 'exitcode' in config:
		exit(config['exitcode'])
	else:
		exit(0)
