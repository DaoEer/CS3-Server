# -*- coding: utf-8 -*-

# 副本阶段显示功能接口

import copy
import time
import Functions
from LoadModule import *
import KBEDebug
import Define
import csdefine
from ConfigObject.SpaceStatistics.SpaceStatistics import *
from ConfigObject.SpaceStatistics.SpaceStatisticsEntry import *

class SpaceStatisticsInterface:
	"""
	"""
	def __init__( self ):
		self.spaceStatisticsList = []						
	
	def initSpaceStatistics( self, fileName ):
		"""
		初始化阶段数据
		"""
		section = openJsonCfg( "GameObject/SpaceObject/SpaceStatisticsFile/%s.json"%fileName )
		self.statisticsFileName = section.get( "name", "" )
		for indexStr, statisticsSec in section["statistics"].items():
			instance = SpaceStatistics()
			instance.init( statisticsSec )
			self.spaceStatisticsList.append( instance )
	
	def hasSpaceStatistics( self, selfEntity ):
		return selfEntity.spaceStatistics and isinstance( selfEntity.spaceStatistics, SpaceStatistics )
	
	def updateSpaceStatistics( self, selfEntity, changedStatistics ):
		"""
		统计计数更新
		"""
		if len( changedStatistics ) == 0:
			return
		
		tempList = []
		for index, value in changedStatistics:
			tempList.append( { "entryIndex":index, "value":value } )
		tempString = Functions.toJsonString( tempList )
		for roleCell in selfEntity._spaceRoles:
			roleCell.client.CLIENT_updateSpaceStatistics( tempString )
	
	def spaceStatistics_onSpaceInit( self, selfEntity ):
		"""
		副本开始初始化
		设置副本当前统计
		"""
		selfEntity.spaceStatistics = None
		if self.spaceStatisticsList:
			selfEntity.spaceStatistics = copy.deepcopy( self.spaceStatisticsList[0] )

	def spaceStatistics_onPlayerEnter( self, selfEntity, roleCell ):
		"""
		玩家进副本
		"""
		if not self.hasSpaceStatistics( selfEntity ):
			return
		selfEntity.spaceStatistics.updateGetItemTask( selfEntity )
		roleCell.client.CLIENT_showSpaceStatistics( self.statisticsFileName, selfEntity.spaceStatistics.packToString() )
			
	def spaceStatistics_onPlayerLeave( self, selfEntity, roleCell ):
		"""
		玩家退出副本
		"""
		if not self.hasSpaceStatistics( selfEntity ):
			return
			
		roleCell.client.CLIENT_hideSpaceStatistics()
		
	def spaceStatistics_onMonsterDie( self, selfEntity, monsterScriptID ):
		"""
		怪物死亡
		"""
		if not self.hasSpaceStatistics( selfEntity ):
			return
		changedTasks = selfEntity.spaceStatistics.onMonsterDie( selfEntity, monsterScriptID )
		self.updateSpaceStatistics( selfEntity, changedTasks )

	def spaceStatistics_onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		副本某条件发生改变
		"""
		if not self.hasSpaceStatistics( selfEntity ):
			return
		changedTasks = selfEntity.spaceStatistics.onConditionChange( selfEntity, senderType, senderID, conditionKey, extraValue )
		self.updateSpaceStatistics( selfEntity, changedTasks )
	
	def spaceStatistics_onPlayerGetItem( self, selfEntity, itemID, amount ):
		"""
		玩家获得物品
		"""
		if not self.hasSpaceStatistics( selfEntity ):
			return
		changedTasks = selfEntity.spaceStatistics.onPlayerGetItem( selfEntity, itemID, amount )
		self.updateSpaceStatistics( selfEntity, changedTasks )
	
	def spaceStatistics_onPlayerRemoveItem( self, selfEntity, itemID, amount ):
		"""
		玩家移除物品
		"""
		if not self.hasSpaceStatistics( selfEntity ):
			return
		changedTasks = selfEntity.spaceStatistics.onPlayerRemoveItem( selfEntity, itemID, amount )
		self.updateSpaceStatistics( selfEntity, changedTasks )