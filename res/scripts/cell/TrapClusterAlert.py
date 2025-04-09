# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
from Trap import Trap


class TriggerConQuestStatus:
	"""
	检测任务状态
	参数1："qID:qState;tID:tState;tID:tState|...."
	"""
	def __init__( self ):
		self.quests = []
	
	def init( self, conDict ):
		self.quests = []
		for questTaskStr in conDict["param1"].split("|"):
			questDict = {}
			tempStrList = questTaskStr.split(";")
			
			questStr = tempStrList.pop(0)
			qId, qState = questStr.split(":")
			questDict["questID"] = int(qId)
			questDict["questState"] = int(qState)
			
			if tempStrList:
				taskIDList = []
				taskStateList = []
				for taskStr in tempStrList:
					tId, tState = taskStr.split(":")
					taskIDList.append( int(tId) )
					taskStateList.append( int(tState) )
				questDict["taskIDs"] = taskIDList
				questDict["taskStates"] = taskStateList
			
			self.quests.append( questDict )
	
	def check( self, roleEntity ):
		"""
		有一个任务满足条件即可；一个任务的任务状态和任务目标（选填项）状态都满足条件则算此任务满足条件
		"""
		for questDict in self.quests:
			if roleEntity.queryQuestStatus( questDict["questID"] ) != questDict["questState"]:
				continue
			if questDict.get("taskIDs", []):
				for index, taskID in enumerate( questDict["taskIDs"] ):
					taskState = questDict["taskStates"][index]
					if roleEntity.queryTaskStatus( questDict["questID"], taskID ) != taskState:
						continue
			return True
		
		return False


CON_TYPE_MAP = { 1: TriggerConQuestStatus }


class TrapClusterAlert( Trap ):
	"""
	集群怪统一警戒陷阱，客户端循环检测范围内是否有玩家（CST-1019）
	触发条件通过刷新点配置，不通过非公表配置
	"""
	def __init__( self ):
		Trap.__init__( self )
		#self.triggerRadius = 0		#def属性
		self.triggerConditions = []
	
	def initTriggerCon( self, config ):
		for conDict in config:
			func = CON_TYPE_MAP.get( conDict["type"], None )
			if not func:
				KBEDebug.ERROR_MSG( "TrapClusterAlert trigger condition has no type(%s)."%conDict["type"] )
			else:
				inst = func()
				inst.init( conDict )
				self.triggerConditions.append( inst )

	def CELL_onEnter( self, exposed, enterID ):
		"""
		Exposed Method.
		进入客户端陷阱
		"""
		roleEntity = KBEngine.entities.get( enterID )
		if not roleEntity:
			return
		
		if not roleEntity.isReady() or roleEntity.inDestroying():
			return
		
		for con in self.triggerConditions:
			if not con.check( roleEntity ):
				return
		
		spawnIndex = getattr( self, "spawnIndex", -1 )
		if spawnIndex < 0:
			return
		
		#通知刷新点将踩陷阱的玩家加到所有怪物的敌人列表
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.callSpawnFunction( spawnIndex, "addEnemyToAllEntity", (enterID,) )
	
	def CELL_onLeave( self, exposed, enterID ):
		"""
		Exposed Method.
		离开客户端陷阱
		"""
		pass