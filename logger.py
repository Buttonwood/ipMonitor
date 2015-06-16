#!/usr/bin/env python
# encoding: utf-8
import logging 
from helper import u_to_s

def setLogger(log_name,log_file):
	logger = logging.getLogger(log_name)
	logger.setLevel(logging.DEBUG) 
	fh = logging.FileHandler(log_file)  
	fh.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
	fh.setFormatter(formatter) 
	logger.addHandler(fh)
	return logger

class Logger(object):
	"""docstring for Logger"""
	def __init__(self, log_name, log_file):
		super(Logger, self).__init__()
		self.logger = setLogger(log_name,log_file)

	def info(self,msg):
		self.logger.info(u_to_s(msg))

	def warn(self,msg):
		self.logger.warn(u_to_s(msg))

def main():
	mlogger = Logger('iplogger', 'ipMonitor.log')
	mlogger.info("谭浩!Here we go!")
	mlogger.warn("谭浩!Here you wrong!")

if __name__ == '__main__':
	main()