# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import KBEngine
import KBEDebug	

class ActionBase(metaclass=ABCMeta):
	"""
	指令基类
	"""
	_ACTION_CALSS = {}
	def __init__(self):
		"""
		"""
		pass
		
	@classmethod
	def setClass( SELF, actionName, classObj ):
		SELF._ACTION_CALSS[ actionName ] = classObj
	
	@classmethod
	def getClassObj( SELF, actionName ):
		if actionName in SELF._ACTION_CALSS:
			return SELF._ACTION_CALSS[ actionName ]( )
		return None

	@abstractmethod
	def doAction(self, role, param):
		"""
		"""
		if role.ai:
			role.ai.startAction(self.__class__.__name__, param)