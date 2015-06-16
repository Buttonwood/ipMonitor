#!/usr/bin/env python
# encoding: utf-8
import socket, fcntl, struct  

def get_hostname():
	return socket.gethostname()

def get_local_ip(ifname = 'eth0'):  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
    ret = socket.inet_ntoa(inet[20:24])  
    return ret  
  
def	to_unicode(unicode_or_str):
	if	isinstance(unicode_or_str,	str):
		value =	unicode_or_str.decode('utf-8')
	else:
		value =	unicode_or_str
	return	value

def	to_str(unicode_or_str):
	if	isinstance(unicode_or_str,	unicode):
		value =	unicode_or_str.encode('utf-8')
	else:
		value =	unicode_or_str
	return	value

def u_to_s(unicode_or_str):
	return to_str(to_unicode(unicode_or_str))

def main():
	ustr = u'谭浩'
	print(to_unicode(ustr))
	print(to_str(to_unicode(ustr)))
	print(u_to_s(ustr))
	print(get_local_ip())
	print(get_hostname())  

if __name__ == '__main__':
	main()