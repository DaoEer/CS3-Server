# -*- coding: utf-8 -*-

# 副本统计

import Functions
import Define
import SmartImport
from KBEDebug import *
from SpaceStatisticsDataType import SpaceStatisticsDataType


class SpaceStatistics( SpaceStatisticsDataType ):
	def __init__( self ):
		self.title = ""
		self.questID = 0
		self.comment = ""
		self.statisticsList = []
		
	def init( self, datas ):
		self.title = datas["title"]
		self.questID = datas["questID"]
		self.comment = datas["comment"]
		for indexStr, entrySection in datas["entrys"].items():
			entryClass = SmartImport.smartImport( "ConfigObject.SpaceStatistics.SpaceStatisticsEntry:" + entrySection["type"] )
			instance = entryClass()
			instance.init( int(indexStr), entrySection )
			self.statisticsList.append( instance )
		self.statisticsList.sort(key = lambda x:x.entryIndex)
		
	def packToString( self ):
		"""
		"""
		tempDict = self.getDictFromObj( self )
		return Functions.toJsonString( [ tempDict ] )
		
	def getSpaceStatisticsNum( self, entryIndex ):
		"""获取统计数值"""
		if len( self.statisticsList ) - 1 >= entryIndex:
			return self.statisticsList[entryIndex].value
		else:
			ERROR_MSG("Space getSpaceStatisticsNum err!")
		return 0
	
	def onMonsterDie( self, spaceEntity, scriptID ):
		"""
		"""
		resultList = []
		for statistics in self.statisticsList:
			if statistics.getType() == Define.SPACE_STATISTICS_ENTRY_KILL_MONSTER:
				if statistics.checkMonsterScriptID( scriptID ):
					statistics.onNumChange( spaceEntity )
					resultList.append( (statistics.entryIndex, statistics.value) )
		return resultList
		
	def onConditionChange( self, spaceEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		"""
		resultList = []
		for statistics in self.statisticsList:
			if statistics.getType() == Define.SPACE_STATISTICS_ENTRY_CONDITION_CHANGE:
				if statistics.checkCondition( senderType, senderID, conditionKey, extraValue ):
					statistics.onNumChange( spaceEntity )
					resultList.append( (statistics.entryIndex, statistics.value) )
		return resultList

	def onPlayerGetItem( self, spaceEntity, itemID, amount ):
		"""
		"""
		resultList = []
		for statistics in self.statisticsList:
			if statistics.getType() == Define.SPACE_STATISTICS_ENTRY_GET_ITEM:
				if statistics.onAddItem( itemID, amount ):
					statistics.onNumChange( spaceEntity )
					resultList.append( (statistics.entryIndex, statistics.value) )
		return resultList

	def onPlayerRemoveItem( self, spaceEntity, itemID, amount ):
		"""
		"""
		resultList = []
		for statistics in self.statisticsList:
			if statistics.getType() == Define.SPACE_STATISTICS_ENTRY_GET_ITEM:
				if statistics.onRemoveItem( itemID, amount ):
					resultList.append( (statistics.entryIndex, statistics.value) )
		return resultList
		
	#------------------------------获取物品类目标特殊处理---------------------------------
	def updateGetItemTask( self, spaceEntity ):
		"""
		刷新一下获取物品类目标的已完成数量
		注：重新计算所有玩家的物品数
		"""
		resultList = []
		for statistics in self.statisticsList:
			if statistics.getType() == Define.SPACE_STATISTICS_ENTRY_GET_ITEM:
				statistics.updateItemNum( spaceEntity )
