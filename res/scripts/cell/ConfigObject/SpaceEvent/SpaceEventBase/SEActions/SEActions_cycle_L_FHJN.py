# -*- coding: utf-8 -*-
# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction239( SEActionBase ):
	"""
	环任务副本 焚火金牛
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.randomSelectChannel()

class SEAction368( SEActionBase ):
	"""
	环任务副本 焚火金牛 显示血条和血条信息
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.maxCount = int(section["param1"])
		self.curCount = 0
		if section["param2"]:
			self.curCount = int(section["param2"])
		self.describe = section["param3"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.setTemp("FHJN_MaxCount",self.maxCount )
		spaceEntity.setTemp("FHJN_CurCount",self.curCount )
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.ShowFHJNSpecialWidget(self.maxCount, self.curCount,self.describe)

class SEAction369( SEActionBase ):
	"""
	环任务副本 焚火金牛 移除血条和血条信息
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.removeTemp( "FHJN_MaxCount" )
		spaceEntity.removeTemp( "FHJN_CurCount" )
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.HideFHJNSpecialWidget()

class SEAction370( SEActionBase ):
	"""
	环任务副本 焚火金牛 更新血条信息血条
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.reduceCount = int( section["param1"] )
		self.notifyID = section["param2"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		maxCount = spaceEntity.queryTemp("FHJN_MaxCount")
		curCount = spaceEntity.queryTemp("FHJN_CurCount")
		if not maxCount or not curCount:
			return
		curCount = curCount - self.reduceCount
		if curCount < 0:
			curCount = 0
		if curCount == 0:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, self.notifyID, "")
		spaceEntity.setTemp( "FHJN_CurCount", curCount )
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.UpdateFHJNSpecialWidget( maxCount, curCount )

SEActionBase.setActionClass("SEAction239", SEAction239)
SEActionBase.setActionClass("SEAction368", SEAction368)
SEActionBase.setActionClass("SEAction369", SEAction369)
SEActionBase.setActionClass("SEAction370", SEAction370)