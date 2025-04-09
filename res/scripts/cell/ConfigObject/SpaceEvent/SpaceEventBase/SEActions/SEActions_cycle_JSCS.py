# -*- coding: utf-8 -*-

# 急速穿梭 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction306( SEActionBase ):
	"""
	CST-6021 急速穿梭:设置传送门封锁锁开关
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self._isTrue = bool(int(section["param1"]))  # 填0 或者 1
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if spaceEntity:
			spaceEntity.setIsCloseDoor(self._isTrue)

class SEAction309( SEActionBase ):
	"""
	急速穿梭: 急速穿梭传送门刷新倒计时界面   CST-7711
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		self._time = 0
		if section["param1"]:
			self._time = int(section["param1"])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		strTime = ""
		if self._time:
			strTime = str(self._time * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime())
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_ShowJSCSCountDownUI(strTime)

class SEAction310( SEActionBase ):
	"""
	急速穿梭: 急速穿梭传送门刷新提示  CST-7711
	"""
	def init ( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_ShowJSCSTipsUI()

SEActionBase.setActionClass("SEAction306", SEAction306)
SEActionBase.setActionClass("SEAction309", SEAction309)
SEActionBase.setActionClass("SEAction310", SEAction310)