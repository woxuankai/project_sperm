#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
def getclients(filepath):
	with open(filepath, 'r') as f:
		s = f.read()
	config_dict = json.loads(s)
	if not "clients" in config_dict :
		raise KeyError("could not find key 'clients' in file {}".format(filepath))
	else :
		#clients_list = config_dict["clients"]
		clients_dict = config_dict["clients"]
	#clients_dict = {}
	#for clientnames in clients_list :
		#clients_dict.update(clientnames)
	for clientnames in clients_dict :
		if type(clientnames) != str or type(clients_dict[clientnames]) != str :
			raise NameError('client config should be string')
		if clientnames.isalnum() != True or clients_dict[clientnames].isnumeric() != True :
			raise NameError('client should in format like {"alphaornumber":"number"}')
	return clients_dict


if __name__=='__main__':
	configpath = input("input path of config file: ")
	try :
		clients = getclients(configpath)
		print("clients :",clients)
	except Exception as e:
		print("Error ! ",e)
		
