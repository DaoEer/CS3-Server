# -*- coding: utf-8 -*-

import csdefine
import Const
from MsgLogger import g_logger

class GMToolsInterface:
	"""
	GM工具相关接口
	"""
	def __init__(self):
		self.gmProLogTimerID = self.addTimerRepeat(Const.ROLE_PROPERTIES_ADDLOG_TIME, "timerCallBack", ())
		
	def timerCallBack(self):
		"""
		timer到达
		"""
		g_logger.addPropertiesLog(self)
	
	def beforeDestroy(self):
		"""
		玩家下线时也写一次日志
		"""
		g_logger.addPropertiesLog(self)
		
		#取消timer
		self.popTimer( self.gmProLogTimerID )
		self.gmProLogTimerID = 0
