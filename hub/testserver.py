#!/usr/bin/env python3
# -*- coding: utf-8 -*-

post_serveraddr = "http://211.83.111.245/biaoben/receive.php"

import re
from packages.postdata import postdata
def proclink(sock, addr, clients_dict):
	data = sock.recv(256)
	sock.close()
	data = data.decode('utf-8')
	print("received !")
	#print('Received from ',addr)
	#print('content :',data)
	cname, cdata = data.split(':')
	cweight = cdata[7:14]
	if cdata[0:7] != 'ST,GS,+':
	    print('Error data format!')
	    return -1
	if cdata[14:16] != 'kg':
	    print('Error data unit!')
	    return -1
        #print(cname,",",cweight)
	if cname in clients_dict :
		print("uploading...")
		try :
			res = postdata(post_serveraddr, int(clients_dict[cname]), float(cweight))
			#print(res)
			if "state" in res :
				if res["state"] != 1 :
					print("failed !server return state : {}".format(res['state']))
				else :
					print("success !")
			else :
				print("success ! (with no return state)")
		except Exception as e:
			print("failed to upload")
			print("problem: ",e)
	else:
		print("Warnning! didn't have a client named {}".format(cname))
	

listenaddr = ('0.0.0.0', 2333)
configfilepath = "./config.json"

#getclients from config file
from packages.getclients import getclients
print("obtianing clients information...")
try :
	clients_dict = getclients(configfilepath)
except Exception as e:
	print("failed to obtain client information from config file, quit")
	quit()
print("success !")

import socket, threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(listenaddr)
s.listen(10)
print("waiting for connectting...")

while True:
	sock, addr = s.accept()
	t = threading.Thread(target=proclink,args=(sock, addr, clients_dict))
	t.start()
