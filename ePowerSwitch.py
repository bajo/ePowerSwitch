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
import prettytable

class EpsSocket:
	""" class for ePowerSwitch power outlets """
	""" each EpsSocket has a number, name, status and an unknown parameter """
	def __init__(self, number, name, status, param, cycles):
		self.number = number
		self.name = name
		self.status = status
		self.param = param
		self.cycles = cycles
	
	number = 0
	name = ''
	status = 0
	param = 0
	cycles = 0

class EpsSwitch:
	""" class for ePowerSwitch power outlets """
	""" each EPowerSwitch has 1, 2, 4 or 8 EpsSockets, name, ip, user and pw """

	def __init__(self, ip, port, user, password):
		self.port = port
		self.url = 'http://'+ip+':'+self.port+'/'
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
		""" data is the name, socketname, status and count of power cycles """

		del self.sockets[:]
		resp, content = self.h.request(self.url+'config/home_f.html', 'GET', headers=self.header)
		resp, content = self.h.request(self.url+'cmd.html', 'GET', headers=self.header)
		if content == '401 Authorization Required':
			print 'Webserver is too slow. \nPlease repeat the request'
			return False
		else:
			cycles = dict()
			resp2, content2 = self.h.request(self.url+'config/misc_f.html', 'GET', headers=self.header)
			if content == '401 Authorization Required':
				print 'user '+self.username+'is not the administration user.\n Power cycle count will not be available'
			else:
				lines2 = string.split(content2, '\n')
				sockets2 = [s for s in lines2 if "Socket" in s]
				for item in sockets2:
					a = re.search(r"Socket(.+)\)",item)
					b = a.group(1).split(',')[0].split('"')[0].strip()
					c = a.group(1).split(',')[1].strip()
					cycles[b] = c

			lines = string.split(content, '\n')
			tmp_name = [s for s in lines if "H1" in s]
			sockets = [s for s in lines if "socket(" in s]
			self.name = re.search(r"<H1>(.+)<\/H1>",tmp_name[0]).group(1).strip()

			for socket in sockets:
				item = re.search(r"\((.+)\)",socket).group(1).strip()
				number = int(item.split(',')[0]) 
				name = item.split(',')[1].split()[0][1:]
				status = int(item.split(',')[2]) 
				param = int(item.split(',')[3]) 
				if len(cycles) < number:
					cycles[str(number)] = 'None'
				self.sockets.append(EpsSocket(number, name, status, param, cycles[str(number)]))
			return True

	def showStatus(self):
		""" print status of all sockets for the ePowerSwitch """
		if (self.getData()):
			print self.name
			x = prettytable.PrettyTable(['socket number', 'connected device', 'status', 'power cycles'])
			for socket in self.sockets:
				if socket.status: 
					status = 'On'
				else: 
					status = 'Off'
				x.add_row([socket.number, socket.name, status, socket.cycles])
			print x
	
	def setStatus(self, number, status):
		""" set status of socket """
		if status.lower() in {'on','On','1'}:
			name = 'P'+str(number)+'=1'
		elif status.lower() in {'off','Off','0'}:
			name = 'P'+str(number)+'=0'
		else: 
			return False
		resp, content = self.h.request(self.url+'cmd.html', 'POST', headers=self.header, body=name)
		return True
