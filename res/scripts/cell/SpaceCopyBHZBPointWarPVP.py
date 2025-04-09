# -*- coding: utf-8 -*-

from SpaceCopy import SpaceCopy
import csdefine
import time
import KBEDebug
import KBEngine
import csstatus
import csarithmetic
import csconst
import Functions
import KBEMath
from CoreInterface.SpaceBHZBWarDetailInterface import SpaceBHZBWarDetailInterface
import cschannel_msgs

class SpaceCopyBHZBPointWarPVP( SpaceCopy, SpaceBHZBWarDetailInterface ):
	"""
	帮会争霸 据点争夺战 PVP
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		SpaceBHZBWarDetailInterface.__init__( self )
		tongDBID = int( self.spaceKey.split("|")[1] )
		protectWarDetail = self.createArgs.get("protectWarDetailData",None)
		if protectWarDetail != None:
			self.warDetailMgr[tongDBID] = protectWarDetail
		# else:
		# 	self.addBHZBWarDetailData( tongDBID )
		declareTongDBID = self.createArgs.get("declareTongDBID",0)
		attackWarDetail = self.createArgs.get("attackWarDetailData",None)
		if attackWarDetail != None:
			self.warDetailMgr[declareTongDBID] = attackWarDetail
		# else:
		# 	self.addBHZBWarDetailData( declareTongDBID )
		self.isWin = False
		self.revivePosInfos = {}
		self.recordRoleReviveData = {}
		self.barrackInfo= {}							# 兵营据点等信息{ belongSide : { scriptID : pos},}
		self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_ATTACK] = {}
		self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_PROTECT] = {}
		self.isShowSettlementWnd = False
		self.recordRoleCalledArmy = {}	#记录玩家在此副本召唤的部队的索引 {dbid:armyIndex}

	def addWarMember( self, tongName,tongDBID,belongSide, id,mailBox, name,enemyTongName ):
		"""
		增加成员
		"""
		self.warMemberDatas.addMember( tongName,tongDBID,belongSide, id,mailBox, name,enemyTongName )

	def getRoleRecordCallArmy( self, dbid ):
		"""
		获取玩家召唤的部队记录
		"""
		return self.recordRoleCalledArmy.get( dbid, -1 )

	def updateRoleRecordCallArmy( self, dbid, armyIndex ):
		"""
		更新玩家召唤的部队记录
		"""
		self.recordRoleCalledArmy[dbid] = armyIndex
	
	def requestBHZBPointSpaceSaveInfoCB( self, spaceSaveInfos ):
		"""
		请求帮会争霸据点布防数据回调
		"""
		for spaceSaveInfo in spaceSaveInfos:
			self.createEntityByScriptID( spaceSaveInfo.scriptID, spaceSaveInfo.position, spaceSaveInfo.direction,{"belongSide":csdefine.BELONG_SIDE_PROTECT} )

	def onMonsterBeKill( self, killEntity, dieEntity, range ):
		"""
		玩家带领的小兵被击杀
		"""
		if dieEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: # 玩家带领的小怪被击杀
			dieControl = dieEntity.getControlEntity()
			if dieControl:
				self.warMemberDatas.addMemberSoldierDeadNum( dieControl.tongDBID,dieControl.playerDBID )
			if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
				cmder = killEntity.getControlEntity()
				if cmder:
					self.warMemberDatas.addMemberKillSoldierNum( cmder.tongDBID, cmder.playerDBID )
			elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE:
				self.warMemberDatas.addMemberKillSoldierNum( killEntity.tongDBID, killEntity.playerDBID )

	def onRoleBeKill( self, killEntity, dieEntity, range ):
		"""
		玩家被击杀
		"""
		self.warMemberDatas.addMemberDeadNum(dieEntity.tongDBID,dieEntity.playerDBID )
		if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE:
			self.warMemberDatas.addMemberKillEnemyNum( killEntity.tongDBID, killEntity.playerDBID )
			killEntity.addExp( self.getScript().getKillRoleAddExp(), csdefine.EXP_ADD_REASON_BHZB_POINT_WAR )
			contribution = self.getScript().getKillRoleAddContribution()
			if contribution > 0:
				killEntity.addContribution( contribution )
		elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT:
			cmder = killEntity.getControlEntity()
			if not cmder:
				return
			self.warMemberDatas.addMemberKillEnemyNum( cmder.tongDBID, cmder.playerDBID )
			cmder.addExp( self.getScript().getKillRoleAddExp(), csdefine.EXP_ADD_REASON_BHZB_POINT_WAR )
			contribution = self.getScript().getKillRoleAddContribution()
			if contribution > 0:
				cmder.addContribution( contribution )

	def setGCZIsWin( self, isWin ):
		"""
		设置攻城战是否胜利
		"""
		if self.isShowSettlementWnd:
			return
		self.isShowSettlementWnd = True
		self.isWin = isWin
		self.showGCZSettlementWnd()
		time = self.getScript().delyCloseTime - 1.0
		self.addTimerCallBack( time,"bhzbPointWarEnd",() )
		self.addTimerCallBack( self.getScript().delyCloseTime,"closeSpace",() )

	def showGCZSettlementWnd( self ):
		"""
		"""
		useTime = int(time.time() - self.lifeStartTime)
		members = self.warMemberDatas.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		for m in members:
			if m.roleMB and m.roleMB.getClient() and m.roleMB in self._spaceRoles:
				m.roleMB.client.CLIENT_ShowGCZSettlementWnd( self.isWin, useTime, self.getScript().delyCloseTime )
		protectMembers = self.warMemberDatas.getMembersBySide( csdefine.BELONG_SIDE_PROTECT )
		win = not self.isWin
		for m in protectMembers:
			if m.roleMB and m.roleMB.getClient() and m.roleMB in self._spaceRoles:
				m.roleMB.client.CLIENT_ShowGCZSettlementWnd( win, useTime, self.getScript().delyCloseTime )

	def bhzbPointWarEnd( self ):
		"""
		"""
		camp = self.createArgs.get("camp",0)
		pointIndex = self.createArgs.get("pointIndex",0)
		groupID = self.createArgs.get("declarePlayerDBID",0) #后一个版本修改为队伍编号
		if self.isWin:
			KBEngine.globalData["BHZBManager"].onBHZBPointWarSuccess( camp, pointIndex,groupID )
			KBEngine.globalData["BHZBManager"].occupyPointAddIntergral( camp, pointIndex, self.getScript().getRewardIntegral(),self.getScript().getRewardRepeatIntegral(),self.getScript().getRewardRepeatTime() )
		else:
			KBEngine.globalData["BHZBManager"].onBHZBPointWarFail( camp, pointIndex,groupID )
		self.statusEndMsg()

	def statusEndMsg( self ):
		"""
		"""
		attackMembers = self.warMemberDatas.getMembersBySide( csdefine.BELONG_SIDE_ATTACK )
		protectMembers = self.warMemberDatas.getMembersBySide( csdefine.BELONG_SIDE_PROTECT )
		for m in attackMembers:
			if m.roleMB:
				if self.isWin:
					m.roleMB.addExp(self.getScript().getAddRewardExp(), csdefine.EXP_ADD_REASON_BHZB_POINT_WAR)
					m.roleMB.statusMessage( csstatus.BHZB_ATTACK_PVEPOINT_SUCCESS, self.createArgs.get("declareTongName",""),self.createArgs.get("pointName","") )
				else:
					m.roleMB.statusMessage( csstatus.BHZB_ATTACK_PVEPOINT_FAIL, self.createArgs.get("pointName","") )
		for m in protectMembers:
			if m.roleMB:
				if self.isWin:
					m.roleMB.statusMessage( csstatus.BHZB_ATTACK_PVPPOINT_PROTECT_FAIL, self.createArgs.get("pointName","") )
				else:
					m.roleMB.statusMessage( csstatus.BHZB_ATTACK_PVPPOINT_PROTECT_SUCCESS, self.createArgs.get("belongTongName",""),self.createArgs.get("pointName","") )

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		SpaceCopy.addEntityMailBoxRecord( self, scriptID, entityMailBox )
		self.getScript().addEntityMailBoxRecord( self,scriptID, entityMailBox )
		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongAttackScriptIDs():
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
				entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_ATTACK )
				self.changeRviverPosition( entityMailBox.id, csdefine.TRAP_BARRACKS_BELONG_ATTACK,entityMailBox.position,csdefine.TRAP_BARRACKS_BELONG_ATTACK )
				self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_ATTACK].update( { str(entityMailBox.id) : KBEMath.KBEngine2UnrealPosition( entityMailBox.position) } )
			else:
				entityMailBox.setBelongSide( csdefine.BELONG_SIDE_ATTACK )
		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongProtectScriptIDs():
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
				entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_PROTECT )
				self.changeRviverPosition( entityMailBox.id, csdefine.TRAP_BARRACKS_BELONG_PROTECT,entityMailBox.position,csdefine.TRAP_BARRACKS_BELONG_PROTECT )
				self.barrackInfo[csdefine.TRAP_BARRACKS_BELONG_PROTECT].update( { str(entityMailBox.id) : KBEMath.KBEngine2UnrealPosition( entityMailBox.position )} )
			else:
				entityMailBox.setBelongSide( csdefine.BELONG_SIDE_PROTECT )
		if self.createArgs.get( "isEnterDefense",0 ) and entityMailBox.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			entityMailBox.addFlag(csdefine.FLAG_RELATION_NORMAL_TO_ROLE)
			entityMailBox.addFlag(csdefine.FLAG_RELATION_NORMAL_TO_MONSTER)

	def spawnGroupEntity( self, group, effectScriptID, delaySpawnTime ):
		"""
		刷新一批怪（刷了光效怪则先刷光效怪）
		@param effectScriptID:光效怪ID
		@param delaySpawnTime:光效怪刷出后延时多少秒刷配置的怪
		"""
		if not self.createArgs.get("isEnterDefense",0):
			SpaceCopy.spawnGroupEntity(self, group, effectScriptID, delaySpawnTime )

	def changeRviverPosition(self, entityID, belongType, position, oldBelongType):
		"""
		更改复活信息
		"""
		if oldBelongType in self.revivePosInfos:
			if entityID in self.revivePosInfos[oldBelongType]:
				self.revivePosInfos[oldBelongType].pop(entityID)
		
		if belongType not in self.revivePosInfos:
			self.revivePosInfos[belongType] = {}
		self.revivePosInfos[belongType][entityID] = position
		battackEntity = KBEngine.entities.get( entityID )
		if battackEntity and oldBelongType in self.barrackInfo and str(battackEntity.id) in self.barrackInfo[oldBelongType]:
			pos = self.barrackInfo[oldBelongType].pop( str(battackEntity.id) )
			self.barrackInfo[belongType] = { str(battackEntity.id) : pos } 
			for roleCell in self._spaceRoles:
				roleCell.client.occupyGTBarrack( belongType, str(battackEntity.id) )

	def getRevivePosition( self, role ):
		"""
		获取副本动态复活点
		"""
		belongSide = role.getBelongSide()
		revivePosInfos = list(self.revivePosInfos.get(belongSide, {}).values())
		if not len(revivePosInfos):
			revivePosInfos = self.getScript().getDefaultRevivePos(belongSide, role)
		
		minDist = 999999
		nearPosition = role.position
		for position in revivePosInfos:
			dist = position.flatDistTo( role.position )
			if minDist > dist: 
				nearPosition = position
				minDist = dist
		
		position = csarithmetic.getPositionByCircular( nearPosition, self.getScript().getReviveRadius() )
		return position,role.direction

	def addRecordRoleReviveNum( self, playerDBID ):
		"""
		增加记录玩家复活次数
		"""
		if playerDBID not in self.recordRoleReviveData:
			self.recordRoleReviveData[playerDBID] = (0,0) #（复活次数，下次复活时间）
		reviveNum, tempNextReviveTime = self.recordRoleReviveData[playerDBID]
		reviveNum = reviveNum + 1
		self.recordRoleReviveData[playerDBID] = (reviveNum, tempNextReviveTime)

	def updateRoleNextReviveTime( self, playerDBID ):
		"""
		更新玩家下次复活的时间
		"""
		if playerDBID not in self.recordRoleReviveData:
			self.recordRoleReviveData[playerDBID] = (0,0)
		reviveNum, tempNextReviveTime = self.recordRoleReviveData[playerDBID]
		tempNextReviveTime = reviveNum * self.getScript().getDieAddReviveTime() * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()
		self.recordRoleReviveData[playerDBID] = ( reviveNum,tempNextReviveTime )

	def getRecordRoleReviveData( self, playerDBID ):
		"""
		获得玩家复活数据次数
		"""
		if playerDBID in self.recordRoleReviveData:
			return self.recordRoleReviveData[playerDBID]

		return 0,0

	def statusMsgToMember( self, msgID, msgArgs ):
		"""
		"""
		for role in self._spaceRoles:
			if role.getClient():
				role.client.statusMessage( msgID, msgArgs )

	def statusMsgToTongMember( self, msgID, msgArgs, tongDBID ):
		"""
		"""
		for role in self._spaceRoles:
			if role.tongDBID == tongDBID and role.getClient():
				role.client.statusMessage( msgID, msgArgs )

	def delayTransferDataToClient( self, roleCell ):
		"""延迟传送时间，因为怪物还没创建好"""
		self.addTimerCallBack(2, "transferDataToClient", (roleCell,))
		
	def transferDataToClient( self, roleCell ):
		"""
		传输数据到客户端
		"""
		if not roleCell or not roleCell.client:return
		barrackDict = {}
		barrackDict["dictDatas"] = []
		for side, datas in self.barrackInfo.items():
			temp = {}
			temp["belongSide"] = side
			temp["datas"] = []
			for key, value in datas.items():
				_dict = {}
				_dict["key"] = key
				_dict["value"] = value
				temp["datas"].append( _dict )
			barrackDict["dictDatas"].append( temp )
		if roleCell.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
			roleCell.client.InitGTAttackDatas( barrackDict )
		else:
			batteryDict = {}
			batteryDict["dictDatas"] = []
			roleCell.client.InitGTProtectDatas( barrackDict, batteryDict, [], 0 )

	def isAllAttackSideOut( self ):
		"""
		是否所有进攻方的成员全部掉线副本
		"""
		hasNotAttackSideRole = True
		for role in self._spaceRoles:
			if role.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
				hasNotAttackSideRole = False
				break

		return hasNotAttackSideRole

	def onTeleportCompleted( self, playerRole ):
		SpaceCopy.onTeleportCompleted( self, playerRole )
		SpaceBHZBWarDetailInterface.onTeleportCompleted( self, playerRole )
