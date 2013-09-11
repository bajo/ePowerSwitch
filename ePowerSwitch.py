#!/usr/bin/env python
# Filename: ePowerSwitch.py

""" 
EPowerSwitch module provides a way to set and retrieve the status of a socket on a remote-control socket strip from Leuning
See http://www.leunig.de/_en/_pro/remote-power-switch/eps.htm for the 4 socket model (ePowerSwitch-4).
Tested on ePowerSwitch-4.
"""

import base64
import httplib2
import string
import re

class EpsSocket:
	""" class for ePowerSwitch power outlets """
	""" each EpsSocket has a number, name, status and an unknown parameter """
	def __init__(self, number, name, status, param):
		self.number = number
		self.name = name
		self.status = status
		self.param = param
	
	number = 0
	name = ''
	status = 0
	param = 0

class EpsSwitch:
	""" class for ePowerSwitch power outlets """
	""" each EPowerSwitch has 1, 2, 4 or 8 EpsSockets, name, ip, user and pw """

	def __init__(self, ip, port, user, password):
		self.port = port
		self.url = 'http://'+ip+'/config/home_f.html:'+self.port
		self.user = user
		self.password = password
		self.auth = base64.encodestring(self.user + ':' + self.password)
		self.h = httplib2.Http()
		self.header = { 'Authorization' : 'Basic ' + self.auth }

	name = ''
	port = '80'
	url = ''
	sockets = []
	user = ''
	password = ''
	auth = ''
	h = ''
	header = ''

	def getData(self):
		""" getData function """
		""" retrieve data from ePowerSwitch power outlet """
		""" data is the name, socketname and status """

		del self.sockets[:]
		resp, content = self.h.request(self.url, 'GET', headers=self.header)
		if content == '401 Authorization Required':
			print 'Webserver is too slow. \nPlease repeat the request'
			return False
		else:
			lines = string.split(content, '\n')
			tmp_name = [s for s in lines if "hfr(\"" in s]
			self.name = re.search(r"\"(.+)\"",tmp_name[0]).group(1).strip()
		
			sockets = [s for s in lines if "socket(" in s]
			for socket in sockets:
				item = re.search(r"\((.+)\)",socket).group(1).strip()
				number = int(item.split(',')[0]) 
				#name = re.search("\"(.+)\"",item).group(1).strip()
				name = item.split(',')[1].split()[0][1:]
				status = int(item.split(',')[2]) 
				param = int(item.split(',')[3]) 
				self.sockets.append(EpsSocket(number, name, status, param))
			return True

	
	def showStatus(self):
		""" print status of all sockets for the ePowerSwitch """
		if (self.getData()):
			print self.name
			for socket in self.sockets:
				if socket.status: 
					print '#' + str(socket.number)+', device: ' + socket.name +' is On' 
				else: 
					print '#' + str(socket.number)+', device: ' + socket.name +' is Off'
	
	def setStatus(self, number, status):
		""" set status of socket """
		name = 'P'+str(number)+'='+str(status)
		resp, content = self.h.request(self.url, 'POST', headers=self.header, body=name)
