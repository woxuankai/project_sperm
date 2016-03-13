#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#a virtural client for test
#will send string like "+ xxx.xx"

dstaddr = ('192.168.1.187', 2333)
import socket, time
def startvirtualclient (nodename):
	while True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		pack = "{}:+34.45".format(nodename)
		pack= pack.encode('utf-8')
		try :
			print("uploading...")
			s.connect(dstaddr)
			s.send(pack)
			print("uploaded !")
		except BaseException as e:
			print("failed to upload due to :", e)
		finally :
			s.close()
			#print("connection closed !")
		time.sleep(1)#wait 1 sec	
#main
if __name__ == '__main__':
	nodename = input("enter a unique name for the node :") 
	if not nodename.isalnum() :
		print("alpha or number allowed only")
		quit()
	print("running virtual node {}...".format(nodename))
	startvirtualclient(nodename)
