# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import KBEMath
import csdefine
import csstatus
from SpaceCopy import SpaceCopy
import csarithmetic
import ItemFactory
import time

class SpaceCopyTongPlunder( SpaceCopy ):
	"""
	CST-11602 帮会掠夺
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.revivePosInfos = {}
		self.belongSide2roleDBID = {}
		self.recordRoleReviveData = {}
		self.getVoucherRecord = [] #玩家获得兑换券的记录
		self.barracksIDList = [] #兵营entityID列表
		self.winnerTongBelongSide = -1
		self.rewardItems = []
		self.boxRecordPlayerDatas = {} #playerDBID: boxEntitiy.id，已打开过宝箱的玩家dbid列表，活动设定一个玩家只能打开一个宝箱
		self.recordRoleCalledArmy = {}	#记录玩家在此副本召唤的部队的索引 {dbid:armyIndex}
	
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

	def setBothSidesInfo(self, tongInfo):
		"""
		define method
		设置攻守双方帮会DBID
		"""
		self.getScript().setBothSidesInfo(tongInfo)
		self.plunderMemberDatas.setBothName(self.getScript().attackTongName, self.getScript().protectTongName)

	def getBothSidesDBID(self):
		return self.getScript().getBothSidesDBID()
		
	def getWinnerTongLevel(self):
		"""
		获取胜利帮会等级
		"""
		attackTongLevel, protectTongLevel = self.getScript().getBothSidesLevel()
		if self.winnerTongBelongSide == csdefine.BELONG_SIDE_ATTACK:
			return attackTongLevel
		elif self.winnerTongBelongSide == csdefine.BELONG_SIDE_PROTECT:
			return protectTongLevel

	def getLoserTongLevel(self):
		"""
		获取失败帮会等级
		"""
		attackTongLevel, protectTongLevel = self.getScript().getBothSidesLevel()
		if self.winnerTongBelongSide == csdefine.BELONG_SIDE_ATTACK:
			return protectTongLevel
		elif self.winnerTongBelongSide == csdefine.BELONG_SIDE_PROTECT:
			return attackTongLevel

	def getWinnerTongDBID(self):
		"""
		获取失败帮会等级
		"""
		attackTongDBID, protectTongDBID = self.getScript().getBothSidesDBID()
		if self.winnerTongBelongSide == csdefine.BELONG_SIDE_ATTACK:
			return attackTongDBID
		elif self.winnerTongBelongSide == csdefine.BELONG_SIDE_PROTECT:
			return protectTongDBID

		return 0
		
	def addVoucherRecord(self, playerDBID):
		"""
		"""
		self.getVoucherRecord.append(playerDBID)

	def onTongPlunderVictory(self, rewardData):
		"""
		某个帮会获胜
		"""
		for data in rewardData:
			itemID = data.itemID
			amount = data.amount
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount, {})
			self.rewardItems.append(itemInst)

		self.createPlunderBox()

	def createPlunderBox(self):
		"""
		创建掠夺战副本中的宝箱
		"""
		for scriptID in self.getScript().getPlunderBoxScriptID():
			self.spawnPointCreateEntityByScriptID(scriptID)

	def getRewardItems(self):
		"""
		"""
		return self.rewardItems

	def setBelongTypeWin( self, belongType ):
		"""
		设置一方胜利
		"""
		self.winnerTongBelongSide = belongType
		
		if self.winnerTongBelongSide == -1:
			return
		
		memberData = self.plunderMemberDatas.getClientData(self.plunderMemberDatas)
		useTime = int(time.time() - self.lifeStartTime)
		delayCloseTime = self.getScript().getDelayCloseTime()
		"""
		for m in self.plunderMemberDatas.getMembers():
			if m.roleMB:
				belongSideType = m.roleMB.getBelongSide()
				m.roleMB.destroyArms() #收起士兵
				if m.roleMB.getClient():
					if belongSideType == self.winnerTongBelongSide:
						m.roleMB.client.CLIENT_ShowTongPlunderSettlementWnd(1, useTime, int(delayCloseTime), memberData)
					else:
						m.roleMB.client.CLIENT_ShowTongPlunderSettlementWnd(0, useTime, int(delayCloseTime), memberData)
				#所有人设置问进攻方，不能互相攻击		
				#m.roleMB.setBelongSide(csdefine.TRAP_BARRACKS_BELONG_ATTACK) 
				m.roleMB.setSpaceRelationRule(csdefine.TRAP_BARRACKS_BELONG_ATTACK)
		"""

		for role in self._spaceRoles:
			belongSideType = role.getBelongSide()
			role.destroyArms() #收起士兵
			if role.getClient():
				if belongSideType == self.winnerTongBelongSide:
					role.client.CLIENT_ShowTongPlunderSettlementWnd(1, useTime, int(delayCloseTime), memberData)
				else:
					role.client.CLIENT_ShowTongPlunderSettlementWnd(0, useTime, int(delayCloseTime), memberData)

			#所有人设置问进攻方，不能互相攻击
			role.setSpaceRelationRule(csdefine.TRAP_BARRACKS_BELONG_ATTACK)
			
		attackTongDBID, protectTongDBID = self.getScript().getBothSidesDBID()
		KBEngine.globalData["TongPlunderManager"].onActivityGetTheResult(attackTongDBID, protectTongDBID)
		
		self.getScript().stopSpaceLife(self)

		self.addTimerCallBack(delayCloseTime, "closeSpace", ())

	def getWinnerTongBelongSide(self):
		"""
		获取胜利方所属类型
		"""
		return self.winnerTongBelongSide

	def getWinnerType(self):
		"""
		活动开启一段时间后，会检查攻守双方是否有人在场，然后判断胜负情况
		"""
		if self.winnerTongBelongSide != -1:
			return self.winnerTongBelongSide

		winnerTongBelongSide = -1
		if len(self.belongSide2roleDBID) == 0: #没有成员，默认是防守方胜利
			winnerTongBelongSide = csdefine.BELONG_SIDE_PROTECT
		else: #只有一方人员进入活动场地，进入一方获胜
			if csdefine.BELONG_SIDE_PROTECT in self.belongSide2roleDBID and len(self.belongSide2roleDBID[csdefine.BELONG_SIDE_PROTECT]) > 0:
				if csdefine.BELONG_SIDE_ATTACK not in self.belongSide2roleDBID or len(self.belongSide2roleDBID[csdefine.BELONG_SIDE_ATTACK]) <= 0:
					winnerTongBelongSide = csdefine.BELONG_SIDE_PROTECT
			elif csdefine.BELONG_SIDE_ATTACK in self.belongSide2roleDBID and len(self.belongSide2roleDBID[csdefine.BELONG_SIDE_ATTACK]) > 0:
				if csdefine.BELONG_SIDE_PROTECT not in self.belongSide2roleDBID or len(self.belongSide2roleDBID[csdefine.BELONG_SIDE_PROTECT]) <= 0:
					winnerTongBelongSide = csdefine.BELONG_SIDE_ATTACK

		self.setBelongTypeWin(winnerTongBelongSide)
		
		return self.winnerTongBelongSide

	def activeIsEnd(self):
		"""
		活动是否已结束
		"""
		return self.winnerTongBelongSide != -1

	def addOpenBoxRecord(self, playerDBID, boxEntitiyID):
		"""
		添加玩家开宝箱记录
		"""
		self.boxRecordPlayerDatas[playerDBID] = boxEntitiyID

	def getOpenBoxEntityID(self, playerDBID):
		"""
		"""
		if playerDBID in self.boxRecordPlayerDatas:
			return self.boxRecordPlayerDatas[playerDBID]
		return -1
		
	def recordRoleBelongSide(self, belongSide, playerDBID):
		"""
		记录玩家进入地图后的攻守方
		"""
		if belongSide not in self.belongSide2roleDBID:
			self.belongSide2roleDBID[belongSide] = []
		if playerDBID not in self.belongSide2roleDBID[belongSide]:
			self.belongSide2roleDBID[belongSide].append(playerDBID)
			
	def onRoleLeaveSpace(self, player):
		"""
		玩家离开地图后，移除激励
		"""
		belongSide = player.getBelongSide()
		playerDBID = player.playerDBID
		if belongSide in self.belongSide2roleDBID and playerDBID in self.belongSide2roleDBID[belongSide]:
			self.belongSide2roleDBID[belongSide].remove(playerDBID)
		if belongSide in self.belongSide2roleDBID and len(self.belongSide2roleDBID[belongSide]) == 0:
			self.belongSide2roleDBID.pop(belongSide)
		
	def recordOpterationMachine(self, id):
		"""记录被操作的器械"""
		self.machineWarList.append(id)
		
	def removeOpterationMachine(self, id):
		"""移除被操作的器械"""
		if id in self.machineWarList:
			self.machineWarList.remove(id)
			
	def addEntityMailBoxRecord(self, scriptID, entityMailBox):
		"""
		增加entityMailBox 记录
		"""
		SpaceCopy.addEntityMailBoxRecord( self, scriptID, entityMailBox )

		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongAttackScriptIDs():
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BATTLEFLAG or entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
				entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_ATTACK )
			entityMailBox.setBelongSide(csdefine.BELONG_SIDE_ATTACK)

		if entityMailBox.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE and entityMailBox.scriptID in self.getScript().getBelongProtectScriptIDs():
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BATTLEFLAG:
				entityMailBox.setBarracksBelongType( csdefine.TRAP_BARRACKS_BELONG_PROTECT )
			
			if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
				entityMailBox.setBarracksBelongType(csdefine.TRAP_BARRACKS_BELONG_PROTECT)
				
			entityMailBox.setBelongSide(csdefine.BELONG_SIDE_PROTECT)

		if entityMailBox.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_TRAP_BARRACKS:
			self.barracksIDList.append(entityMailBox.id)

			belongSide = entityMailBox.getBarracksBelongType()
			if belongSide not in self.revivePosInfos:
				self.revivePosInfos[belongSide] = {}
			self.revivePosInfos[belongSide][entityMailBox.id] = entityMailBox.position
		
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

		#战旗归属变化，通知客户端
		battackEntity = KBEngine.entities.get(entityID)
		if battackEntity and oldBelongType != belongType:
			for roleCell in self._spaceRoles:
				roleCell.client.occupyGTBarrack(belongType, str(battackEntity.id))
		
	def getRevivePosition(self, role):
		"""
		获取副本动态复活点
		"""
		belongSide = role.getBelongSide()
		revivePosInfos = []

		for id, position in self.revivePosInfos.get(belongSide, {}).items():
			entity = KBEngine.entities.get(id, None)
			if entity and hasattr(entity, "checkCanRevivePlayer") and entity.checkCanRevivePlayer(role):
				revivePosInfos.append(position)

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
		return position
		
	def addRecordRoleReviveNum(self, playerDBID):
		"""
		增加记录玩家复活次数
		"""
		if playerDBID not in self.recordRoleReviveData:
			self.recordRoleReviveData[playerDBID] = 0 #复活次数
		reviveNum = self.recordRoleReviveData[playerDBID]
		self.recordRoleReviveData[playerDBID] = reviveNum + 1
		
	def getRecordRoleReviveData( self, playerDBID ):
		"""
		获得玩家复活数据次数
		"""
		#reviveNum：已经复活次数，remainReviveNum：剩余复活次数，reviveTime：下次复活等待时间
		reviveNum = 0
		reviveTime = self.getScript().getReviveTime()
		if playerDBID in self.recordRoleReviveData:
			reviveNum = self.recordRoleReviveData[playerDBID]

		maxReviveNum = self.getScript().getMaxReviveNum()

		remainReviveNum = maxReviveNum - reviveNum - 1
		if remainReviveNum == 0:
			reviveTime = 0.0

		return (remainReviveNum, reviveTime)
				
	def gotoLeavelTongSpace(self, player):
		"""
		"""
		scriptID, position, direction = self.getScript().getLeaveTongSpaceInfo()
		player.gotoSpace(scriptID, position, direction)

	def leaveTongOnActivity(self, player):
		"""
		活动期间离开帮会
		"""
		self.addTimerCallBack(10.0, "gotoLeavelTongSpace", (player, ))

	def addPlunderMember(self, id, mailBox, name, belongSide):
		"""
		添加掠夺战参战人员信息
		"""
		self.plunderMemberDatas.addMember(id, mailBox, name, belongSide)

	def onMonsterBeKill(self, killEntity, dieEntity, range):
		"""
		Monster被击杀
		"""
		if dieEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: #玩家带领的士兵被击杀
			if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE: # 玩家击杀
				self.plunderMemberDatas.addMemberKillSoldierNum(killEntity.playerDBID)

			elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: #玩家带领的小兵击杀
				id = self.plunderMemberDatas.getIDByEntityID(killEntity.controlEntityID)
				self.plunderMemberDatas.addMemberKillSoldierNum(id)

			id = self.plunderMemberDatas.getIDByEntityID(dieEntity.controlEntityID)
			self.plunderMemberDatas.addMemberSoldierDeadNum(id)

			self.plunderMemberDatas.onSoldierDead(dieEntity.getBelongSide())


	def onRoleBeKill(self, killEntity, dieEntity, range):
		"""
		玩家被击杀
		"""
		self.plunderMemberDatas.addMemberDeadNum(dieEntity.playerDBID)

		if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_ROLE: #玩家击杀
			self.plunderMemberDatas.addMemberKillEnemyNum(killEntity.playerDBID)
		elif killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT: #玩家带领的小兵击杀
			id = self.plunderMemberDatas.getIDByEntityID(killEntity.controlEntityID)
			self.plunderMemberDatas.addMemberKillEnemyNum(id)

	def delayTransferDataToClient(self, roleCell):
		"""
		延迟传送时间，因为怪物还没创建好
		"""
		self.addTimerCallBack(2, "transferDataToClient", (roleCell,))

	def transferDataToClient(self, roleCell):
		"""
		传输数据到客户端
		"""
		if not roleCell or not roleCell.client:
			return

		barrackDict = {}
		barrackDict["dictDatas"] = []
		for side, datas in self.revivePosInfos.items():
			temp = {}
			temp["belongSide"] = side
			temp["datas"] = []
			for key, value in datas.items():
				_dict = {}
				_dict["key"] = str(key)
				_dict["value"] = KBEMath.KBEngine2UnrealPosition(value)
				temp["datas"].append(_dict)
			barrackDict["dictDatas"].append(temp)

		if roleCell.isBelongSide(csdefine.BELONG_SIDE_ATTACK):
			roleCell.client.InitGTAttackDatas(barrackDict)
		else:
			batteryDict = {}
			batteryDict["dictDatas"] = []
			roleCell.client.InitGTProtectDatas(barrackDict, batteryDict, [], 0)
