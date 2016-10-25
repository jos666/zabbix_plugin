#!/usr/bin/env python
# author : finy
# openvpn config file add: management localhost 7505
# need nc command; if not, install nc 

import os, re, sys

dirname = os.path.dirname(__file__)
if dirname != "/opt/zabbix/scripts":
	print "------------------INSTALl---------------------------"
	print "openvpn config file add: management localhost 7505"
	print "restart openvpn"
	print "Please put this script in /opt/zabbix/scripts directory"
	print "command: mkdir -p /opt/zabbix/scripts;mv %s /opt/zabbix/scripts/" % __file__
	exit()
command = '''echo load-stats | python -c "import subprocess;import time;a=subprocess.Popen(['nc','127.0.0.1','7505']);time.sleep(0.01);a.kill()" | grep -v Management'''
data = {}

try:
	result = os.popen(command)
	values = re.findall('\w+=\d+', result.read())
	for v in values:
		keyname,keyval = v.split('=')
		data[keyname] = keyval
except Exception, e:
	pass

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: %s key" % sys.argv[0]
		print "\t key: [%s]" % '|'.join(data.keys())
		exit(0)
	try:
		print data[sys.argv[1]]
	except:
		print 0
