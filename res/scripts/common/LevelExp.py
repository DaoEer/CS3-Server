# -*- coding:utf-8 -*-

from KBEDebug import *

import LevelExpData.RoleExp as RoleExp
import csconst



class RoleLevelExp:
	__maxLv = 1
	__datas = {}

	@classmethod
	def init( cls ):
		cls.__maxLv = csconst.ROLE_EXP_MAX_LEVEL
		cls.__datas = RoleExp.Datas

	@classmethod
	def getMaxLv( cls ):
		"""
		get the maxLV
		@rtype:		int
		@return:	the maxLV
		"""
		return cls.__maxLv

	@classmethod
	def getMaxExp( cls, level ):
		"""
		get matching exp
		@type 			level: int
		@param			level: level of the role
		@rtype				 : int
		@return 			 : EXP value
		"""
		try:
			return cls.__datas[ level ]
		except:
			ERROR_MSG("level error or not initialize")
		return None


