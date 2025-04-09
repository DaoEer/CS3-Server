
# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import KST
import time
import csstatus
import csdefine
import Const
import copy
import random
import Math
import math
import KBEMath

from Barracks.TrainingGroundCombatDatas import Datas as TGCombatDatas
from Barracks.TrainingGroundQuestDatas import Datas as TGQuestDatas
from Barracks.TrainingGroundPointDatas import Datas as TGQPointDatas


from RoleOccupyTrainInfo import RoleOccupyTrainInfo

class RoleTrainSoldierGroundInterface:
	"""
	玩家练兵场数据
	"""
	def __init__( self ):
		"""
		初始化
		"""
		self.initTGQuest()

	def setRoleOccupyTrainData( self, lineNumber, index ):
		"""
		设置占领练兵场数据
		"""
		self.occupyTrainData.occupyTrainLineNumber = lineNumber
		self.occupyTrainData.occupyTrainIndex = index

	def getRoleOccupyTrainType( self ):
		"""
		获得玩家占领的练兵场类型
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_STAND_MAP:
			npcEntity = spaceEntity.getTrainSoldierGroundEntityByIndex( self.occupyTrainData.occupyTrainIndex )
			if not npcEntity:
				return 0
			return npcEntity.getScript().getTrainGroundType()
		return 0

	def isOccupyTrain( self, occupyTrainType = csdefine.NPCTRAINSOLDIERGROUND_TYPE_NONE ):
		"""
		是否占领练兵场
		"""
		if self.occupyTrainData.occupyTrainLineNumber > 0 and self.occupyTrainData.occupyTrainIndex >= 0 and self.getRoleOccupyTrainType() >= occupyTrainType:
			return True
		return False

	def getRoleOccupyTrainData( self ):
		"""
		获得玩家占领的领兵场数据
		"""		
		return self.occupyTrainData.occupyTrainLineNumber, self.occupyTrainData.occupyTrainIndex

	def onClientGetCell( self ):
		"""
		"""
		KBEngine.globalData["TrainSoldierGroundManager"].queryIsDeclareWar( self.base, self.playerDBID )
		KBEngine.globalData["TrainSoldierGroundManager"].queryRoleOccupyTrainGroundData( self.base, self.playerDBID )

	def setIsDeclareWar( self, isDeclareWar ):
		"""
		是否已经发起了宣战
		"""
		self.isDeclareWar = isDeclareWar
		if self.isDeclareWar:
			KBEngine.globalData["TrainSoldierGroundManager"].addDeclareWarPlayer( self.playerDBID )
		else:
			KBEngine.globalData["TrainSoldierGroundManager"].removeDeclareWarPlayer( self.playerDBID )

	def getIsDeclareWar( self ):
		"""
		"""
		return self.isDeclareWar

	def sendIsJoinDeclareWarMsg( self, lineNumber, trainSoldierGroundIndex, spaceScriptID, npcEntity, occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict ):
		"""
		发送是否参与某个练兵场争夺
		"""
		self.inquireMessage( csstatus.TRAIN_SOLDIER_GROUND_DECLARWAR_SURE,"","replyIsJoinDeclareWar",lineNumber, trainSoldierGroundIndex, spaceScriptID, npcEntity,occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict)

	def replyIsJoinDeclareWar( self, reply, lineNumber, trainSoldierGroundIndex, spaceScriptID, npcEntity,occupyPlayerDBID,trainGroundType,npcName,npcTrainGroundDict ):
		"""
		是否参与练兵场争夺
		"""
		if reply:
			if trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL:
				self.gotoTrainSoldierGround( lineNumber, trainSoldierGroundIndex, spaceScriptID,occupyPlayerDBID,npcName,trainGroundType,npcTrainGroundDict )
				npcEntity.setDclareWarState( csdefine.NPCTRAINSOLDIERGROUND_STATE_FIGHT )
				npcEntity.calculatFightEndTime( spaceScriptID )
			elif trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL or trainGroundType == csdefine.NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL:
				if self.gotoSeniorTrainSoldierGround( lineNumber, trainSoldierGroundIndex, spaceScriptID,occupyPlayerDBID,npcName,trainGroundType,npcTrainGroundDict ):
					npcEntity.setDclareWarState( csdefine.NPCTRAINSOLDIERGROUND_STATE_FIGHT )
					npcEntity.calculatFightEndTime( spaceScriptID )
		else:
			if self.playerDBID != occupyPlayerDBID:
				npcEntity.clearDeclareWarData()
				self.setIsDeclareWar( False )

	def gotoTrainSoldierGround( self, lineNumber, trainSoldierGroundIndex, spaceScriptID,occupyPlayerDBID,npcName,trainGroundType,npcTrainGroundDict ):
		"""
		请求进入某个练兵场
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
		if not spaceObj:
			return
		if self.playerDBID == occupyPlayerDBID:	
			enterInfo = spaceObj.getProtectEnterInfo()
		else:
			enterInfo = spaceObj.getAttackEnterInfo()
		packArgs = {}
		packArgs["lineNumber"] = lineNumber
		packArgs["trainSoldierGroundIndex"] = trainSoldierGroundIndex
		packArgs["belongDBID"] = occupyPlayerDBID
		packArgs["trainGroundName"] = npcName
		packArgs["trainGroundType"] = trainGroundType
		packArgs["trainGroundDict"] = npcTrainGroundDict
		self.setIsDeclareWar(False)
		self.gotoSpaceUseArg( spaceScriptID, enterInfo[0], enterInfo[1], packArgs )

	def gotoSeniorTrainSoldierGround( self, lineNumber, trainSoldierGroundIndex, spaceScriptID,occupyPlayerDBID,npcName,trainGroundType,npcTrainGroundDict ):
		"""
		请求进入高级练兵场
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
		if not spaceObj:
			return False
		num = spaceObj.getAllowTeamNumber()
		if len(self.getAllTeamMemberMB()) != num:
			return False
		for entityMB in self.getAllTeamMemberMB():
			packArgs = {}
			packArgs["lineNumber"] = lineNumber
			packArgs["trainSoldierGroundIndex"] = trainSoldierGroundIndex
			packArgs["belongDBID"] = occupyPlayerDBID
			playerDBIDS = self.getAllTeamMemberDBIDs()
			packArgs["enterDBIDs"] = playerDBIDS
			packArgs["trainGroundName"] = npcName
			packArgs["trainGroundType"] = trainGroundType
			packArgs["trainGroundDict"] = npcTrainGroundDict
			if self.playerDBID == occupyPlayerDBID:	
				enterInfo = spaceObj.getProtectEnterInfo()
				packArgs["belongSide"] = csdefine.BELONG_SIDE_PROTECT
			else:
				enterInfo = spaceObj.getAttackEnterInfo()
				packArgs["belongSide"] = csdefine.BELONG_SIDE_ATTACK
			self.setIsDeclareWar(False)
			entityMB.cell.gotoSpaceUseArg( spaceScriptID, enterInfo[0], enterInfo[1], packArgs )
		return True

	def declareTrainSoldierGround( self, srcEntityID, npcID ):
		"""
		exposed method
		跟练兵场 宣战
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npcEntity = KBEngine.entities.get( npcID, None )
		if not npcEntity:
			return
		npcEntity.declareTrainSoldierGround( self.id )

	def cancelDeclareTrainSoldierGround( self, srcEntityID, npcID ):
		"""
		exposed method
		取消练兵场宣战
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npcEntity = KBEngine.entities.get( npcID, None )
		if not npcEntity:
			return
		npcEntity.cancelDeclareTrainSoldierGround( self.id )
		
	#-------------------------------------------------------------------------------------------------
	# 练兵场任务
	#-------------------------------------------------------------------------------------------------
	def initTGQuest( self ):
		"""玩家上线，初始化任务"""
		for battackID, dataList in dict(self.TGQuestDict).items():
			# 这里有一个 设计缺陷，有可能玩家重新上线，跟那个 怪物不在同一个cell。但是，这边不作考虑。因为练兵任务战斗才20秒。时间不长。
			monster = KBEngine.entities.get(dataList[1])				
			if monster:
				monster.onPlayerOnLine( self.base )
				if monster.process == 0:continue
			else:
				army = self.getRoleArmyDataByID( battackID )
				army.setComtrolArmy(0)
			self.onTGQuestFightEnd(battackID)
	
	def requestTrainGroundQuest( self, npcID ):
		"""
		请求练兵场任务数据
		"""
		self.client.InitRoleArmyDatas( list( self.roleArmyDatas.values() ) )
		self.tryRefreshTGQuestNum()
		if self.isSysRefreshTGQuest():
			self.refreshTGQTime = time.time()
			self.refreshTrainGroundQuest()
		doingTGQuest = []
		for dataList in self.TGQuestDict.values():
			doingTGQuest.append( dataList[1] )
		questDatas = []
		ids= []
		for id in self.trainGroundQuest:
			if id in ids:continue
			ids.append(id)
			data = TGQuestDatas[id]
			temp = {}
			temp["title"] = data["title"]
			temp["questID"] = data["questID"]
			temp["taskTitle"] = data["description"]
			temp["reward"] = data["successReward"]
			soldiers = list(data["general"].keys())
			temp["soldierScriptID"] = soldiers[0] if soldiers else ""
			questDatas.append(temp)
			
		self.client.CLIENT_initTrainGroundQuest( npcID, self.trainGroundQuest, self.successTGQuest, self.failTGQuest, doingTGQuest, questDatas)
		
	def tryRefreshTGQuestNum( self ):
		"""刷新 练兵场任务 完成个数"""
		nTime = time.localtime()
		rTime = time.localtime( self.refreshTGQTime )
		if nTime.tm_year > rTime.tm_year or nTime.tm_mon > rTime.tm_mon or nTime.tm_mday > rTime.tm_mday:
			self.trainGroundQuestNum = 0
		
	def isSysRefreshTGQuest( self ):
		"""是否 系统刷新"""
		sTime = time.time()
		lTime = time.localtime(sTime)
		for tKey in Const.TRAIN_GROUND_REFRESH_TIME:
			t = (lTime.tm_year, lTime.tm_mon, lTime.tm_mday, tKey, 0, 0, 0, 0, 0)
			tTime = time.mktime(t)
			if self.refreshTGQTime < tTime and sTime >= tTime:
				return True
		return False
		
	def refreshTrainGroundQuest( self ):
		"""
		刷新 练兵场任务
		"""
		self.trainGroundQuest = []						# 玩家所有的练兵任务
		self.successTGQuest = []						# 成功完成的练兵任务
		self.failTGQuest = []							# 失败的练兵任务
		self.refreshTGQTime = time.time()
		if self.TGQuestDict:
			for id, dataList in self.TGQuestDict.items():	# 备注已经刷新了任务
				dataList.append(1)
		
		questList = list( TGQuestDatas.keys() )
		if not questList:
			return
		for i in range( Const.TRAIN_GROUND_QUEST_NUM ):
			self.trainGroundQuest.append( random.choice( questList) )
			
	def requestRefreshTGQuest( self, srcEntityID ):
		"""
		exposed method
		请求刷新 练兵场任务
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		payItems ={}
		payItems[ csdefine.TRADE_PAY_ITEM_MONEY ] = Const.TRAIN_GROUND_REFRESH_MONEY

		self.requestPay( csdefine.TRADE_TYPE_REFRESH_TG_QUEST, 0, payItems )
		
	def doRefreshTGQuest( self ):
		""""""
		self.refreshTrainGroundQuest()
		questDatas = []
		ids= []
		for id in self.trainGroundQuest:
			if id in ids:continue
			ids.append(id)
			data = TGQuestDatas[id]
			temp = {}
			temp["title"] = data["title"]
			temp["questID"] = data["questID"]
			temp["taskTitle"] = data["description"]
			temp["reward"] = data["successReward"]
			soldiers = list(data["soldier"].keys())
			temp["soldierScriptID"] = soldiers[0] if soldiers else ""
			questDatas.append(temp)
		self.client.CLIENT_OnRefreshTGQuest(self.trainGroundQuest, questDatas)
		
	def autoRefreshTGQuest( self, srcEntityID ):
		"""
		exposed method
		系统刷新 任务
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if not self.isSysRefreshTGQuest():
			KBEDebug.ERROR_MSG("role(%d) refresh sys TG Quest!as time not reach~"%self.id)
			return
			
		self.refreshTGQTime = time.time()
		self.doRefreshTGQuest()

	def requestAcceptTGQuest( self, srcEntityID, index, battackID ):
		"""
		exposed method
		接受 练兵任务
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if index in self.successTGQuest or index in self.failTGQuest:
			KBEDebug.ERROR_MSG("index(%d) is no avalid!"%index)
			return
		for dataList in self.TGQuestDict.values():
			if dataList[1] == index:
				KBEDebug.ERROR_MSG("quest(index:%d) is doing!"%index)
				return
		questID = self.trainGroundQuest[index]
		if not self.canDispatch( battackID ):
			KBEDebug.ERROR_MSG("can not dispatch soldiers(%d)!as not free"%battackID)
			return
		if self.occupyTrainData.occupyTrainIndex < 0:
			KBEDebug.ERROR_MSG("role not occupy Train(%d)"%self.occupyTrainData.occupyTrainIndex)
			return
		if not self.occupyTrainData.occupyTrainIndex in TGQPointDatas or not questID in TGQPointDatas[self.occupyTrainData.occupyTrainIndex]:
			KBEDebug.ERROR_MSG("role(%d) occupyTrainIndex(%d) is not in config,or questID(%d) not in config"%(self.id, self.occupyTrainData.occupyTrainIndex, questID))
			return
		army = self.getRoleArmyDataByID( battackID )
		if army is None:
			KBEDebug.ERROR_MSG("not battackID(%) in the roleArmyDatas property!"%battackID)
			return
		if self.trainGroundQuestNum >= Const.TRAIN_GROUND_QUEST_MAX_NUM:
			self.statusMessage( csstatus.TRAIN_SOLDIER_GROUND_QUEST_FULL )
			return
		payItems ={}
		payItems[ csdefine.TRADE_PAY_ITEM_GOODS_BY_ID ] = {Const.TRAIN_GROUND_QUEST_UST_ITEM : 1}
		self.requestPay( csdefine.TRADE_TYPE_ACCEPT_QUEST, 0, payItems, index, questID, battackID )
		
	def onAcceptTGQuest(self, index, questID, battackID ):
		""""""
		self.trainGroundQuestNum += 1
		
		army = self.getRoleArmyDataByID( battackID )
		soldierObj = KST.g_objFactory.getMonsterObject( army.firstGuardScriptID )
		tempDict = {}
		data = TGQPointDatas[self.occupyTrainData.occupyTrainIndex][questID]
		params = {}
		params["spawnPos"] = Math.Vector3( data["spawnPos"] )
		params["extraModelNumber"] = soldierObj.getEntityProperty( "modelNumber","" )
		params["basePlayerMB"] = self.base
		params["battackID"] = battackID
		params["dstPos"] = Math.Vector3( data["dstPos"] )
		monster = self.createEntityByScriptID( Const.TRAIN_GROUND_QUEST_SRC_SCRIPTID, params["spawnPos"], Math.Vector3( data["spawnDir"] ), params )
		if monster is None:
			return
		soldierObj = KST.g_objFactory.getMonsterObject( army.soldierScriptID )
		monster.setArmyModelList([ soldierObj.getEntityProperty( "modelNumber","" ),])
		army.setComtrolArmy(monster.id)
		self.TGQuestDict[battackID] = [questID, index, monster.id] 
		self.client.CLIENT_OnAcceptTGQuest( index, battackID )

	def onTGQuestFightEnd(self, battackID):
		"""
		<define method>
		练兵任务 战斗结束
		"""
		dataList = self.TGQuestDict.pop( battackID )
		bRefreshAlready = len(dataList) >= 4
		questID = dataList[0]
		index = dataList[1]
		self.calcelateQuestResult( questID, index, battackID, bRefreshAlready )

	def calcelateQuestResult( self, questID, index, battackID, bRefreshAlready ):
		"""计算 练兵任务结果"""
		army = self.getRoleArmyDataByID(battackID)
		playerCombat = self.calcelatePlayerCombat( army )
		enemyCombat = self.calcelateEnemyCombat( questID )
		combatRate = playerCombat / enemyCombat
		if combatRate < Const.TRAIN_GROUND_QUEST_MIN_RATE_NUM:
			result = 0
		elif combatRate >= Const.TRAIN_GROUND_QUEST_MAX_RATE_NUM:
			result = 1
		else:
			result = int( math.pow( (math.sin( combatRate - 1) + 1), 1.8 ) * 0.5 >= random.random() )
	
		questData = TGQuestDatas[questID]
		if result:
			averLossNum = round( 1 / combatRate * 1.125)
			exp = questData["successReward"]
			if not bRefreshAlready:
				self.successTGQuest.append( index )
		else:
			averLossNum = round(1 / combatRate * 3.375)
			exp = questData["failReward"]
			if not bRefreshAlready:
				self.failTGQuest.append( index )
		addExp = 0
		if self.findLastBuffByBuffID( Const.TRAIN_GROUND_QUEST_DOU_BUFF ) >= 0:
			addExp = exp
			exp += addExp
		elif self.findLastBuffByBuffID( Const.TRAIN_GROUND_QUEST_POiNT_FIVE_BUFF ) >= 0:
			addExp = int( exp / 2 )
			exp += addExp
		
		self.addBarracksExp( exp )
		lossNum = min( max(averLossNum + random.randint(-3, 3), 0), len(army.soldierIDs))
		lossSoldiers = random.sample(army.soldierIDs, lossNum)
		for id in lossSoldiers:
			self.onSoliderDead( battackID, csdefine.BARRACKS_SOLDIER_COMMON_TYPE, army.soldierScriptID, id )
		
		self.client.CLIENT_onTGQuestResult( index, result, exp, addExp, battackID, lossNum, bRefreshAlready )
	
	def calcelatePlayerCombat( self, army ):
		"""计算玩家 派出士兵战斗力"""
		totalCombat = 0
		tempDict = {}
		tempList = []
		tempList.extend( self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, army.firstGuardScriptID ) )
		tempList.extend( self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_GUARD_TYPE, army.secondGuardScriptID ) )
		soldiers = self.roleBarracksMgr.getBarracksSoldiersByScriptID( csdefine.BARRACKS_SOLDIER_COMMON_TYPE, army.soldierScriptID )
		for soldier in soldiers:
			if soldier.id in army.soldierIDs:
				tempList.append( soldier )
		for soldier in tempList:
			if not soldier.scriptID in tempDict:
				tempDict[soldier.scriptID] = []
			tempDict[soldier.scriptID].append( soldier.level )
		for scriptID, levels in tempDict.items():
			for level in levels:
				totalCombat += self.getSoldireCombat(scriptID, level)
		return totalCombat
			
	def calcelateEnemyCombat( self, questID ):
		"""计算敌人战斗力"""
		totalCombat = 0
		questData = TGQuestDatas[questID]
		soldData = {}
		soldData.update( dict(questData["general"]) )
		soldData.update( dict(questData["soldier"]) )
		for scriptID, datas in soldData.items():
			totalCombat += datas["num"] * self.getSoldireCombat(scriptID, datas["level"])
		return totalCombat
			
	def getSoldireCombat(self, scriptID, level):
		"""获取士兵战斗力"""
		if not scriptID in TGCombatDatas:
			KBEDebug.ERROR_MSG("cannot find soldier(%s) combat in the config(TrainingGroundCombatDatas)"%scriptID)
			return 0
		if not level in TGCombatDatas[scriptID]:
			KBEDebug.ERROR_MSG("cannot find soldier(%d) level(%d) combat in the config(TrainingGroundCombatDatas)"%(scriptID,level))
			return 0
		return TGCombatDatas[scriptID][level]
		
	def onSoldierBackHome( self, battackID ):
		"""
		<define method>
		部队 回到 大本营
		"""
		army = self.getRoleArmyDataByID( battackID )
		army.setComtrolArmy(0)
		self.client.CLIENT_onSoldierFinishQuestBack( battackID )

	def requestGotoTrainGroundByGroup( self, srcEntityID, lineNumber, group, position ):
		"""
		exposed method
		请求传送到某个练兵场
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		packArgs = {}
		packArgs["spaceKey"] = str(lineNumber)
		packArgs["playerDBID"] = self.playerDBID
		packArgs["belongType"] = csdefine.SPACE_BELONG_NORMAL
		pos = KBEMath.Unreal2KBEnginePosition( position )
		KBEngine.globalData["TrainSoldierGroundManager"].enterStandMap( self.base, pos, self.direction, packArgs )

	def requestAllGroundDetail( self, srcEntityID, lineNumber, npcID ):
		"""
		exposed method
		请求某个分线的所有练兵场数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		roleLineNumber, index = self.getRoleOccupyTrainData()
		KBEngine.globalData["TrainSoldierGroundManager"].openAllGroundDetail( roleLineNumber, index, self, lineNumber,npcID )

	def openAllGroundDetail( self, roleOccupylineNumber, roleOccupytrainSoldierGroundIndex, trainGroundIndexs, trainGroundDBIDs, maxLineNumber, npcID ):
		"""
		"""
		if self.getClient():
			self.client.OpenAllGroundDetail( roleOccupylineNumber, roleOccupytrainSoldierGroundIndex, trainGroundIndexs, trainGroundDBIDs, maxLineNumber,npcID  )

	def requestAttckPos( self, srcEntityID ):
		"""
		exposed method
		低级练兵场请求 攻击玩家的位置
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
			KBEDebug.ERROR_MSG("err!!!attack side can not request self pos")
			return
		spaceEntity = self.getCurrentSpace()
		spaceEntity.requestAttckPos( self )
		
	def requestTeleportPos( self, srcEntityID, pos ):
		"""
		exposed method
		低级练兵场 守方请求传送
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.isBelongSide( csdefine.BELONG_SIDE_ATTACK ):
			KBEDebug.ERROR_MSG("err!!!attack side can not request teleport pos")
			return
		spaceEntity = self.getCurrentSpace()
		spaceEntity.requestTeleportPos( self, pos )
		
		
	