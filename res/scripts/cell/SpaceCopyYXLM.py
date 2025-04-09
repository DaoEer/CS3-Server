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
import csconst
import ZyjjRewardData
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader

class SpaceCopyYXLM( SpaceCopy ):
	"""
	英雄联盟
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.xianTeamID = self.createArgs.get("xianTeamID",0)
		self.moTeamID = self.createArgs.get("moTeamID",0)
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
		
		self.memberInfos = {}
		self.zyjjRewardDatas = ZyjjRewardData.ZyjjRewardDatas()

	def addYXLMMemberData( self, roleMB ):
		"""
		增加成员数据
		"""
		self.memberDatas.add( roleMB )
		self.memberInfos[roleMB.playerDBID] = (roleMB.getCamp(), roleMB.level, roleMB.playerName)

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
				camp = entity.getCamp()
				entity.delayDestroy(1.0)
				wayStr = cschannel_msgs.YXLM_TOWER_NAME.get(wayType,"")
				memberList = self.memberDatas.getMembersByCamp( camp )
				for member in memberList:
					member.roleMB.statusMessage( csstatus.SPACECOPY_CAMP_YXLM_BUILIDING_UPGRADE,wayStr )
				enemyMemberList =[]
				if camp == csdefine.CAMP_TAOSIM:
					enemyMemberList = self.memberDatas.getMembersByCamp( csdefine.CAMP_DEMON )
				elif camp == csdefine.CAMP_DEMON:
					enemyMemberList = self.memberDatas.getMembersByCamp( csdefine.CAMP_TAOSIM )
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
			if entityMailBox.getCamp() == csdefine.CAMP_TAOSIM:
				if self.xianShowEnemyPosTimer:
					self.popTimer(self.xianShowEnemyPosTimer)
					self.xianShowEnemyPosTimer = 0
				if self.xianHideEnemyPosTimer:
					self.popTimer( self.xianHideEnemyPosTimer )
					self.xianHideEnemyPosTimer = 0
				hideTime = (len(self.getEntityMailBoxRecord( scriptID )) * self.getScript().showTime) - self.xianAlreadyShowTime
				self.xianShowEnemyPosTimer = self.addTimerRepeat( 1.0, "showEnemyPos",(csdefine.CAMP_TAOSIM,csdefine.CAMP_DEMON) )
				self.xianHideEnemyPosTimer = self.addTimerCallBack( hideTime,"HideEnemyPos",( csdefine.CAMP_TAOSIM,) )
			elif entityMailBox.getCamp() == csdefine.CAMP_DEMON:
				if self.moShowEnemyPosTimer:
					self.popTimer(self.moShowEnemyPosTimer)
					self.moShowEnemyPosTimer = 0
				if self.moHideEnemyPosTimer:
					self.popTimer( self.moHideEnemyPosTimer )
					self.moHideEnemyPosTimer = 0
				hideTime = (len(self.getEntityMailBoxRecord( scriptID )) * self.getScript().showTime) - self.moAlreadyShowTime
				self.moShowEnemyPosTimer = self.addTimerRepeat( 1.0, "showEnemyPos",(csdefine.CAMP_DEMON,csdefine.CAMP_TAOSIM) )
				self.moHideEnemyPosTimer = self.addTimerCallBack( hideTime,"HideEnemyPos",( csdefine.CAMP_DEMON,) )
		if scriptID == self.getScript().jadeScriptID:
			if entityMailBox.getCamp() == csdefine.CAMP_TAOSIM:
				if self.xianAddJadeTimer:
					self.popTimer(self.xianAddJadeTimer)
					self.xianAddJadeTimer = 0
				self.xianAddJadeTimer = self.addTimerRepeat( 1.0,"memberAddJade",( csdefine.CAMP_TAOSIM, scriptID) )
			elif entityMailBox.getCamp() == csdefine.CAMP_DEMON:
				if self.moAddJadeTimer:
					self.popTimer(self.moAddJadeTimer)
					self.moAddJadeTimer = 0
				self.moAddJadeTimer = self.addTimerRepeat( 1.0,"memberAddJade",( csdefine.CAMP_DEMON, scriptID) )
		if scriptID == self.getScript().attrScriptID:
			if entityMailBox.getCamp() == csdefine.CAMP_TAOSIM:
				self.memberAddBuff(csdefine.CAMP_TAOSIM)
			elif entityMailBox.getCamp() == csdefine.CAMP_DEMON:
				self.memberAddBuff(csdefine.CAMP_DEMON)

	def delEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		删除 soldiersDict 记录
		"""
		SpaceCopy.delEntityMailBoxRecord( self, scriptID, entityMailBox )
		if scriptID == self.getScript().attrScriptID:
			if entityMailBox.getCamp() == csdefine.CAMP_TAOSIM:
				self.memberRemoveBuff( csdefine.CAMP_TAOSIM )
			elif entityMailBox.getCamp() == csdefine.CAMP_DEMON:
				self.memberRemoveBuff( csdefine.CAMP_DEMON )
		if scriptID not in self.soldierIDList:
			return
		way = entityMailBox.way
		number = entityMailBox.number
		if way not in self.soldiersDict:
			return
		if number not in self.soldiersDict[way]:
			return
		if entityMailBox not in self.soldiersDict[way][number]:
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
		if srcCamp == csdefine.CAMP_TAOSIM:
			self.xianAlreadyShowTime += 1.0
		elif srcCamp == csdefine.CAMP_DEMON:
			self.moAlreadyShowTime += 1.0
		members = self.memberDatas.getMembersByCamp( srcCamp )
		enemyMembers = self.memberDatas.getMembersByCamp( dstCamp )
		tempPos = []
		for enemyMember in enemyMembers:
			tempPos.append( KBEMath.KBEngine2UnrealPosition(enemyMember.roleMB.position))
		for member in members:
			if member.roleMB.getClient():
				member.roleMB.client.CLIENT_showEnemyPos( tempPos )

	def HideEnemyPos( self, camp ):
		"""
		隐藏魔道玩家坐标
		"""
		if camp == csdefine.CAMP_TAOSIM and self.xianShowEnemyPosTimer:
			self.popTimer( self.xianShowEnemyPosTimer )
			self.xianShowEnemyPosTimer = 0
			self.xianAlreadyShowTime = 0.0
		if camp == csdefine.CAMP_DEMON and self.moShowEnemyPosTimer:
			self.popTimer( self.moShowEnemyPosTimer )
			self.moShowEnemyPosTimer = 0
			self.moAlreadyShowTime = 0.0
		members = self.memberDatas.getMembersByCamp( camp )
		for member in members:
			if member.roleMB.getClient():
				member.roleMB.client.CLIENT_HideEnemyPos()

	def memberAddJade( self, camp, scriptID):
		"""
		增加camp玩家魂玉
		"""
		if not len(self.getEntityMailBoxRecord( scriptID )):
			if camp == csdefine.CAMP_TAOSIM:
				self.popTimer( self.xianAddJadeTimer)
				self.xianAddJadeTimer = 0
			elif camp == csdefine.CAMP_DEMON:
				self.popTimer( self.moAddJadeTimer )
				self.moAddJadeTimer = 0
			return
		jadeValue = len(self.getEntityMailBoxRecord( scriptID )) *  self.getScript().jadeScriptIDRewardJade
		members = self.memberDatas.getMembersByCamp( camp )
		for member in members:
			member.roleMB.addJade( jadeValue )

	def memberAddBuff( self, camp ):
		"""
		camp玩家增加Buff
		"""
		members = self.memberDatas.getMembersByCamp( camp )
		for member in members:
			member.roleMB.addBuff(member.roleMB, self.getScript().attrScriptIDRewardBuff )

	def memberRemoveBuff( self , camp ):
		"""
		camp玩家移除Buff
		"""
		members = self.memberDatas.getMembersByCamp( camp )
		for member in members:
			member.roleMB.removeBuffByID(self.getScript().attrScriptIDRewardBuff )

	def hasSpecialMonsterNumber( self, role ):
		"""
		判断是否含有特殊Monster
		"""
		number = 0
		specialMonsters = self.getEntityMailBoxRecord( self.getScript().jadeScriptID )
		if role.getCamp() == csdefine.CAMP_TAOSIM:
			specialMonsters = [ i for i in specialMonsters if i.getCamp() == csdefine.CAMP_TAOSIM ]
		elif role.getCamp() == csdefine.CAMP_DEMON:
			specialMonsters = [ i for i in specialMonsters if i.getCamp() == csdefine.CAMP_DEMON ]
		if not len( specialMonsters ):
			return number
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

	def addEndReward( self ):
		"""
		奖励功勋、经验、军功
		"""
		for dbid, memberInfo in self.memberInfos.items():
			if memberInfo[0] == self.winCamp:
				exp = self.getScript().getWinFinalRewardExp(memberInfo[1])
				feats = self.getScript().endWinFeats
				exploit = self.getScript().endWinExploit
				mailID = self.getScript().getWinFinalMailID(memberInfo[1])
				offLineMailID = self.getScript().getWinOffLineFinalMailID(memberInfo[1])
			else:
				exp = self.getScript().getFailFinalRewardExp(memberInfo[1])
				feats = self.getScript().endFailFeats
				exploit = self.getScript().endFailExploit
				mailID = self.getScript().getFailFinalMailID(memberInfo[1])
				offLineMailID = self.getScript().getFailOffLineFinalMailID(memberInfo[1])
			
			playerRole = None
			for role in self._spaceRoles:
				if role.playerDBID == dbid:
					playerRole = role
					break
			
			KBEDebug.DEBUG_MSG("%s -- %s -- %s -- %s - %s" %(exp, feats, exploit, mailID, offLineMailID))
			self.addFinalExploit(playerRole, dbid, exploit)
			self.addFailFeats(playerRole, dbid, feats, csdefine.FEATS_ADD_REASON_YXWZ)
			self.addFinalExpReward(playerRole, dbid, exp, csdefine.EXP_ADD_REASON_YXLM_FINAL_EXP)
			
			if mailID: g_mailContentDataLoader.sendSpaceReward(mailID, memberInfo[2])
			if playerRole is None and offLineMailID: g_mailContentDataLoader.sendSpaceReward(offLineMailID, memberInfo[2])
			
		
#-------------------------阵营竞技结算奖励------------------------------------

	def addFinalContributionReward(self):
		#帮贡奖励 CST-13692
		#同一个帮会的成员分类
		tongDict = {}
		for player in self._spaceRoles:
			tongMB = player.tongMB
			if not tongMB:
				continue
			if tongMB.id not in tongDict:
				tongDict[tongMB.id] = []
			tongDict[tongMB.id].append(player)
		#同帮会成员人数达标后才可获得奖励
		for playerList in tongDict.values():
			amount = len(playerList)
			if amount in csconst.ZYJJ_REWARD_CONTRIBUTION:
				ctrbValue = csconst.ZYJJ_REWARD_CONTRIBUTION[amount]
				for player in playerList:
					player.addContribution(ctrbValue)
					self.zyjjRewardDatas.addContribution(player.playerDBID, ctrbValue)

	def addFinalExpReward(self, playerRole, playerDBID, value, reason):
		"""
		"""
		if playerRole: playerRole.addExp(value, reason)
		self.zyjjRewardDatas.addExp(playerDBID, value)
		
	def addFailFeats(self, playerRole, playerDBID, value, reason):
		"""
		"""
		if playerRole: playerRole.addFeats(value)
		self.zyjjRewardDatas.addFeats(playerDBID, value)
		
	def addFinalExploit(self, playerRole, playerDBID, value):
		"""
		"""
		if playerRole: playerRole.addExploit(value)
		self.zyjjRewardDatas.addExploit(playerDBID, value)