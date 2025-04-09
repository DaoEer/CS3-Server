# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import json
import Functions
import KBEMath
import Math
from ArmyInfo import ArmyInfo
from ConfigObject.Barracks.BarracksMgr import g_barracksMgr
import csdefine
import time
import Const
import csstatus
import csconst
import KBEDebug

class SpaceCopyAttackCityWar( SpaceCopy ):
	"""
	攻城战 CST-8954
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.aerialLadderPos = {}
		self.aerialLadderDir = {}
		self.aerialLadderUpPos = {}
		self.roleDefaultArmyDatas = []
		self.reviveBossScriptID = []
		self.notReviveBossScriptID = []
		self.belongAttackScriptIDs = []
		self.belongProtectScriptIDs = []
		self.protectName = ""
		self.delyCloseTime = 0
		self.bossReviveTime = 0.0
		self.reviveRadius = 0.0
		self.reviveAddBuffIDs = []
		self.commonMonsterScriptIDs = []
		self.qixieScriptIDs = []
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		if configData["SpaceData"].get("aerialLadderPos",""):
			aerialLadderPosInfos = configData["SpaceData"].get("aerialLadderPos","").split("|")
			for index in range(len(aerialLadderPosInfos)):
				pos = Functions.vector3TypeConvert(aerialLadderPosInfos[index])
				pos = KBEMath.Unreal2KBEnginePosition( pos )
				self.aerialLadderPos[index] = pos

		if configData["SpaceData"].get( "aerialLadderUpPos","" ):
			aerialLadderUpPosInfos = configData["SpaceData"].get("aerialLadderUpPos","").split("|")
			for index in range( len(aerialLadderUpPosInfos) ):
				pos = Functions.vector3TypeConvert(aerialLadderUpPosInfos[index])
				pos = KBEMath.Unreal2KBEnginePosition( pos )
				self.aerialLadderUpPos[index] = pos

		if configData["SpaceData"].get( "aerialLadderDir","" ):
			aerialLadderDirInfos = configData["SpaceData"].get("aerialLadderDir","").split("|")
			for index in range( len( aerialLadderDirInfos ) ):
				dir = Functions.vector3TypeConvert(aerialLadderDirInfos[index])
				dir = KBEMath.Unreal2KBEngineDirection( dir )
				self.aerialLadderDir[index] = dir

		if configData["SpaceData"].get("defaultArmyData",""):
			self.roleDefaultArmyDatas = configData["SpaceData"].get("defaultArmyData","").split("|")

		self.reviveBossScriptID = configData["SpaceData"].get("reviveBossScriptID","").split("|")
		self.notReviveBossScriptID = configData["SpaceData"].get("notReviveBossScriptID","").split("|")

		self.belongAttackScriptIDs = configData["SpaceData"].get( "belongAttackScriptIDs","" ).split("|")
		belongProtectScriptIDStrs = configData["SpaceData"].get( "belongProtectScriptIDs",[] )
		for belongProtectScriptIDStr in belongProtectScriptIDStrs:
			self.belongProtectScriptIDs.extend( belongProtectScriptIDStr.split("|") )

		self.protectName = configData["SpaceData"].get( "protectName","" )
		self.delyCloseTime = configData["SpaceData"].get( "delyCloseTime",0 )
		self.bossReviveTime = configData["SpaceData"].get( "bossReviveTime",0.0 )
		self.reviveRadius = configData["SpaceData"].get( "reviveRadius", 0.0 )
		self.reviveAddBuffIDs = configData["SpaceData"].get( "reviveAddBuffIDs",[] )

		commonMonsterScriptIDStrs = configData["SpaceData"].get("commonMonsterScriptIDs",[])
		for commonMonsterScriptIDStr in commonMonsterScriptIDStrs:
			self.commonMonsterScriptIDs.extend( commonMonsterScriptIDStr.split("|") )			

		self.qixieScriptIDs = configData["SpaceData"].get("qixieScriptIDs","").split("|")

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )

	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass

	def getAerialLadderPosInfo( self ):
		"""
		"""
		return self.aerialLadderPos

	def getAerialLadderDirInfo( self, index ):
		"""
		"""
		if index in self.aerialLadderDir:
			return self.aerialLadderDir[index]
		return None

	def getBossReviveTime( self ):
		"""
		"""
		return self.bossReviveTime

	def getAerialLadderUpPosInfo( self ):
		return self.aerialLadderUpPos

	def getBelongAttackScriptIDs( self ):
		return self.belongAttackScriptIDs

	def getBelongProtectScriptIDs( self ):
		return self.belongProtectScriptIDs

	def getReviveBossScriptID( self ):
		return self.reviveBossScriptID

	def getNotReviveBossScriptID( self ):
		return self.notReviveBossScriptID

	def getReviveRadius( self ):
		return self.reviveRadius

	def getCommonMonsterScriptIDs( self ):
		return self.commonMonsterScriptIDs

	def getQiXieScriptIDs( self ):
		return self.qixieScriptIDs

	def getReviveAddBuffIDByReviveNum( self, reviveNum ):
		"""
		获得复活增加的Buff
		"""
		if reviveNum < len( self.reviveAddBuffIDs ):
			return self.reviveAddBuffIDs[reviveNum]
		return 0

	def addEntityMailBoxRecord( self, selfEntity,scriptID, entityMailBox ):
		"""
		策划要求
		会复活的大概有5个ID
		每个ID 单独计算，击杀
		不会复活的大概有6-8个ID
		所有ID，击杀数合计在一起
		那到时候就取不会复活序列 的 第一个ID名称就可以了。
		"""
		# if scriptID in self.reviveBossScriptID:
		# 	selfEntity.addGCZMember( entityMailBox.id, entityMailBox, entityMailBox.getUname(),csdefine.BELONG_SIDE_PROTECT,self.protectName,"" )
		# elif scriptID in self.notReviveBossScriptID:
		# 	name = ""
		# 	if self.notReviveBossScriptID.index( scriptID ) == 0:
		# 		name = entityMailBox.getUname()
		# 	selfEntity.addGCZMember( 0, entityMailBox, name, csdefine.BELONG_SIDE_PROTECT, self.protectName,"" )
		# CST-11481 没有能复活的boss 类型
		if scriptID in self.notReviveBossScriptID:
			member = selfEntity.GCZMemberDatas.getMemberByName( entityMailBox.getUname() )
			if member == None:
				selfEntity.addGCZMember( entityMailBox.id, entityMailBox, entityMailBox.getUname(), csdefine.BELONG_SIDE_PROTECT, self.protectName,"" )

		if scriptID in self.commonMonsterScriptIDs:
			if self.commonMonsterScriptIDs.index(scriptID) == 0:
				selfEntity.addGCZMember( 0, entityMailBox, entityMailBox.getUname(), csdefine.BELONG_SIDE_PROTECT, self.protectName,"" )
	
	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		playerRole.onEnterAttackCityWar()
		attackName = ""
		if playerRole.isTeamCaptain():
			attackName = playerRole.getName()
		selfEntity.addGCZMember( playerRole.playerDBID,playerRole,playerRole.getName(), csdefine.BELONG_SIDE_ATTACK, self.protectName, attackName)
		if len(playerRole.getRoleArmyDatas()) > 0: #如果玩家有部队数据就不需要默认部队数据
			return
		if playerRole.playerDBID not in selfEntity.roleDefaultArmyDatas:
			selfEntity.roleDefaultArmyDatas[playerRole.playerDBID] = []
		for roleDefaultArmyData in self.roleDefaultArmyDatas:
			roleDefaultArmyInfos = roleDefaultArmyData.split(" ")
			armyInst = ArmyInfo()
			armyInst.id = self.roleDefaultArmyDatas.index(roleDefaultArmyData)
			armyInst.firstGuardScriptID = roleDefaultArmyInfos[0]
			armyInst.secondGuardScriptID = roleDefaultArmyInfos[1]
			soldierInfos = roleDefaultArmyInfos[2].split(":")
			armyInst.soldierScriptID = soldierInfos[0]
			barracksItem = g_barracksMgr.getBarracksItemByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, armyInst.soldierScriptID )
			if not barracksItem:
				return
			for index in range( int(soldierInfos[1] )):
				id = barracksItem.getMaxHaveAmount() + 1 + index
				armyInst.soldierIDs.append(id)
			selfEntity.roleDefaultArmyDatas[playerRole.playerDBID].append(armyInst)

	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onTeleportCompleted( self, selfEntity, playerRole )
		
		#召唤部队
		if len(playerRole.getRoleArmyDatas()) > 0:
			armyIndex = selfEntity.getRoleRecordCallArmy( playerRole.playerDBID )
			if armyIndex == -1:		#等于-1说明玩家之前没有进过副本或没有部队
				armyIndex = playerRole.getDefaultArmyIndex()
			if armyIndex != -1:
				playerRole.callIDArmyToWar( armyIndex )

	def onPlayerCallArmy( self, selfEntity, playerID, playerDBID, armyIndex ):
		"""
		玩家点击了出战
		"""
		selfEntity.updateRoleRecordCallArmy( playerDBID, armyIndex )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		playerRole.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		selfEntity.addGCZMember( playerRole.playerDBID,playerRole,playerRole.getName(), csdefine.BELONG_SIDE_ATTACK, self.protectName, "")

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( (spaceLifeSecond + self.delyCloseTime), "closeSpace", () )
		selfEntity.addTimerCallBack( spaceLifeSecond, "showGCZSettlementWnd", () )
		totalTime = spaceLifeSecond + self.delyCloseTime
		if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalTime - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		else:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalTime - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))

	def changeSpaceLife( self, selfEntity, dynamicTime ):
		"""
		改变计时
		"""
		selfEntity.popTimer( selfEntity.lifeTimer )
		selfEntity.lifeTimer = 0
		selfEntity.popTimer( selfEntity.lifeNotifyTimer )
		selfEntity.lifeNotifyTimer = 0
		
		selfEntity.dynamicTime += dynamicTime
		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) - selfEntity.lifeTotalStopTime + selfEntity.dynamicTime
		if remainTime >= 0:
			selfEntity.lifeTimer = selfEntity.addTimerCallBack( (remainTime + self.delyCloseTime), "closeSpace", () )
			selfEntity.addTimerCallBack( remainTime, "showGCZSettlementWnd", () )
			totalRemainTime = remainTime + self.delyCloseTime
			if totalRemainTime - Const.SPACE_LIFE_NOTIFY_TIME >= 0:
				if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
					selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalRemainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
				else:
					selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalRemainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
			for e in selfEntity._spaceRoles:
				e.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ) )
		else:
			selfEntity.closeSpace()

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		playerRole.setCallArmyIndex( -1 )
		indexs = list(playerRole.getAttrBuffs().keys())
		for index in indexs:
			playerRole.removeBuff(index)
		if playerRole.getClient():
			playerRole.client.CLIENT_OnLeaveGCZ()
