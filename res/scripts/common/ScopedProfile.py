# -*- coding: utf-8 -*-

"""
用法:
import ScopedProfile
ScopedProfile.start( "scopedName", 0.01 )

# some code to execute...
...

ScopedProfile.stop( "scopedName" )
"""

import time, sys

import KBEngine
#from KBEDebug import *

class ScopedProfile(object):
	"""
	"""
	def __init__( self, name, logTime ):
		"""
		"""
		self.start( name, logTime )
	
	def start( self, name, logTime ):
		"""
		@param name: string; 表示该项检查的名称
		@param logTime: float; 表示超过这个时间时就会输出相应的日志
		"""
		self.name = name
		self.logTime = logTime
		self.st = time.time()

	def stop( self ):
		"""
		"""
		t = time.time() - self.st
		if t >= self.logTime:
			# 这里不使用ERROR_MSG()之类的封装函数，以减少不必要的消耗，提高精度
			KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
			print( "%s: scriptCall took %s seconds" % (self.name, t) )


# key = scoped name
# vlaue = instance of ScopedProfile
_scoped_map = {}

def start( name, logTime ):
	"""
	@param name: string; 表示该项检查的名称
	@param logTime: float; 表示超过这个时间时就会输出相应的日志
	"""
	assert name not in _scoped_map
	_scoped_map[name] = ScopedProfile(name, logTime)

def stop( name ):
	"""
	"""
	_scoped_map["name"].stop()

