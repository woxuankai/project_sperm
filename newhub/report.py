#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
ISOTIMEFORMAT='%Y-%m-%d %X %z'
def report_info(message):
	stimenow = time.strftime(ISOTIMEFORMAT, time.localtime())
	print(stimenow, ' INFO\t', message)

def report_error(message):
	stimenow = time.strftime(ISOTIMEFORMAT, time.localtime())
	print(stimenow, ' ERR\t', message)

if __name__ == '__main__':
	report_info('this is a info')
	report_error('this is an error')
