#!/usr/bin/env python3
# -*- coding: utf-8 -*-
configfilepath = './config_img.json'

import pygame, pygame.camera
from urllib import request, parse
import json

def caponeframe(imgpath, dev, resolution):
	try:	
		pygame.camera.init()
		cam = pygame.camera.Camera(dev,resolution)
		cam.start()
		img = cam.get_image()
		cam.stop()
	except Exception as e:
		print('capture failed')
		print('details: ',e)
		raise
	try:
		pygame.image.save(img,imgpath)
	except Exception as e:
		print('save image failed')
		print('details: ',e)
		raise
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

import datetime
def gettimestr():
	return str(datetime.datetime.now())

import json
def getconfig(filepath):
    with open(filepath, 'r') as f:
        s = f.read()
    config = json.loads(s)
    return config

import time, os
if __name__ == '__main__':
	if configfilepath[0] != '/':
		BASE_DIR = os.path.dirname(__file__)
		configfilepath = os.path.join(BASE_DIR, configfilepath)
	config = getconfig(configfilepath)
	addr = config['addr']
	imgfilepath = config['imgfilepath']
	timeinterval = config['timeinterval']
	videodevice = config['videodevice']
	resolution = config['resolution']
	if imgfilepath[0] != '/':
		BASE_DIR = os.path.dirname(__file__)
		imgfilepath = os.path.join(BASE_DIR, imgfilepath)
	timenext = time.time()
	while(1):
		timenext = timenext + timeinterval
		#capture and save a frame
		print(gettimestr(),': session start')
		caponeframe(imgfilepath, videodevice, resolution)
		print(gettimestr(),': captured')
		#upload a frame
		#result = uploadoneframe(addr, "../testimgs/1.jpg")
		#result = uploadoneframe(addr, "./postdata.py")
		#print(result)
		try:
			result = uploadoneframe(addr, imgfilepath)
		except Exception as e:
			print(gettimestr(),': failed to upload')
		else:
			print(gettimestr(),': uploaded')
			print('result: ',result)
		time.sleep(timenext-time.time())
