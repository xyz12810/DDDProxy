# -*- coding: UTF-8 -*-
'''
Created on 2015年9月12日

@author: dxw
'''
import sys
import traceback
import time
import logging

debuglevel = 2

def log(level, *args, **kwargs):
	if level < debuglevel:
		return
	
	data = "	".join(str(i) for i in args)
	data += "	".join("%s=%s"%(str(k),str(v)) for k,v in kwargs.items())
	if level==3:
		data += "	"+str(sys.exc_info())
		data += "	"+str(traceback.format_exc())
	
	data = time.strftime("%y-%B-%d %H:%M:%S:	")+ data
	if level<2:
		print data
	else:
		logging.log([logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR][level], data)
if __name__ == "__main__":
	log(3,"123")
	log(2,"123")
	log(1,"123")
	log(0,"123")
	
	
	