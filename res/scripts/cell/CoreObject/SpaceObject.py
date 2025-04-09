# -*- coding: utf-8 -*-

"""
用于地图的基本类型
"""

import KBEngine
import Math
from KBEDebug import *
from CoreObject.GameObject import GameObject
from CoreInterface.SpawnInterface import SpawnInterface
from CoreInterface.GroupSpawnInterface import GroupSpawnInterface
from CoreInterface.SpaceEffectInterface import SpaceEffectInterface
import ObjectScript
import Const
import csconst
import random
import KST
import csdefine
import Functions
import KBEMath

class SpaceObject( GameObject, SpawnInterface, GroupSpawnInterface, SpaceEffectInterface ):
	def __init__( self ):
		KST.registerSpace(self.spaceID, self.scriptID, self.id, self.spaceKey)
		KBEngine.cellAppData[ Const.GET_SPACE_CELLAPP_KEY( self.spaceID ) ] = self.base
		KBEngine.cellAppData[ Const.GET_SPACE_CELLAPP_KEY_1( self.spaceID ) ] = self.id
		self.monsterSpawnIndexs = []	#保存刷新点配置中明怪的index 当所有明怪初始化完成后统一开启他们的AI
		self.monsterAIWaitStart = []	#等待开启AI的Monster id列表
		GameObject.__init__( self )
		SpawnInterface.__init__( self )
		GroupSpawnInterface.__init__( self )
		SpaceEffectInterface.__init__( self )
		self.getScript().initEntity( self )
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_SPACE )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_SPACE)

	def startMonsterAI(self):
		"""
		开启monsterAIWaitStart中的MonsterAI 
		"""
		for monsterID in self.monsterAIWaitStart:
			monster = KBEngine.entities.get(monsterID, None)
			if monster:
				#如果有FLAG_AI_TICK标志位 直接开启AI
				if monster.hasFlag(csdefine.FLAG_AI_TICK):
					monster.monsterAIStart()
				else:
					#自身在玩家的AOI范围内开启AI
					distance = self.getScript().getSpaceAoi()
					roles = monster.entitiesInRangeExtForAI(distance, csconst.AI_ENTITIES_IN_RANGE_HEIGHT, "Role" )
					if len(roles):
						monster.monsterAIStart()

		self.monsterAIWaitStart.clear()


	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		self.getScript().beforeDestroy( self )
		GameObject.beforeDestroy( self )
		
	
	def onDestroy( self ):
		"""
		"""
		self.destroySpace()		#调用引擎方法，以便销毁副本内entity
		GameObject.onDestroy( self )
		KST.deregisterSpace(self.spaceID)
		spaceBaseKey = Const.GET_SPACE_CELLAPP_KEY(self.spaceID)
		if spaceBaseKey in KBEngine.cellAppData:
			del KBEngine.cellAppData[spaceBaseKey]
	
	def getScript( self ):
		if not self._scriptObject:
			self._scriptObject = KST.g_objFactory.getSpaceObject( self.scriptID )
		return self._scriptObject
	
	def teleportEntity( self, roleBase, position, direction, packArgs ):
		"""
		<define method>
		传送一个entity
		"""
		if not self.hasRole( roleBase ) and not self.isAlreadyEnter( roleBase ):	#不是同地图传送
			self._readyEnterRoles.append( roleBase )
		self.getScript().teleportEntity( self, roleBase, Math.Vector3(position), direction, packArgs )
	
	def onEnter( self, playerRole, packArgs ):
		DEBUG_MSG("Player(%s) enter space(%s)! scriptID:%s."%( playerRole.id, self.id, self.scriptID ))
		self.registerRole( playerRole )
		for roleMB in self._readyEnterRoles:
			if roleMB.id == playerRole.id:
				self._readyEnterRoles.remove( roleMB )
		self.getScript().onEnter( self, playerRole, packArgs )
	
	def onTeleportCompleted( self, playerRole ):
		self.getScript().onTeleportCompleted( self, playerRole )
		playerRole.disableAssistJump = self.getScript().getDisableAssistJump()


	def onLeave( self,  playerRole, packArgs ):
		DEBUG_MSG("Player(%s) leave space(%s)! scriptID:%s."%( playerRole.id, self.id, self.scriptID ))
		self.deregisterRole( playerRole )
		self.getScript().onLeave( self, playerRole, packArgs )
	
	def onLogin( self, playerRole ):
		DEBUG_MSG("Player(%s) Login space(%s)! scriptID:%s."%( playerRole.id, self.id, self.scriptID ))
		self.registerRole( playerRole )
		self.getScript().onLogin( self, playerRole )
	
	def closeSpace( self ):
		"""
		<define method>
		关闭副本唯一入口，所有关闭副本操作（base或cell）都应该走此接口
		"""
		DEBUG_MSG("Close space(%s)! scriptID:%s."%( self.id, self.scriptID ))
		self.clearCellAppDataBeforeClose()
		
		if len( self._spaceRoles ):
			for roleCell in self._spaceRoles:
				roleCell.gotoExitSpacePos()
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			DEBUG_MSG("Delay close space(%s) reason 1! scriptID:%s."%( self.id, self.scriptID ))
		
		elif len( self._readyEnterRoles ):
			for roleBase in self._readyEnterRoles:
				roleBase.cell.gotoExitSpacePos()
			self._readyEnterRoles = []
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			DEBUG_MSG("Delay close space(%s) reason 2! scriptID:%s."%( self.id, self.scriptID ))
		
		else:
			self.destroySelf()
			
	def clearCellAppDataBeforeClose( self ):
		"""
		"""
		#地图开始关闭时，就需要移除，主要是防止在销毁的过程中海油其他玩家进来
		key = Const.GET_SPACE_CELLAPP_KEY_1( self.spaceID )
		if key in KBEngine.cellAppData:
			del KBEngine.cellAppData[key]
	
	def addEntityRecord( self, scriptID, entityID ):
		"""
		virtual method
		记录entity（所有继承于NPCBaseObject的entity）ID
		"""
		pass	# 目前只有副本会记录，基类里直接pass
	
	def delEntityRecord( self, scriptID, entityID ):
		"""
		virtual method
		删除entity记录
		"""
		pass

	def getEntityRecord( self, scriptID ):
		"""
		获取某scriptID的entity
		"""
		return []

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		pass

	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除entityMailBox 记录
		"""
		pass

	def getEntityMailBoxRecord( self, scriptID ):
		"""
		获取某scriptID的entity
		"""
		return []

	def setSpaceHPModifyRatio( self, spaceHPModifyRatio ):
		"""
		设置怪物生命修正倍率 JIRA CST-2172
		"""
		self.spaceHPModifyRatio = spaceHPModifyRatio
		self.onSpaceModifyRatioChange()

	def setSpaceDamageModifyRatio( self, spaceDamageModifyRatio ):
		"""
		设置怪物伤害修正倍率 JIRA CST-2172 
		"""
		self.spaceDamageModifyRatio = spaceDamageModifyRatio
		self.onSpaceModifyRatioChange()

	def onSpaceModifyRatioChange( self ):
		"""
		修正值改变时
		"""
		for entityIDList in self.entityRecord.values():
			for entityID in entityIDList:
				entity = KBEngine.entities.get(entityID,None)
				if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
					entity.calcAttachProperties()

	def onSpaceDataChange( self, spaceID, key, value ):
		"""
		当spaceData改变
		"""
		pass

	def getEntityDynamicPosBigMapShow( self, player, scriptID ):
		"""获取entity在大地图的位置"""
		return []

	def isAlreadyEnter( self, roleBase ):
		"""是否已在列表中"""
		for roleMB in self._readyEnterRoles:
			if roleMB.id == roleBase.id:
				return True
		return False

#---------------空间玩家数据管理------------------------------------
	def registerRole( self, roleMB ):
		"""
		记录空间玩家
		"""
		self._spaceRoles.append( roleMB )
	
	def deregisterRole( self, roleMB ):
		"""
		删除空间玩家
		"""
		for r in self._spaceRoles:
			if r.id == roleMB.id:
				self._spaceRoles.remove( r )
				break
	
	def hasRole( self, roleMB ):
		"""
		"""
		for r in self._spaceRoles:
			if r.id == roleMB.id:
				return True
		return False
	
	def getSpaceRoleNum( self ):
		return len( self._spaceRoles )

	def getSpaceRoles(self):
		return self._spaceRoles

#----------------------怪物死亡------------------------------
	def onMonsterDie( self, monsterID, monsterScriptID, group ):
		"""
		<define method>
		怪物死亡
		"""
		SpawnInterface.onMonsterDie( self, monsterScriptID, monsterID )
		if group > 0:
			GroupSpawnInterface.onGroupMonsterDie( self, group, monsterScriptID, monsterID )
		self.getScript().onMonsterDie( self, monsterID, monsterScriptID )

#--------------------场景物件触发---------------------------
	def onTriggerBox( self, boxID, boxScriptID ):
		"""
		<define method>
		箱子触发
		"""
		self.getScript().onTriggerBox( self, boxID, boxScriptID )

#----------------------NPCObject销毁------------------------------
	def onNPCObjectDestroy( self, enityID, entityScriptID, group ):
		"""
		<define method>
		NPCObject 销毁
		"""
		if group > 0:
			GroupSpawnInterface.onGroupNPCObjectDestroy( self, group, entityScriptID, enityID )
		self.getScript().onNPCObjectDestroy( self, enityID, entityScriptID )

#---------------------寻路相关--------------------------------------

	def setAreaFlags(self, areaFlags):
		"""
		"""
		self.areaFlags = areaFlags

	def getAreaFlags(self):
		"""
		"""
		return self.areaFlags

	def addAreaFlags(self, areaFlags):
		"""
		"""
		self.areaFlags |= areaFlags

	def removeAreaFlags(self, areaFlags):
		"""
		"""
		if areaFlags > self.areaFlags:
			return
		self.areaFlags &= ~areaFlags

#----------------------世界Boss刷新------------------------------
	def onSpaceInitLoadOver( self ):
		"""
		初始化完成
		"""
		KBEngine.globalData[ "RareMonsterMgr" ].onSpaceInitOver( self.base )

	def onCreateWorldBoss( self ):
		"""
		创建世界Boss
		"""
		bossScriptIDList, bossPositionList = self.getScript().getBossRefreshInfo()
		randomPosList = random.sample( bossPositionList, len(bossScriptIDList) )
		for i in range(len(bossScriptIDList)):
			posList = randomPosList[i].split(":")
			pos = Functions.vector3TypeConvert( posList[0] )
			dir = Functions.vector3TypeConvert( posList[1] )
			entity = self.createEntityByScriptID( bossScriptIDList[i], KBEMath.Unreal2KBEnginePosition( Math.Vector3(pos) ), KBEMath.Unreal2KBEngineDirection( Math.Vector3(dir) ), { "spawnPos": KBEMath.Unreal2KBEnginePosition( Math.Vector3(pos) ), "spawnDir": KBEMath.Unreal2KBEngineDirection( Math.Vector3(dir) )} )
			KBEngine.globalData[ "RareMonsterMgr" ].onStartRefreshNotice( entity.getUname(), self.getScript().getSpaceName(), self.scriptID )

	def onCountDpwnRefreshTime( self ):
		"""
		倒计时结束重新刷新
		"""
		self.addTimerCallBack( self.getScript().getCountDownTime(), "onCreateWorldBoss", () )
		
	
#------------------ 地图频道发言 -------------------------------------
	def onSendChatMessage( self, playerDBID, chatData ):
		"""
		"""
		for role in self._spaceRoles:
			if not role.cellHadBlacklist(playerDBID):
				role.onReceiveChatMessage( chatData )
				
	def globalWorld( self, messageType, messageArg ):
		"""
		消息广播
		"""
		self.base.globalWorld(messageType, messageArg)
		
			