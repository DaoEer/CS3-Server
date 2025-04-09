# -*- coding: utf-8 -*-

from SpaceMultiLine import SpaceMultiLine
import Const
import KBEDebug
import KBEngine
import Math

class SpaceLunHuiMiJinMultiLine( SpaceMultiLine ):
	def __init__( self ):
		SpaceMultiLine.__init__( self )
		self.entityRecordbyGroup = {}				#  {group : entityID, group1:entityID1...}

	def activityStart( self ):
		"""
		define method
		活动开始(开始刷怪)
		"""
		self.openActivitySpawn = True
		self.createSpawnEntityBySpawnType( "SpawnPointRandomExtActivity" )

	def activityEnd( self ):
		"""
		活动结束(停止刷怪)
		"""
		self.openActivitySpawn = False
		
	def onEnter( self, playerRole, packArgs ):
		""""""
		SpaceMultiLine.onEnter( self, playerRole, packArgs )
		self.onPlayerRoleEnterSpace( playerRole )
		self.showMessageBackFromJiYuan(packArgs)


	def showMessageBackFromJiYuan(self, packArgs):
		"""
		从机缘副本返回时，广播消息
		"""
		if "jiyuanSpaceName" in packArgs:
			for role in self._spaceRoles:
				role.showMessagePlaySound(csstatus.LHMJ_JYWF_BACK, role.playerName, packArgs["jiyuanSpaceName"])
		
	def onLogin( self, playerRole ):
		""""""
		SpaceMultiLine.onLogin( self, playerRole )
		self.onPlayerRoleEnterSpace( playerRole )
		
	def onPlayerRoleEnterSpace( self, playerRole ):
		""""""
		if playerRole.activeChartID:						# 玩家激活了阵图
			for group in playerRole.groundPosDict.keys():
				if group in self.entityRecordbyGroup:
					id = self.entityRecordbyGroup[group]
					entityObject = KBEngine.entities.get(id, None)
					if entityObject and entityObject.belongDBID == playerRole.playerDBID:
						entityObject.setPlayerMB( playerRole )
		
	def createCellEntityByScriptID(self, id, playerDBID, scriptID, npcID, group):
		"""
		define method
		创建cellEntity
		"""
		npc = KBEngine.entities.get( npcID )
		if npc is None:
			KBEDebug.ERROR_MSG("player(dbid:%d) Create Entity(%s) err!! can not find npcID(%d)"%(playerDBID, scriptID, npcID))
			return
		param = {}
		param["ownerID"] = id
		param["belongDBID"] = playerDBID
		entityObject = self.createEntityByScriptID(scriptID, npc.position, npc.direction, param)
		if entityObject:
			self.entityRecordbyGroup[group] = entityObject.id
	
	def noticeMECPEnter(self, group, playerID):
		"""
		define method
		通知罩子，攻方来了
		"""
		if group in self.entityRecordbyGroup:
			entityID = self.entityRecordbyGroup.pop(group)
			entityObj = KBEngine.entities.get(entityID, None)
			if entityObj:
				entityObj.noticeMECPEnter( playerID )
	
	def destroyCellEntityByScriptID(self, group):
		"""
		define method
		销毁cellEntity
		"""
		if group in self.entityRecordbyGroup:
			entityID = self.entityRecordbyGroup.pop(group)
			entityObj = KBEngine.entities.get(entityID, None)
			if entityObj:
				entityObj.destroySelf()
			
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