# -*- coding: utf-8 -*-

# 副本统计条目

import SpaceStatisticsEntryDataType
import Define

class SpaceStatisticsEntryBase( SpaceStatisticsEntryDataType.SpaceStatisticsEntryDataType ):
	type = Define.SPACE_STATISTICS_ENTRY_NONE
	
	def __init__( self ):
		SpaceStatisticsEntryDataType.SpaceStatisticsEntryDataType.__init__( self )
		self.entryIndex = 0
		self.title = ""
		self.value = 0
		self.postfix = ""						# 可配置单位/总量
		self.param1 = ""
		self.param2 = ""
		self.param3 = ""
		self.param4 = 0
		self.progress = 0
		
	def init( self, index, datas ):
		self.entryIndex = index
		self.title = datas["title"]
		self.value = 0 and datas["value"] or int( datas["value"])
		self.postfix = datas["postfix"]
		self.param1 = datas["param1"]
		self.param2 = datas["param2"]
		self.param3 = datas["param3"]
		self.param4 = 0 and datas["param4"] or int( datas["param4"])
		self.progress = 0 and datas["progress"] or int( datas["progress"])
		
	def getType( self ):
		return Define.SPACE_STATISTICS_ENTRY_NONE
		
	def checkStatisticsState( self ):
		"""
		是否完成统计
		"""
		if self.postfix.isnumeric():
			if int(self.postfix) <= self.value:
				return False
		return True
		
	def onNumChange( self, spaceEntity ):
		"""计数改变"""
		if self.postfix.isnumeric():
			if int(self.postfix) == self.value:
				spaceEntity.getScript().spaceEvent_onSpaceStatisticsFinish( spaceEntity, self.entryIndex )
		
class SStatisticsEntry_killMonster( SpaceStatisticsEntryBase ):
	"""杀怪"""
	def getType( self ):
		return Define.SPACE_STATISTICS_ENTRY_KILL_MONSTER
		
	def checkMonsterScriptID( self, scriptID ):
		if not self.checkStatisticsState():return False
		scriptIDList = self.param1.split("|")
		if scriptID in scriptIDList:
			self.value += 1
			return True
		return False
		
class SStatisticsEntry_conditionChange( SpaceStatisticsEntryBase ):
	"""副本某条件改变"""
	def getType( self ):
		return Define.SPACE_STATISTICS_ENTRY_CONDITION_CHANGE
	
	def checkCondition( self, senderType, senderID, conditionKey, extraValue ):
		if not self.checkStatisticsState():return False
		if self.param1 and self.param1 != senderType:		# 发送者类型：AI填“AI”，镜头事件填“STORY”
			return False
		if self.param2:
			idList = self.param2.split( "|" )
			if senderID not in idList:			# 发送者ID：AI填发送者scriptID，镜头事件填镜头ID
				return False
		if self.param3 != conditionKey:						# 通知ID：string类型
			return False
		value = 1
		if extraValue:
			value = int( extraValue )
		if self.param3.endswith("remove"):
			self.value -= value
		else:
			self.value += value
		return True
		
class SStatisticsEntry_getItem( SpaceStatisticsEntryBase ):
	def getType( self ):
		return Define.SPACE_STATISTICS_ENTRY_GET_ITEM
		
	def onAddItem( self, itemID, amount ):
		if not self.checkStatisticsState():return False
		if int( self.param1 ) == itemID:
			self.value += amount
			return True
		return False
		
	def onRemoveItem( self, itemID, amount ):
		if int( self.param1 ) == itemID:
			self.value -= amount
			return True
		return False
		
	def updateItemNum( self, spaceEntity ):
		"""
		获取所有玩家某物品总数
		"""
		hasAmount = 0
		itemList = []
		itemID = int( self.param1 )
		
		for e in spaceEntity._spaceRoles:
			itemList.extend( e.getItemInstsByID( itemID ))
			
		for itemInst in itemList:
			hasAmount += itemInst.amount
		if hasAmount:
			self.value += hasAmount

class SStatisticsEntry_CountDown( SpaceStatisticsEntryBase ):
	"""倒计时"""
	def getType( self ):
		return Define.SPACE_STATISTICS_ENTRY_COUNT_DOWN

SpaceStatisticsEntryDataType.MAP_ENTRY_TYPE_TO_ENTRY_CLASS( Define.SPACE_STATISTICS_ENTRY_KILL_MONSTER, SStatisticsEntry_killMonster )
SpaceStatisticsEntryDataType.MAP_ENTRY_TYPE_TO_ENTRY_CLASS( Define.SPACE_STATISTICS_ENTRY_CONDITION_CHANGE, SStatisticsEntry_conditionChange )
SpaceStatisticsEntryDataType.MAP_ENTRY_TYPE_TO_ENTRY_CLASS( Define.SPACE_STATISTICS_ENTRY_GET_ITEM, SStatisticsEntry_getItem )
SpaceStatisticsEntryDataType.MAP_ENTRY_TYPE_TO_ENTRY_CLASS( Define.SPACE_STATISTICS_ENTRY_COUNT_DOWN, SStatisticsEntry_CountDown )