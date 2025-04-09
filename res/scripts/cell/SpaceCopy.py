# -*- coding: utf-8 -*-

import time
import Math
from CoreObject.SpaceObject import SpaceObject
import csdefine
import Const
import KBEngine
import Functions
import KBEMath
import KBEDebug

class SpaceCopy( SpaceObject ):
	def __init__( self ):
		SpaceObject.__init__( self )
		self.createTime = time.time()
		
	def setDynamicReviverInfo( self, positionStr, directionStr ):
		"""
		<Define method>
		设置副本动态复活点
		positionStr x y z|x y z		#仙道动态复活坐标|魔道动态复活坐标 如果只填了一个，说明仙道魔道共用复活点
		directionStr x y z|x y z
		"""
		posList = positionStr.split("|")
		dirList = directionStr.split("|")
		taosimPos = Functions.vector3TypeConvert(posList[0])
		self.dynamicTaosimReviverPos = KBEMath.Unreal2KBEnginePosition(taosimPos)
		if len(posList) > 1:
			demonPos = Functions.vector3TypeConvert(posList[1])
			self.dynamicDemonReviverPos = KBEMath.Unreal2KBEnginePosition(demonPos)
		else:
			self.dynamicDemonReviverPos = KBEMath.Unreal2KBEnginePosition(taosimPos)

		taosimDir = Functions.vector3TypeConvert(dirList[0])
		self.dynamicTaosimReviverDir = KBEMath.Unreal2KBEngineDirection(taosimDir)
		if len(dirList) > 1:
			demonDir = Functions.vector3TypeConvert(dirList[1])
			self.dynamicDemonReviverDir = KBEMath.Unreal2KBEngineDirection(demonDir)
		else:
			self.dynamicDemonReviverDir = KBEMath.Unreal2KBEngineDirection(taosimDir)
		
	def getDynamicReviverInfo( self, camp = csdefine.CMAP_NONE ):
		"""
		<Define method>
		获取副本动态复活点
		"""
		if camp == csdefine.CAMP_TAOSIM:
			return (self.dynamicTaosimReviverPos,self.dynamicTaosimReviverDir)
		elif camp == csdefine.CAMP_DEMON:
			return (self.dynamicDemonReviverPos,self.dynamicDemonReviverDir)
		else:
			return  (self.dynamicTaosimReviverPos,self.dynamicTaosimReviverDir)
	
	def addEntityRecord( self, scriptID, entityID ):
		"""
		virtual method
		记录entity（所有继承于NPCBaseObject的entity）ID
		"""
		if scriptID in self.entityRecord:
			self.entityRecord[ scriptID ].append( entityID )
		else:
			self.entityRecord[ scriptID ] = [ entityID ]
	
	def delEntityRecord( self, scriptID, entityID ):
		"""
		virtual method
		删除entity记录
		"""
		if scriptID not in self.entityRecord:
			return
		if entityID not in self.entityRecord[ scriptID ]:
			return
		for player in self._spaceRoles:
			if player and player.getClient():
				player.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_KILL_BOSS )
		self.entityRecord[ scriptID ].remove( entityID )
		if len( self.entityRecord[ scriptID ] ) == 0:
			self.entityRecord.pop( scriptID )
	
	def getEntityRecord( self, scriptID ):
		"""
		获取某scriptID的entity
		"""
		return self.entityRecord.get( scriptID, [] )
	
	def getAllEntityRecord( self ):
		"""
		"""
		return self.entityRecord

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		if scriptID in self.entityMailBoxRecord:
			self.entityMailBoxRecord[scriptID].append(entityMailBox)
		else:
			self.entityMailBoxRecord[scriptID] = [entityMailBox]

	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除entityMailBox 记录
		"""
		if scriptID not in self.entityMailBoxRecord:
			return
		if entityMailBox not in self.entityMailBoxRecord[scriptID]:
			return
		self.entityMailBoxRecord[scriptID].remove(entityMailBox)
		if len( self.entityMailBoxRecord[scriptID] ) == 0:
			self.entityMailBoxRecord.pop( scriptID )

	def getEntityMailBoxRecord( self, scriptID ):
		"""
		获取某scriptID的entity
		"""
		return self.entityMailBoxRecord.get( scriptID, [] )

	def getAllEntityMailBoxRecord( self ):
		"""
		"""
		return self.entityMailBoxRecord
	
	def getSpaceStatisticsNum( self, entryIndex ):
		"""获取统计数值"""
		if self.spaceStatistics:
			return self.spaceStatistics.getSpaceStatisticsNum( entryIndex )
		else:
			KBEDebug.ERROR_MSG("Space getSpaceStatisticsNum err!")
		return 0
					
	def getEntityDynamicPosBigMapShow( self, player, scriptID ):
		"""获取entity在大地图的位置"""
		entityIDs = self.getCurrentSpace().getEntityRecord(scriptID)
		entities=[]
		for entityID in entityIDs:
			e =KBEngine.entities.get(entityID, None)
			if e:
				entities.append(e)
		return entities