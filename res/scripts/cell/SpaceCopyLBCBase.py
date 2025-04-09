# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import KBEngine
import csstatus
from ConfigObject import PatrolRouteLoader
import Math
import cschannel_msgs
import KBEMath
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr

class SpaceCopyLBCBase( SpaceCopy ):
	"""
	高级练兵场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.number = 0
		self.soldiersDict = {}
		self.soldierIDList = []
		self.randomEventScriptIDDict = {}
		self.xianShowEnemyPosTimer = 0
		self.xianHideEnemyPosTimer = 0
		self.moShowEnemyPosTimer = 0
		self.moHideEnemyPosTimer = 0
		self.xianAddJadeTimer = 0
		self.moAddJadeTimer = 0
		self.xianAlreadyShowTime = 0.0 # 仙道已经显示敌方位置的时间
		self.moAlreadyShowTime = 0.0 # 魔道已经显示敌方位置的时间
		self.playerBelongSide = {} #存玩家的belongSide {dbid:belongSide}


	def addPlayerBelongSide(self, dbid, belongSide):
		"""
		"""
		self.playerBelongSide[dbid] = belongSide

	def getPlayerBelongSide(self, dbid):
		"""
		"""
		if dbid in self.playerBelongSide:
			return self.playerBelongSide[dbid]
		return 0


	def addYXLMMemberData( self, roleMB ):
		"""
		增加成员数据
		"""
		self.memberDatas.add( roleMB )

	def removeYXLMMemberData( self, roleMB ):
		"""
		减少成员数据
		"""
		self.memberDatas.remove(roleMB)

	def onMemberAddItem( self, roleMB, itemInstID ):
		"""
		成员增加物品
		"""
		self.memberDatas.onAddItem( roleMB, itemInstID )

	def onMemberRemoveItem( self, roleMB, itemInstID ):
		"""
		成员删除物品
		"""
		self.memberDatas.onRemoveItem( roleMB, itemInstID )

	def createMonsterByShop( self, player, scriptID, index, param ):
		"""
		商店购买小兵
		index 表示第几条路线
		"""
		self.getScript().createMonsterByShop( self, player, scriptID, index, param )

	def updateGradeBuilding( self, oldscriptid, newscriptid, wayType):
		"""
		升级塔
		"""
		idList = self.getEntityRecord( oldscriptid )
		if len(idList) <= 0:
			return
		for id in idList:
			entity = KBEngine.entities.get(id,None)
			if entity and entity.wayType == wayType:
				self.createEntityByScriptID( newscriptid, entity.position, entity.direction,{"spawnPos":entity.position,"spawnDir":entity.direction,"wayType":wayType} )

				entity.delayDestroy(1.0)
				wayStr = cschannel_msgs.YXLM_TOWER_NAME.get(wayType,"")
				belongSide = entity.getBelongSide()
				enemyBelongSide = csdefine.BELONG_SIDE_ATTACK \
					if belongSide == csdefine.BELONG_SIDE_PROTECT \
						else csdefine.BELONG_SIDE_PROTECT

				memberList = self.memberDatas.getMembersByCamp( belongSide )
				for member in memberList:
					member.roleMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_BUILIDING_UPGRADE,wayStr )

				enemyMemberList = self.memberDatas.getMembersByCamp( enemyBelongSide )
				for enemyMember in enemyMemberList:
					enemyMember.roleMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_ENEMY_BUILIDING_UPGRADE,wayStr )

	def getXianDestroyBuildingData( self, wayType ):
		"""
		获得仙道销毁的塔
		"""
		if wayType in self.xianDestroyBuildingData:
			return self.xianDestroyBuildingData[wayType]
		return []

	def getMoDestrooyBuildingData( self, wayType ):
		"""
		获得魔道销毁的塔
		"""
		if wayType in self.moDestroyBuildingData:
			return self.moDestroyBuildingData[wayType]
		return []

	def brushSoldiers( self, wayDataList, dir, soldierWay ):
		"""
		刷小兵
		"""
		if not len(wayDataList):
			return
		self.number += 1
		delayTime = 0.0
		for wayData in wayDataList:
			data = wayData.split(":")
			scriptID = data[0]
			route = int(data[1])
			if scriptID not in self.soldierIDList:
				self.soldierIDList.append(scriptID)
			routeInfo = PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( self.scriptID, route )
			if len(routeInfo):
				delayTime += 1.5
				position = Math.Vector3(routeInfo[1]["position"])
				#self.createEntityByScriptID(scriptID,position, dir,{"patrolList":route,"number":self.number,"position":position,"way":soldierWay})
				self.addTimerCallBack(delayTime,"createEntityByScriptID",(scriptID,position, dir,{"patrolList":route,"number":self.number,"position":position,"way":soldierWay}))

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加 soldiersDict 记录
		"""
		SpaceCopy.addEntityMailBoxRecord( self, scriptID, entityMailBox )
		if scriptID in self.soldierIDList:
			way = entityMailBox.way
			number = entityMailBox.number
			if way not in self.soldiersDict:
				self.soldiersDict[way] = {}
			if number not in self.soldiersDict[way]:
				self.soldiersDict[way][number] = []
			self.soldiersDict[way][number].append(entityMailBox)
		
		if scriptID in self.getScript().showScriptID:
			if entityMailBox.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
				if self.xianShowEnemyPosTimer:
					self.popTimer(self.xianShowEnemyPosTimer)
					self.xianShowEnemyPosTimer = 0
				if self.xianHideEnemyPosTimer:
					self.popTimer( self.xianHideEnemyPosTimer )
					self.xianHideEnemyPosTimer = 0
				hideTime = (len(self.getEntityMailBoxRecord( scriptID )) * self.getScript().showTime) - self.xianAlreadyShowTime
				self.xianShowEnemyPosTimer = self.addTimerRepeat( 1.0, "showEnemyPos",(csdefine.BELONG_SIDE_ATTACK, csdefine.BELONG_SIDE_PROTECT) )
				self.xianHideEnemyPosTimer = self.addTimerCallBack( hideTime,"HideEnemyPos",( csdefine.BELONG_SIDE_ATTACK,) )
			elif entityMailBox.getBelongSide() == csdefine.BELONG_SIDE_PROTECT:
				if self.moShowEnemyPosTimer:
					self.popTimer(self.moShowEnemyPosTimer)
					self.moShowEnemyPosTimer = 0
				if self.moHideEnemyPosTimer:
					self.popTimer( self.moHideEnemyPosTimer )
					self.moHideEnemyPosTimer = 0
				hideTime = (len(self.getEntityMailBoxRecord( scriptID )) * self.getScript().showTime) - self.moAlreadyShowTime
				self.moShowEnemyPosTimer = self.addTimerRepeat( 1.0, "showEnemyPos",(csdefine.BELONG_SIDE_PROTECT, csdefine.BELONG_SIDE_ATTACK) )
				self.moHideEnemyPosTimer = self.addTimerCallBack( hideTime,"HideEnemyPos",(csdefine.BELONG_SIDE_PROTECT,))
		
		if scriptID == self.getScript().jadeScriptID:
			if entityMailBox.getBelongSide() == csdefine.BELONG_SIDE_ATTACK:
				if self.xianAddJadeTimer:
					self.popTimer(self.xianAddJadeTimer)
					self.xianAddJadeTimer = 0
				self.xianAddJadeTimer = self.addTimerRepeat( 1.0,"memberAddJade",( csdefine.BELONG_SIDE_ATTACK, scriptID) )
			elif entityMailBox.getBelongSide() == csdefine.BELONG_SIDE_PROTECT:
				if self.moAddJadeTimer:
					self.popTimer(self.moAddJadeTimer)
					self.moAddJadeTimer = 0
				self.moAddJadeTimer = self.addTimerRepeat( 1.0,"memberAddJade",( csdefine.BELONG_SIDE_PROTECT, scriptID) )
		if scriptID == self.getScript().attrScriptID:
			self.memberAddBuff(entityMailBox.getBelongSide())


	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除 soldiersDict 记录
		"""
		SpaceCopy.delEntityMailBoxRecord( self, scriptID, entityMailBox )
		if scriptID == self.getScript().attrScriptID:
			self.memberRemoveBuff(entityMailBox.getBelongSide())

		if scriptID not in self.soldierIDList:
			return

		way = entityMailBox.way
		number = entityMailBox.number
		if way not in self.soldiersDict or number not in self.soldiersDict[way] or entityMailBox not in self.soldiersDict[way][number]:
			return

		self.soldiersDict[way][number].remove(entityMailBox)
		if len(self.soldiersDict[way][number]) == 0:
			self.soldiersDict[way].pop(number)

	def getEntityMailBoxByPatrolListAndNumber( self, way, number ):
		"""
		获得某一路的某一波兵
		"""
		soldiersDict = self.soldiersDict.get(way,{})
		return soldiersDict.get(number,[])

	def getEntityMailBoxByPatrolList( self, way ):
		"""
		获得某一路的小兵
		"""
		soldierList = []
		soldiersDict = self.soldiersDict.get(way,{})
		for soldiers in soldiersDict.values():
			soldierList.extend(soldiers)

		return soldierList

	def buyRandomScriptID( self, role,scriptID ):
		"""
		随机事件 购买小兵
		"""
		self.getScript().buyRandomScriptID( self,role,scriptID )

	def showEnemyPos( self, srcCamp, dstCamp ):
		"""
		显示dstCamp 玩家坐标
		"""
		if srcCamp == csdefine.BELONG_SIDE_ATTACK:
			self.xianAlreadyShowTime += 1.0
		elif srcCamp == csdefine.BELONG_SIDE_PROTECT:
			self.moAlreadyShowTime += 1.0
		members = self.memberDatas.getMembersByCamp( srcCamp )
		enemyMembers = self.memberDatas.getMembersByCamp( dstCamp )
		tempPos = []
		for enemyMember in enemyMembers:
			tempPos.append( KBEMath.KBEngine2UnrealPosition(enemyMember.roleMB.position))
		for member in members:
			if member.roleMB.getClient():
				member.roleMB.client.CLIENT_showEnemyPos( tempPos )

	def HideEnemyPos( self, belongSide ):
		"""
		隐藏魔道玩家坐标
		"""
		if belongSide == csdefine.BELONG_SIDE_ATTACK and self.xianShowEnemyPosTimer:
			self.popTimer( self.xianShowEnemyPosTimer )
			self.xianShowEnemyPosTimer = 0
			self.xianAlreadyShowTime = 0.0
		if belongSide == csdefine.BELONG_SIDE_PROTECT and self.moShowEnemyPosTimer:
			self.popTimer( self.moShowEnemyPosTimer )
			self.moShowEnemyPosTimer = 0
			self.moAlreadyShowTime = 0.0
		members = self.memberDatas.getMembersByCamp( belongSide )
		for member in members:
			if member.roleMB.getClient():
				member.roleMB.client.CLIENT_HideEnemyPos()

	def memberAddJade( self, camp, scriptID):
		"""
		增加camp玩家魂玉
		"""
		if not len(self.getEntityMailBoxRecord( scriptID )):
			if camp == csdefine.BELONG_SIDE_ATTACK:
				self.popTimer( self.xianAddJadeTimer)
				self.xianAddJadeTimer = 0
			elif camp == csdefine.BELONG_SIDE_PROTECT:
				self.popTimer( self.moAddJadeTimer )
				self.moAddJadeTimer = 0
			return
		jadeValue = len(self.getEntityMailBoxRecord( scriptID )) *  self.getScript().jadeScriptIDRewardJade
		members = self.memberDatas.getMembersByCamp( camp )
		for member in members:
			member.roleMB.addJade( jadeValue )

	def memberAddBuff( self, belongSide ):
		"""
		camp玩家增加Buff
		"""
		members = self.memberDatas.getMembersByCamp( belongSide )
		for member in members:
			member.roleMB.addBuff(member.roleMB, self.getScript().attrScriptIDRewardBuff )

	def memberRemoveBuff( self , belongSide ):
		"""
		camp玩家移除Buff
		"""
		members = self.memberDatas.getMembersByCamp( belongSide )
		for member in members:
			member.roleMB.removeBuffByID(self.getScript().attrScriptIDRewardBuff )

	def hasSpecialMonsterNumber( self, role ):
		"""
		判断是否含有特殊Monster
		"""
		number = 0
		specialMonsters = [i for i in self.getEntityMailBoxRecord(self.getScript().jadeScriptID) if i.getBelongSide() == role.getBelongSide()]

		if len(specialMonsters):
			for specialMonster in specialMonsters:
				if role.position.distTo( specialMonster.position ) < self.getScript().jadeScriptIDRewardRadius:
					number += 1
		return number

	def addKillRewardExp( self, camp,value ):
		"""
		击杀获得经验
		"""
		members = self.memberDatas.getMembersByCamp( camp )
		for member in members:
			totalAddExpValue = member.getTotalAddExpValue()
			if totalAddExpValue == self.getScript().killRewardExpUpper:
				continue
			if totalAddExpValue + value > self.getScript().killRewardExpUpper:
				member.addTotalAddExpValue( (self.getScript().killRewardExpUpper - totalAddExpValue) )
			else:
				member.addTotalAddExpValue( value )

	def addMemberRewardExp( self, player, value ):
		"""
		增加成员经验
		"""
		member = self.memberDatas.getMemberByPlayerDBID( player.playerDBID )
		if member != None:
			totalAddExpValue = member.getTotalAddExpValue()
			if totalAddExpValue == self.getScript().killRewardExpUpper:
				return
			if totalAddExpValue + value > self.getScript().killRewardExpUpper:
				member.addTotalAddExpValue( (self.getScript().killRewardExpUpper - totalAddExpValue) )
			else:
				member.addTotalAddExpValue( value )

	def addEndRewardExp( self ):
		"""
		结算奖励
		"""
		if self.winCamp == csdefine.BELONG_SIDE_ATTACK:
			failCamp = csdefine.BELONG_SIDE_PROTECT
		else:
			failCamp = csdefine.BELONG_SIDE_ATTACK
		members = self.memberDatas.getMembersByCamp( self.winCamp )
		rewardDatas = RewardMgr.g_rewardMgr.getReward(self.getScript().rewardExploitID,{})
		for member in members:
			RewardMgr.g_rewardMgr.doRewards( rewardDatas, member.roleMB.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_OCCUPY_LBC )

