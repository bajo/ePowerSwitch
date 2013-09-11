#!/usr/bin/env python
# Filename: ePS.py

"""ePS, ePowerSwitch client

Connect to ePowerSwitch webserver on <host> and <port>, login with <username> and <password>.
get retrieves the current sockets states (On or Off)
set set <socket> to On or Off

Usage:
	ePS.py <host> [<port>] <username> <password> get
	ePS.py <host> [<port>] <username> <password> set <socket> <on>|<off>
	ePS.py (-h | --help)
	ePS.py (-v | --version)

Options:
	-h --help		Show this screen.
	-v --version		Show version.

"""

import ePowerSwitch
from docopt import docopt

if __name__ == '__main__':
	arguments = docopt(__doc__, version='ePowerSwitch client 0.1')

	eps = ePowerSwitch.EpsSwitch(arguments['<host>'], arguments['<port>'], arguments['<username>'], arguments['<password>'])

	if arguments['get']:
		eps.showStatus()
	elif arguments['set']:
		eps.setStatus(arguments['<socket>'], arguments['<on>'])
