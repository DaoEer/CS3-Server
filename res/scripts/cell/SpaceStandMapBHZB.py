# -*- coding: utf-8 -*-

from CoreObject.SpaceObject import SpaceObject
import Const
import KBEDebug
import csdefine
import KBEngine

class SpaceStandMapBHZB( SpaceObject ):
	"""
	帮会争霸沙盘大地图
	"""
	def __init__( self ):
		SpaceObject.__init__( self )
		self.setCurrentSpaceData( Const.SPACE_DATA_LINE_NUMBER,self.spaceKey )
		
	def setMaxLineNumber( self, maxLineNumber ):
		"""
		设置最大线数
		"""
		self.setCurrentSpaceData( Const.SPACE_DATA_MAX_LINE_NUMBER, str(maxLineNumber) )

	def registerRole( self, roleMB ):
		"""
		记录空间玩家
		"""
		SpaceObject.registerRole( self, roleMB )
		if roleMB.playerDBID not in self.spaceRoleDict:
			self.spaceRoleDict[roleMB.playerDBID] = roleMB

	def deregisterRole( self, roleMB ):
		"""
		删除空间玩家
		"""
		SpaceObject.deregisterRole( self, roleMB )
		if roleMB.playerDBID in self.spaceRoleDict:
			del self.spaceRoleDict[roleMB.playerDBID]

	def getRoleMBByPlayerDBID( self, playerDBID ):
		"""
		通过玩家DBID 获得玩家的Mailbox
		"""
		if playerDBID in self.spaceRoleDict:
			return self.spaceRoleDict[playerDBID]

		return None

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_NPC_POINT:
			self.spacePointDict[ entityMailBox.getIndex() ] = entityMailBox

	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除entityMailBox 记录
		"""
		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_NPC_POINT and entityMailBox.getIndex() in self.spacePointDict:
			del self.spacePointDict[entityMailBox.getIndex()]

	def getNPCPointEntityByIndex( self, index ):
		"""
		"""
		if index in self.spacePointDict:
			return self.spacePointDict[index]
		return None

	def onRequestBHZBPointDatasCB( self, pointDatas ):
		"""
		请求该分线据点的数据
		"""
		self.getScript().onRequestBHZBPointDatasCB( self, pointDatas )

	def addNPCPointData( self,lineNumber,index,occupyPlayerDBID,occupyPlayerName,occupyTongDBID,occupyTongName,pointType,fightEndTime,restEndTime,joinPlayerDBIDs,joinProtectPlayerDBIDs ):
		"""
		增加帮会争霸沙盘大地图 据点数据
		"""
		self.pointDataMgr.addNPCPointData( lineNumber,index,occupyPlayerDBID,occupyPlayerName,occupyTongDBID,occupyTongName,pointType,fightEndTime,restEndTime,joinPlayerDBIDs,joinProtectPlayerDBIDs )

	def notifySpacePointOccupy( self, lineNumber,index, occupyTongDBID,occupyTongName,occupyPlayerDBID,occupyPlayerName ):
		"""
		通知space 据点占领
		"""
		self.pointDataMgr.updateOccupyPointData( lineNumber,index, occupyTongDBID,occupyTongName,occupyPlayerDBID,occupyPlayerName )
		npcEntity = self.getNPCPointEntityByIndex( index )
		if not npcEntity:
			return
		npcEntity.setNPCExtPointState( csdefine.NPCEXTPOINT_STATE_REST )

	def notifySpacePointState( self, index ):
		"""
		改变据点状态
		"""
		npcEntity = self.getNPCPointEntityByIndex( index )
		if not npcEntity:
			return
		npcEntity.setNPCExtPointState( csdefine.NPCEXTPOINT_STATE_REST )

