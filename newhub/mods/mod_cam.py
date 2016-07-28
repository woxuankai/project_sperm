#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, pygame.camera
from urllib import request, parse
import json

def caponeframe(imgpath, dev, resolution):
	pygame.camera.init()
	cam = pygame.camera.Camera(dev,resolution)
	cam.start()
	img = cam.get_image()
	cam.stop()
	pygame.image.save(img,imgpath)
	return 0

def uploadoneframe(serveraddr,imgpath):
	imgfile = open(imgpath, 'rb')
	#reqdata = parse.urlencode([('image', imgfile.read())])
	reqdata = imgfile.read()
	imgfile.close()
	req = request.Request(serveraddr)
	#with request.urlopen(req, data = reqdata.encode('utf-8')) as f:
	with request.urlopen(req, data = reqdata) as f:
		if f.status >= 400:
			raise ConnectionError('HTTP ERR: ', f.status)
		res = f.read()
		#resdict = json.loads(res.decode('utf-8'))
	return res.decode('utf-8')


import time, os
def run(config, logger):
	logger.info('this is func run of mod_cam')
	try:
		addr = config['addr']
		imgfilepath = config['imgfilepath']
		timeinterval = config['timeinterval']
		videodevice = config['videodevice']
		resolution = config['resolution']
	except:
		logger.exception('missing config para')
		exit(1)
	cnt = 0
	timenext = time.time()#just put it here to save a try--except
	while True:
		cnt = cnt + 1
		try:
			sleeptime = timenext - time.time()
			if sleeptime < 0:
				sleeptime = 0
			time.sleep(sleeptime)
			timenext = timenext + timeinterval
		except:
			logger.exception('failed to sleep')
			exit(1)
		try:
			#capture and save a frame
			caponeframe(imgfilepath, videodevice, resolution)
		except:
			logger.exception('#{} failed to capture'.format(cnt))
			continue
		logger.info('#{} captured'.format(cnt))
		#	upload a frame
		#	no need to fork
		try:
			result = uploadoneframe(addr, imgfilepath)
		except:
			logger.exception('#{} failed to upload'.format(cnt))
			continue
		logger.info('#{} uploaded, result: {}'.format(cnt, result))
	#end of loop
	exit(1)
	return
