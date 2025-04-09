# -*- coding: utf-8 -*-


import KBEDebug
import KBEngine
from CoreObject import MgrPersistentObject
import time
import json
import Functions
import csstatus
import KST
import csconst
from MsgLogger import g_logger
import csdefine
import Const


class MsgLogMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	日志管理
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		
		self.onlineMacs = []
		self.onlineRoleNum = 0
		self.msgOnlineTimerID = self.addTimerRepeat(Const.MSG_TPYE_ONLINE_RECORD, "onlineRecordCallback", ())
		self.onCompleteInit()
		
	def onlineRecordCallback(self):
		"""
		timer到达
		"""
		onlineMacNum = len(set(self.onlineMacs))
		g_logger.onlineRecord(1, self.onlineRoleNum, onlineMacNum)
	
	def onRoleLogin(self, mac):
		"""
		玩家上线
		"""
		self.onlineRoleNum += 1
		self.onlineMacs.append(mac)
		
	def onRoleLogoff(self, mac):
		"""
		玩家下线
		"""
		self.onlineRoleNum -= 1
		if mac in self.onlineMacs:
			self.onlineMacs.remove(mac)
		

