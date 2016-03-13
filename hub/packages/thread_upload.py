#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#interface
post_serveraddr = "http://211.83.111.245/biaoben/receive.php"



from multiprocessing import Process, Queue


#input paramentera
##qdata: queue to get data
##qconfig: queue to get config
def start_thread_upload(qdata, qconfig):
	pass













#		if resdict['state'] != 1:
#			raise Exception('RETURN STATE ERR: ', resdict['state'])
#		if resdict['update'] != 0:
#			#trig_updateconfig()
#			pass
#
#	sampleid = 2
#	sampleweight = 34
#	try:
#		postdata(post_serveraddr, sampleid, sampleweight)
#	except Exception as e:
#		disptimestamp() 
#		print('  ERROR ! failed to post data! ')
#		print('  id:', sampleid, 'weight:', sampleweight)
#		print('  err info: ', e)
#	finally:
#		pass
#	pass
