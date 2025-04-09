# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Define
import Functions
import csdefine
import time
import KBEngine
import Const
import KBEMath
import Math
import csstatus

class SpaceCopyFirstTongStarcraft7904( SpaceCopy ):
	"""
	帮会争霸 第一场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.reviveInfos = []
		self.initIntergal = 0
		self.doubleAddIntegralBuffs = []
		self.bossScriptIDList = []
		self.firstHurtBossIntegral = 0 # 第一个伤害Boss 获得的积分
		self.KillBossIntegral = 0 # 击杀Boss 获得的积分
		self.highHurtBossIntegral = 0 # 最高伤害boss 获得的积分
		self.secondHurtBossIntegral = 0 # 第二高伤害Boss 获得的积分
		self.otherHurtBossIntegral = 0 # 其他对boss 伤害 获得的积分

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.initIntergal = configData["SpaceData"].get("initIntergal",0)
		doubleAddIntegralBuffStr = configData["SpaceData"].get("doubleIntegralBuff","")
		if doubleAddIntegralBuffStr:
			self.doubleAddIntegralBuffs = [int(i) for i in doubleAddIntegralBuffStr.split("|")]

		self.bossScriptIDList = configData["SpaceData"].get("bossScriptIDs","").split("|")
		self.firstHurtBossIntegral = configData["SpaceData"].get("firstHurtBossIntegral",0)
		self.highHurtBossIntegral = configData["SpaceData"].get("highHurtBossIntegral",0)
		self.secondHurtBossIntegral = configData["SpaceData"].get("secondHurtBossIntegral",0)
		self.thirdHurtBossIntegral = configData["SpaceData"].get("thirdHurtBossIntegral",0)
		self.otherHurtBossIntegral = configData["SpaceData"].get("otherHurtBossIntegral",0)

		enterPosInfos = configData["SpaceData"].get("enterPosList","").split("|")
		enterDirInfos = configData["SpaceData"].get("enterDirList","").split("|")

		enterPosList = []
		enterDirList = []
		for enterPosInfo in enterPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( tuple(pos) )
			enterPosList.append(pos)

		for enterDirInfo in enterDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEnginePosition( tuple(dir) )
			enterDirList.append(dir)
		for i in range(0,len(enterPosList)):
			self.reviveInfos.append( (Math.Vector3(enterPosList[i]), Math.Vector3(enterDirList[i])) )

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.addTimerCallBackForScript(self.spaceLife,"onSpaceLifeEnd",())

	def getDoubleAddIntegralBuffs( self ):
		return self.doubleAddIntegralBuffs 

	def onSpaceLifeEnd( self, selfEntity ):
		"""
		副本时间到达
		"""
		firstTong = selfEntity.warInfos.getFirstTong()
		for member in selfEntity.warInfos.getMembers():
			member.mailbox.statusMessage( csstatus.TONG_STARCRAFT_SECOND_FIRST_TONG, firstTong.tongName )
		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_ThirdSignUp(selfEntity.camp,firstTong.tongDBID,firstTong.tongName )

	def setReviveType( self ):
		"""
		设置复活类型
		"""
		pass

	def getEnterInfo( self, selfEntity,tongDBID ):
		"""
		获得复活信息
		"""
		tongDBIDs = [int(i) for i in selfEntity.spaceKey.split("|")]
		if tongDBID in tongDBIDs:
			index = tongDBIDs.index(tongDBID)
			return self.reviveInfos[index]
		return None

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		selfEntity.warInfos.addMember( packArgs["tongDBID"], packArgs["tongName"],packArgs["playerDBID"],playerRole,self.initIntergal)

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		member = selfEntity.warInfos.getMember( playerRole.tongDBID, playerRole.playerDBID )
		if member:
			selfEntity.warInfos.addMember(  playerRole.tongDBID, selfEntity.warInfos[member.tongDBID].tongName,playerRole.playerDBID,playerRole,self.initIntergal)
		
	def onMonsterHPChanged( self, selfEntity, monsterEntity ):
		"""
		怪物血量改变
		"""
		SpaceCopy.onMonsterHPChanged( self, selfEntity, monsterEntity )
		if not monsterEntity.scriptID in self.bossScriptIDList:
			return
		if not selfEntity.isBossAlreadyFirstHurt():
			selfEntity.addRecordFirstHurtBossEntityID( monsterEntity.id )
			entityID = monsterEntity.getFirstDamageEntityID()
			entity = KBEngine.entities.get( entityID, None )
			if not entity:
				return
			selfEntity.addIntegral( entity,self.firstHurtBossIntegral )

	def onMonsterDie( self, selfEntity, monsterID, monsterScriptID ):
		"""
		怪物死亡
		"""
		SpaceCopy.onMonsterDie( self, selfEntity, monsterID, monsterScriptID )
		if not monsterEntity.scriptID in self.bossScriptIDList:
			return
		damageDict = selfEntity.getBossDamageList( monsterID )
		if len(damageDict) == 0:
			return
		entityIDs = sorted( damageDict, key = lambda x:damageDict[x], reverse = True )
		for entityID in entityIDs:
			rewardIntegral = 0
			if entityIDs.index( entityID ) == 0:
				rewardIntegral = self.highHurtBossIntegral
			elif entityIDs.index( entityID ) == 1:
				rewardIntegral = self.secondHurtBossIntegral
			elif entityIDs.index(entityID) == 2:
				rewardIntegral = self.thirdHurtBossIntegral
			else:
				rewardIntegral = self.otherHurtBossIntegral
			entity = KBEngine.entities.get( entityID,None )
			if entity:
				selfEntity.addIntegral( entity, rewardIntegral )
