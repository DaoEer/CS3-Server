# -*- coding: utf-8 -*-

import KBEDebug
import csdefine
import KST
from LoadModule import *
import SmartImport
import Define
import json
import time
import GameObject.SpaceObject.SpaceStrategy.SpaceStrategyReward.SpaceStrategyGrade as SpaceStrategyGrade
import Reward.RewardBasicValueData as RewardBase

STRATEGY_REWARD_TYPE_EXP 			= 1		# 奖励经验
STRATEGY_REWARD_TYPE_POTENTIAL		= 2		# 奖励潜能
STRATEGY_REWARD_TYPE_CONTRIBUTION	= 3		# 奖励帮贡
STRATEGY_POINT_TIME_TYPE		= 60.0	#时间类型策略点  检测时间

class SpaceStrategyInterface:
	"""
	副本策略点接口
	"""
	def __init__( self ):
		self.spaceStrategyPointList = []	#副本策略点  #index 不一定连续
		self.roleStrategyPointDict = {}	 	#玩家个人策略点 {DBID:策略点obj}
		self.strategyPointTypeDict = {}	 	#记录策略点类型 {index:Define.SPACE_STRATEGYPOINT_BELONG_SPACE}
		self.recordSpaceStrategyPointReward = {} # 记录副本策略点是否已发放奖励 用于重进副本
		self.strategyTimerKey = {}  #{策略点index:timerID}

		self.spaceStrategyPointConditons = {} 	#副本策略点检测条件{ 策略点ID:[条件1，条件2]}
		self.rolePointConfitionDict = {}      	#玩家策略点检测条件 {DBID:{策略点ID:[条件1，条件2]}}
		self.strategyCondTypeDict = {}			#记录策略点条件类型 {策略点ID:{条件ID:Define.SPACE_STRATEGYPOINT_CONDITION_BELONG_SPACE}}


	def initSpaceStrategy( self, fileName ):
		"""
		初始化副本策略点数据  由于策略点条件归属类型也有 个人、副本、队伍区分  所以条件的初始化不写到SpaceStrategyPoint中(要与SpaceStrategyPoint区分)
		"""
		section = openJsonCfg( "GameObject/SpaceObject/SpaceStrategy/%s.json"%fileName )
		for index, config in section.items():
			self.strategyPointTypeDict[int(index)] = config["pointBelongType"]
			if config["pointBelongType"] == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
				objClass = SmartImport.smartImport("ConfigObject.SpaceStrategy.SpaceStrategyPoint:" + config["type"])
				instance = objClass()
				instance.init(int(index),config)
				self.spaceStrategyPointList.append(instance)

			for condition in config["conditions"]:
				if int(index) not in self.strategyCondTypeDict:
					self.strategyCondTypeDict[int(index)] = {}
				self.strategyCondTypeDict[int(index)][condition["id"]] = condition["conditionBelongType"]
				if condition["conditionBelongType"] == Define.SPACE_STRATEGYPOINT_CONDITION_BELONG_SPACE:
					if int(index) not in self.spaceStrategyPointConditons:
						self.spaceStrategyPointConditons[int(index)] = []
					objClass = SmartImport.smartImport("ConfigObject.SpaceStrategy.SpaceStrategyCondition:" + condition["conditionType"])
					instance = objClass()
					instance.init(condition["id"],condition)

					self.spaceStrategyPointConditons[int(index)].append(instance)

	def spaceStrategy_onPlayerEnter( self, selfEntity, roleCell, fileName ):
		"""
		玩家进入副本
		"""
		playerDBID = roleCell.playerDBID
		if playerDBID not in self.roleStrategyPointDict:
			self.addRoleStrategys(playerDBID, fileName )

		if playerDBID not in self.rolePointConfitionDict:
			self.addRoleStrategyConditions( playerDBID, fileName )
		
		#首先需要同步下策略点归属类型为队伍的数据, 个人和副本的就不需要了
		indexList = []
		for index, value in self.strategyPointTypeDict.items():
			if value == Define.SPACE_STRATEGYPOINT_BELONG_TEAM:
				indexList.append(index)
		self.synchronousTeamStrategyData( selfEntity, roleCell, indexList )

		#首先需要同步下策略点条件类型为队伍的数据，个人和副本的就不需要了
		conditionDict = {} #{策略点ID:[条件ID,条件ID]}
		for index, conDict in self.strategyCondTypeDict.items():
			for id,belongType in conDict.items():
				if belongType == Define.SPACE_STRATEGYPOINT_CONDITION_BELONG_TEAM:
					if index not in conditionDict:
						conditionDict[index] = []
					conditionDict[index].append( id )

		self.synchronousTeamConditionData( selfEntity, roleCell, conditionDict )

		for index in selfEntity.strategyEndIndexList:   #结束策略点
			if self.getStrategyType(index) == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
				strategyPoint = self.getSpaceStrategyPoint(index)
				#self.updateStrateToClient( selfEntity,roleCell,strategyPoint,1 )
				self.updateEndStrategyToClient( selfEntity,roleCell,strategyPoint )
			elif self.getStrategyType(index) in [Define.SPACE_STRATEGYPOINT_BELONG_PERSON,Define.SPACE_STRATEGYPOINT_BELONG_TEAM]:
				strategyPoint = self.getRoleStrategyPoint(roleCell.playerDBID,index)
				self.updateEndStrategyToClient( selfEntity,roleCell,strategyPoint )
		for index in selfEntity.strategyOpenIndexList:  #开启策略点
			if self.getStrategyType(index) in [Define.SPACE_STRATEGYPOINT_BELONG_PERSON,Define.SPACE_STRATEGYPOINT_BELONG_TEAM]:
				strategyPoint = self.getRoleStrategyPoint(roleCell.playerDBID,index)
				self.updateOpenStrateToClient( selfEntity,roleCell,strategyPoint)
			elif self.getStrategyType(index) == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
				strategyPoint = self.getSpaceStrategyPoint(index)
				self.updateOpenStrateToClient( selfEntity,roleCell,strategyPoint)

	def addRoleStrategys( self, roleDBID, fileName ):
		"""
		增加策略点
		"""
		section = openJsonCfg( "GameObject/SpaceObject/SpaceStrategy/%s.json"%fileName )
		roleStrategyList = []
		for index, config in section.items():
			if config["pointBelongType"] in [Define.SPACE_STRATEGYPOINT_BELONG_PERSON,Define.SPACE_STRATEGYPOINT_BELONG_TEAM]:
				objClass = SmartImport.smartImport("ConfigObject.SpaceStrategy.SpaceStrategyPoint:" + config["type"])
				instance = objClass()
				instance.init(int(index),config)
				roleStrategyList.append(instance)
		self.roleStrategyPointDict[roleDBID] = roleStrategyList

	def addRoleStrategyConditions( self, roleDBID, fileName ):
		"""
		增加策略点检测条件
		"""
		section = openJsonCfg( "GameObject/SpaceObject/SpaceStrategy/%s.json"%fileName )
		roleStrategyConditionDict = {}
		for index, config in section.items():
			for condition in config["conditions"]:
				if condition["conditionBelongType"] in [Define.SPACE_STRATEGYPOINT_CONDITION_BELONG_PERSON,Define.SPACE_STRATEGYPOINT_CONDITION_BELONG_TEAM]:
					if int(index) not in roleStrategyConditionDict:
						roleStrategyConditionDict[int(index)] = []
					objClass = SmartImport.smartImport("ConfigObject.SpaceStrategy.SpaceStrategyCondition:" + condition["conditionType"])
					instance = objClass()
					instance.init(condition["id"],condition)
					roleStrategyConditionDict[int(index)].append(instance)

		self.rolePointConfitionDict[roleDBID] = roleStrategyConditionDict


	def startStrategy( self, selfEntity, index ):
		"""
		开始某个策略点
		"""
		strategyType = self.getStrategyType(index)
		strategy = None
		if strategyType == Define.SPACE_STRATEGYPOINT_BELONG_NONE:
			KBEDebug.ERROR_MSG("Space not has strategyPoint(%i)"%index)
			return
		if (index not in selfEntity.strategyOpenIndexList) and (index not in selfEntity.strategyEndIndexList):
			selfEntity.strategyOpenIndexList.append(index)
		else:
			KBEDebug.ERROR_MSG("strategyPoint(index = %i, strategyOpenIndexList = %s, strategyEndIndexList = %s ) is alread to open or end"%(index,selfEntity.strategyOpenIndexList,selfEntity.strategyEndIndexList))
			return
		if strategyType == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
			strategy = self.getSpaceStrategyPoint(index)
		elif strategyType in [Define.SPACE_STRATEGYPOINT_BELONG_PERSON,Define.SPACE_STRATEGYPOINT_BELONG_TEAM]:
			if not len(selfEntity._spaceRoles):
				KBEDebug.ERROR_MSG("Space has no player")
				return
			strategy = self.getRoleStrategyPoint(selfEntity._spaceRoles[0].playerDBID, index) # 在这里随机取个玩家，因为开始某个策略点是副本所有玩家都是一致的
		if strategy.getType() == Define.SPACE_STRATEGYPOINT_TIME:
			strategy.setStartTime(time.time())
			selfEntity.addTimerCallBackForScript(1.0,"firstCheckStrategyPoint",(strategy.index,) )

		for role in selfEntity._spaceRoles:
			conditionDict = {}
			conditionList = self.getStrategyPointAllCondition( role.playerDBID, index )
			for condition in conditionList:
				conditionDict["(%i)"%condition.id] = condition.value
			role.client.CLIENT_StartSpaceStrategy( index ,strategy.getPackToString( self.getSpaceStrategyRewardDict(selfEntity,strategy,True),conditionDict,0 ) )

	def endStrategy( self, selfEntity, index ):
		"""
		结束某个策略点
		"""
		if index not in selfEntity.strategyOpenIndexList:
			KBEDebug.ERROR_MSG("This space has not open this strategyPoint(index = %i)"%index)
			return
		selfEntity.strategyOpenIndexList.remove(index)
		if index not in selfEntity.strategyEndIndexList:
			selfEntity.strategyEndIndexList.append(index)

		if index in self.strategyTimerKey.keys():
			timerID = self.strategyTimerKey.pop(index)
			selfEntity.popTimer( timerID )

		self.updateStrategy( selfEntity, index, 1)

	def firstCheckStrategyPoint( self, selfEntity, strategyIndex ):
		"""
		"""
		strategyPoint = None
		strategyType = self.getStrategyType(strategyIndex)
		if strategyType == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
			strategyPoint = self.getSpaceStrategyPoint(strategyIndex)
		else:
			if len(selfEntity._spaceRoles):
				strategyPoint = self.getRoleStrategyPoint(selfEntity._spaceRoles[0].playerDBID, strategyIndex)
		if strategyPoint == None:
			return
		self.checkStrategyPoint( selfEntity,strategyPoint )
		timerID = selfEntity.addTimerRepeatForScript(STRATEGY_POINT_TIME_TYPE,"checkStrategyPoint",(strategyPoint,))
		self.strategyTimerKey[strategyPoint.index] = timerID

	def checkStrategyPoint( self, selfEntity, strategyPoint ):
		"""
		检查时间类型的策略点
		"""
		tempDict = {}
		
		tempDict["*"] = strategyPoint.getValue()
		for role in selfEntity._spaceRoles:
			role.client.CLIENT_OnUpdateStrategyValue( strategyPoint.index,"*", strategyPoint.getValue()) #"*"标识 代表策略点的值
		grade,upper,lower= strategyPoint.getRewardGarade(True)
		if not strategyPoint.isSameToCurrentGrade(grade):
			for roleCell in selfEntity._spaceRoles:
				roleCell.client.CLIENT_OnUpdateStrategyValue( strategyPoint.index,"?", upper)
				if strategyPoint.describe.count("#"):
					roleCell.client.CLIENT_OnUpdateStrategyValue( strategyPoint.index,"#", lower)
				self.updateRewardValueToClient( selfEntity, roleCell, strategyPoint )

	def updateStrategy( self, selfEntity, index, isEnd = 0 ):
		"""
		更新某个策略点
		isEnd用于判断该策略点是否结束
		"""
		strategyType = self.getStrategyType(index)
		if strategyType == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
			strategyPoint = self.getSpaceStrategyPoint(index)
			if strategyPoint.getType() == Define.SPACE_STRATEGYPOINT_TIME and isEnd:
				strategyPoint.setEndTime( time.time() )
			for role in selfEntity._spaceRoles:
				self.updateStrateToClient( selfEntity,role, strategyPoint, isEnd )
		elif strategyType in[Define.SPACE_STRATEGYPOINT_BELONG_PERSON,Define.SPACE_STRATEGYPOINT_BELONG_TEAM]:
			for role in selfEntity._spaceRoles:
				strategyPoint = self.getRoleStrategyPoint( role.playerDBID, index )
				if strategyPoint.getType() == Define.SPACE_STRATEGYPOINT_TIME and isEnd:
					strategyPoint.setEndTime( time.time() )
				self.updateStrateToClient(selfEntity, role, strategyPoint, isEnd )

	def updateStrateToClient( self, selfEntity, roleCell ,strategyPoint, isEnd = 0 ):
		"""
		更新策略点到客户端
		"""
		rewardValue = 0
		passCondition = True
		conditionList = self.getStrategyPointAllCondition(roleCell.playerDBID,strategyPoint.index)
		for condition in conditionList:
			if not condition.isCompleted():
				passCondition = False
		if isEnd and passCondition:
			isSuccess = self.tryToReward(selfEntity,roleCell,strategyPoint)
			strategyPoint.setIsReward( True )
			strategyPoint.setIsSuccess( isSuccess )
			if self.getStrategyType(strategyPoint.index) == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
				if strategyPoint.index in self.recordSpaceStrategyPointReward:
					self.recordSpaceStrategyPointReward[strategyPoint.index].append(roleCell.playerDBID)
				else:
					self.recordSpaceStrategyPointReward[strategyPoint.index] = [roleCell.playerDBID]
		if isEnd:
			isSuccess = int(strategyPoint.isSuccess)
			roleCell.client.CLIENT_EndSpaceStrategy( strategyPoint.index, isSuccess)
		else: 
			if strategyPoint.getType() == Define.SPACE_STRATEGYPOINT_TIME: #注意时间类型的策略点不走这里  走checkStrategyPoint
				return
			roleCell.client.CLIENT_OnUpdateStrategyValue( strategyPoint.index, "*",strategyPoint.value ) #"*"标识 代表策略点的值
			grade, upper,lower= strategyPoint.getRewardGarade(True)
			if not strategyPoint.isSameToCurrentGrade(grade):
				roleCell.client.CLIENT_OnUpdateStrategyValue( strategyPoint.index,"?", upper)
				if strategyPoint.describe.count("#"):
					roleCell.client.CLIENT_OnUpdateStrategyValue( strategyPoint.index,"#", lower)
				self.updateRewardValueToClient( selfEntity, roleCell, strategyPoint )

	def getStrategyType( self, index ):
		"""
		获得策略点的类型
		"""
		return self.strategyPointTypeDict.get(index, 0)

	def getSpaceStrategyPoint( self, index ):
		"""
		获得副本策略点
		"""
		for strategy in self.spaceStrategyPointList:
			if strategy.index == index:
				return strategy
		return None

	def getRoleStrategyPoint( self, roleDBID, index ):
		"""
		获得玩家某一策略点
		"""
		if roleDBID in self.roleStrategyPointDict:
			strategyList = self.roleStrategyPointDict[roleDBID]
			for strategy in strategyList:
				if strategy.index == index:
					return strategy
		return None

	def getSpaceStrategyCondition( self, index, condID ):
		"""
		获得副本策略点条件
		"""
		if index in self.spaceStrategyPointConditons:
			conditions = self.spaceStrategyPointConditons[index]
			for condition in conditions:
				if condID == condition.id:
					return condition
		return []

	def getRoleStrategyCondtion( self, roleDBID, index, condID ):
		"""
		获得玩家某个策略点的所有条件
		index:策略点ID
		condID:条件ID
		rolePointConfitionDict {DBID:{策略点ID:[条件1，条件2]}}
		"""
		if roleDBID not in self.rolePointConfitionDict:
			return None
		if index not in self.rolePointConfitionDict[roleDBID]:
			return None
		conditions = self.rolePointConfitionDict[roleDBID][index]
		for condition in conditions:
			if condition.id == condID:
				return condition

	def getStrategyPointAllCondition( self, roleDBID, index ):
		"""
		获得策略点的所有条件
		"""
		conditionList = []
		if index in self.spaceStrategyPointConditons:
			conditionList.extend(self.spaceStrategyPointConditons[index])
		if roleDBID in self.rolePointConfitionDict:
			if index in self.rolePointConfitionDict[roleDBID]:
				conditionList.extend( self.rolePointConfitionDict[roleDBID][index] )
		return conditionList

	def getStrategyPointConditionDict( self, index ):
		"""
		获得该策略点下的所有条件 ID:条件归属类型
		"""
		return self.strategyCondTypeDict[index]

	def synchronousTeamStrategyData( self, selfEntity, roleCell, indexList ):
		"""
		同步下策略点归属类型为队伍的数据
		indexList 需要的同步的策略点index
		"""
		if len(indexList) <= 0:
			return
		mbList = roleCell.getAllTeamMemberMB()
		if not mbList:
			return
		mbIDList = []
		for mb in mbList:
			mbIDList.append(mb.id)
		for role in selfEntity._spaceRoles:
			if role.id in mbIDList and role.id != roleCell.id: #随机取副本中的一名队友除了自己	
				for index in indexList:
					if index in selfEntity.strategyOpenIndexList or index in selfEntity.strategyEndIndexList:
						strategyPoint = self.getRoleStrategyPoint( role.playerDBID, index )
						scrStrategyPoint = self.getRoleStrategyPoint( roleCell.playerDBID, index )
						scrStrategyPoint.value = strategyPoint.getValue()
						scrStrategyPoint.rewardValue = strategyPoint.rewardValue
						if scrStrategyPoint.getType() == Define.SPACE_STRATEGYPOINT_TIME:
							scrStrategyPoint.startTime = strategyPoint.startTime
							scrStrategyPoint.endTime = strategyPoint.endTime
				break

	def synchronousTeamConditionData( self, selfEntity, roleCell, conditionDict ):
		"""
		同步下策略点条件归属类型为队伍的数据
		conditionDict #{策略点ID:[条件ID,条件ID]}
		"""
		if len( conditionDict ) <= 0:
			return
		mbList = roleCell.getAllTeamMemberMB()
		if not mbList:
			return	
		mbIDList = []
		for mb in mbList:
			mbIDList.append(mb.id)

		for role in selfEntity._spaceRoles:
			if role.id in mbIDList and role.id != roleCell.id: #随机取副本中的一名队友除了自己	
				for index, condIDList in conditionDict.items():
					if index in selfEntity.strategyOpenIndexList or index in selfEntity.strategyEndIndexList:
						for condID in condIDList:
							dstCondition = self.getRoleStrategyCondtion( role.playerDBID, index, condID )
							srcCondition = self.getRoleStrategyCondtion( roleCell.playerDBID, index, condID )
							if dstCondition and srcCondition:
								srcCondition.value = dstCondition.value
				break

	def updateEndStrategyToClient( self,selfEntity, roleCell ,strategyPoint ):
		"""
		更新已完成的策略点到客户端 并且给奖励
		"""
		isReward = True
		if self.getStrategyType(strategyPoint.index) == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
			if strategyPoint.index in self.recordSpaceStrategyPointReward:
				rewardRecordList = self.recordSpaceStrategyPointReward[strategyPoint.index]
				if roleCell.playerDBID not in rewardRecordList:
					self.recordSpaceStrategyPointReward[strategyPoint.index].append(roleCell.playerDBID)
					isReward = False
		elif self.getStrategyType(strategyPoint.index) == Define.SPACE_STRATEGYPOINT_BELONG_TEAM:
			 if strategyPoint.isReward:
			 	isReward = False
		if not isReward:
			isSuccess = self.tryToReward( selfEntity, roleCell, strategyPoint )
			strategyPoint.setIsReward(True)
			strategyPoint.setIsSuccess( isSuccess )
		
		conditionDict = {}
		conditionList = self.getStrategyPointAllCondition( roleCell.playerDBID, strategyPoint.index )
		for condition in conditionList:
			conditionDict["(%i)"%condition.id] = condition.value
		roleCell.client.CLIENT_ReceiveCompleteSpaceStrategy( strategyPoint.index, strategyPoint.getPackToString( self.getSpaceStrategyRewardDict(selfEntity,strategyPoint,True),conditionDict,1 ) )

	def updateOpenStrateToClient( self,selfEntity, roleCell ,strategyPoint ):
		"""
		更新正在开始的策略点到客户端 并且给奖励
		"""
		conditionDict = {}
		conditionList = self.getStrategyPointAllCondition( roleCell.playerDBID, strategyPoint.index )
		for condition in conditionList:
			conditionDict["(%i)"%condition.id] = condition.value
		roleCell.client.CLIENT_ReceiveOpenSpaceStrategy( strategyPoint.index, strategyPoint.getPackToString( self.getSpaceStrategyRewardDict( selfEntity, strategyPoint,True ), conditionDict,0) )

	def updateStrategyConditionToClient( self, selfEntity, roleCell, index,condObj ):
		"""
		更新条件数据到客户端
		"""
		roleCell.client.CLIENT_OnUpdateStrategyValue( index, "(%i)"%condObj.id,condObj.value )

#----这里奖励类型直接根据SpaceStrategyGrade配置来的，而且每个策略点只有一种类型的奖励，并且跟策划了解奖励类型不会有太多种，所以奖励直接在tryToReward接口中写的-----
	def tryToReward( self, selfEntity, player, strategyPoint ):
		"""
		给与奖励
		"""
		rewardDict = self.getSpaceStrategyRewardDict( selfEntity, strategyPoint, False )
		if not rewardDict:
			return False
		for rewardType, rewardValue in rewardDict.items():
			if rewardType == STRATEGY_REWARD_TYPE_EXP:
				player.addExp(rewardValue,csdefine.EXP_ADD_REASON_SPACE_STRATEGYPOINT)
			if rewardType == STRATEGY_REWARD_TYPE_POTENTIAL:
				player.addPotential( rewardValue, csdefine.POTENTIAL_ADD_REASON_STRATEGY_POINT )
			if rewardType == STRATEGY_REWARD_TYPE_CONTRIBUTION:
				if player.tongMB:
					player.tongMB.addContribution( player.playerDBID,rewardValue )
		return True

	def getSpaceStrategyRewardDict( self, selfEntity, strategyPoint, isUseToShow ):
		"""
		获得策略点奖励类型和奖励值 {奖励类型：奖励值}
		"""
		if selfEntity.scriptID not in SpaceStrategyGrade.Datas:
			return {}
		pointGradeDict = SpaceStrategyGrade.Datas[selfEntity.scriptID]
		if strategyPoint.index not in pointGradeDict:
			return {}
		grade,upper,lower = strategyPoint.getRewardGarade(isUseToShow)
		pointGrades = pointGradeDict[strategyPoint.index]
		if grade not in pointGrades:
			return {}
		valueDict = pointGrades[grade]
		rewardDict = {}
		if valueDict["expRatio"] > 0.0:
			expBase = RewardBase.datas[selfEntity.spaceLevel]["exp"]
			value = int(expBase * valueDict["expRatio"])
			rewardDict[STRATEGY_REWARD_TYPE_EXP] = value
		if valueDict["potentialRatio"] > 0.0:
			potentialBase = RewardBase.datas[selfEntity.spaceLevel]["potential"]
			value = int( potentialBase * valueDict["potentialRatio"] )
			rewardDict[STRATEGY_REWARD_TYPE_POTENTIAL] = value
		if valueDict["contributionRatio"] > 0.0:
			contributionBase = RewardBase.datas[selfEntity.spaceLevel]["contribution"]
			value = int( contributionBase * valueDict["contributionRatio"] )
			rewardDict[STRATEGY_REWARD_TYPE_CONTRIBUTION] = value
		return rewardDict

	def updateRewardValueToClient( self, selfEntity, roleCell, strategyPoint ):
		"""
		"""
		rewardDict = self.getSpaceStrategyRewardDict( selfEntity, strategyPoint,True )
		for rewardType, rewardValue in rewardDict.items():
			roleCell.client.CLIENT_OnUpdateRewardValue( strategyPoint.index, rewardType, rewardValue )

#---------------------------------玩家的策略点相关( 虽说是由玩家触发的，但策略点都可以配置成 个人、影响队伍、副本，所以在加时请考虑策略点适用性 )--------------------------------------------------						
	def spaceStrategy_onRoleAddBuff( self, selfEntity, roleCell, buffID ):
		"""
		玩家增加Buff
		"""
		for index in selfEntity.strategyOpenIndexList:
			if self.getStrategyType(index) == Define.SPACE_STRATEGYPOINT_BELONG_PERSON:
				self.onInfluenceRoleAddBuff( selfEntity, roleCell, index, buffID )
			elif self.getStrategyType(index) == Define.SPACE_STRATEGYPOINT_BELONG_TEAM:
				for mb in roleCell.getAllTeamMemberMB():
					player = KBEngine.entities.get( mb.id, None )
					if player:
						self.onInfluenceRoleAddBuff( selfEntity, player, index, buffID )

			conditionDict = self.getStrategyPointConditionDict(index)
			for condID, condBelongType in conditionDict.items():
				if condBelongType == Define.SPACE_STRATEGYPOINT_CONDITION_BELONG_PERSON:
					self.onInfluenceConditonRoleAddBuff( selfEntity, roleCell, index, condID,buffID )

				elif condBelongType == Define.SPACE_STRATEGYPOINT_CONDITION_BELONG_TEAM:
					for mb in roleCell.getAllTeamMemberMB():
						player = KBEngine.entities.get( mb.id, None )
						if player:
							self.onInfluenceConditonRoleAddBuff( selfEntity, player, index, condID,buffID )

	def onInfluenceRoleAddBuff(  self, selfEntity, roleCell, index, buffID ):
		"""
		某个玩家增加Buff
		"""
		strategyPoint = self.getRoleStrategyPoint( roleCell.playerDBID, index )
		if strategyPoint.getType() != Define.SPACE_STRATEGYPOINT_ROLE_ADDBUFF:
			return
		if not strategyPoint.checkBuffID(buffID):
			return
		if strategyPoint.increaseVal(1):
			if strategyPoint.isUpdate:
				self.updateStrateToClient( selfEntity,roleCell, strategyPoint )

	def onInfluenceConditonRoleAddBuff( self, selfEntity, roleCell, index, condID, buffID ):
		"""
		某个玩家增加Buff
		"""
		condObj = self.getRoleStrategyCondtion(roleCell.playerDBID,index,condID)
		if not condObj:
			return
		if condObj.getType() != Define.SPACE_STRATEGYPOINT_CONDITION_ROLE_ADDBUFF:
			return
		if not condObj.checkBuffID( buffID):
			return
		if condObj.increaseVal(1):
			self.updateStrategyConditionToClient( selfEntity, roleCell, index, condObj )

	def spaceStrategy_onRoleReceiveDamage( self, selfEntity, roleCell, casterID ):
		"""
		玩家受到伤害
		"""
		for index in selfEntity.strategyOpenIndexList:
			if self.getStrategyType(index) != Define.SPACE_STRATEGYPOINT_BELONG_PERSON:
				continue
			strategyPoint = self.getRoleStrategyPoint( roleCell.playerDBID, index )
			if strategyPoint.getType() != Define.SPACE_STRATEGYPOINT_ROLE_RECEIVEDAMAGE:
				continue
			if not strategyPoint.checkScriptID(casterID):
				continue
			if strategyPoint.increaseVal(1):
				if strategyPoint.isUpdate:
					self.updateStrateToClient( selfEntity,roleCell, strategyPoint )
		

	def spaceStrategy_onRoleTriggerBox( self, selfEntity, roleCell, boxScriptID ):
		"""
		箱子被触发
		"""
		for index in selfEntity.strategyOpenIndexList:
			if self.getStrategyType(index) == Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
				self.onInfluenceSpaceTriggerBox(selfEntity,index,boxScriptID)
			elif self.getStrategyType(index) == Define.SPACE_STRATEGYPOINT_BELONG_PERSON:
				self.onInfluenceRoleTriggerBox( selfEntity, roleCell,index,boxScriptID )
			elif self.getStrategyType(index) == Define.SPACE_STRATEGYPOINT_BELONG_TEAM:
				for mb in roleCell.getAllTeamMemberMB():
					player = KBEngine.entities.get( mb.id, None )
					if player:
						self.onInfluenceRoleTriggerBox( selfEntity,player,index,boxScriptID )

	def onInfluenceSpaceTriggerBox( self, selfEntity,index, boxScriptID ):
		"""
		箱子被触发影响副本策略点
		"""
		strategyPoint = self.getSpaceStrategyPoint(index)
		if strategyPoint.getType() != Define.SPACE_STRATEGYPOINT_TRIGGER_BOX:
			return
		if not strategyPoint.checkBoxScriptID(boxScriptID):
			return
		if strategyPoint.increaseVal(1):
			if strategyPoint.isUpdate:
				for role in selfEntity._spaceRoles:
					self.updateStrateToClient(selfEntity,role, strategyPoint)

	def onInfluenceRoleTriggerBox( self, selfEntity,roleCell, index, boxScriptID ):
		"""
		箱子被触发影响玩家策略点
		"""	
		strategyPoint = self.getRoleStrategyPoint(roleCell.playerDBID,index)
		if strategyPoint.getType() != Define.SPACE_STRATEGYPOINT_TRIGGER_BOX:
			return
		if not strategyPoint.checkBoxScriptID(boxScriptID):
			return
		if strategyPoint.increaseVal(1):
			if strategyPoint.isUpdate:
				self.updateStrateToClient( selfEntity,roleCell, strategyPoint )

#------------------------------副本策略点相关-----------------------------------
	def spaceStrategy_onMonsterDie( self, selfEntity, monsterScriptID ):
		"""
		怪物死亡
		"""
		for index in selfEntity.strategyOpenIndexList:
			if self.getStrategyType(index) != Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
				continue
			strategyPoint = self.getSpaceStrategyPoint(index)
			if strategyPoint.getType() != Define.SPACE_STRATEGYPOINT_KILLMONSTER:
				continue
			if not strategyPoint.checkScriptID( monsterScriptID ):
				continue
			if strategyPoint.increaseVal(1):
				if strategyPoint.isUpdate:
					for roleCell in selfEntity._spaceRoles:
						self.updateStrateToClient( selfEntity,roleCell, strategyPoint )

		for index in selfEntity.strategyOpenIndexList:
			conditionDict = self.getStrategyPointConditionDict(index)
			for condID, condBelongType in conditionDict.items():
				if condBelongType != Define.SPACE_STRATEGYPOINT_CONDITION_BELONG_SPACE:
					continue
				condObj = self.getSpaceStrategyCondition(index,condID)
				if not condObj:
					continue
				if condObj.getType() != Define.SPACE_STRATEGYPOINT_CONDITION_KILLMONSTER:
					continue
				if not condObj.checkScriptID( monsterScriptID ):
					continue
				if condObj.increaseVal(1):
					for roleCell in selfEntity._spaceRoles:
						self.updateStrategyConditionToClient( selfEntity, roleCell, index,condObj )

	def spaceStrategy_onMonsterHPChanged( self, selfEntity, monsterEntity ):
		"""
		怪物血量改变
		"""
		for index in selfEntity.strategyOpenIndexList:
			if self.getStrategyType(index) != Define.SPACE_STRATEGYPOINT_BELONG_SPACE:
				continue
			strategyPoint = self.getSpaceStrategyPoint(index)
			if strategyPoint.getType() != Define.SPACE_STRATEGYPOINT_MONSTER_HP_CHANGED:
				continue
			if not strategyPoint.checkMonsterHP( monsterEntity ):
				continue
			if strategyPoint.increaseVal(1):
				if strategyPoint.isUpdate:
					for roleCell in selfEntity._spaceRoles:
						self.updateStrateToClient( selfEntity,roleCell, strategyPoint )


