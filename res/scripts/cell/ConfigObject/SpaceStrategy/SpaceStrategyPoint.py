# -*- coding: utf-8 -*-

# 副本策略点

import SpaceStrategyDataType
import Define
import time
import json
import KBEngine
import csdefine
import KBEDebug

class SpaceStrategyPointBase( SpaceStrategyDataType.SpaceStrategyDataType ):
	type = Define.SPACE_STRATEGYPOINT_NONE
	
	def __init__( self ):
		SpaceStrategyDataType.SpaceStrategyDataType.__init__( self )
		self.index = 0
		self.value = 0
		self.pointBelongType = Define.SPACE_STRATEGYPOINT_BELONG_NONE #策略点归属类型
		self.describe = ""
		self.param1 = ""
		self.param2 = ""
		self.param3 = ""
		self.isUpdate = True  #用于是否实时更新
		self.rewardValue = 0
		self.isReward = False  #是否发放奖励
		self.rewardGrade = ""
		self.currentGrade = 0
		self.isSuccess = False #是否成功
		
	def init( self, index, datas ):
		self.index = index
		self.describe = datas["describe"]
		self.value = datas["value"]
		self.pointBelongType = datas["pointBelongType"]
		self.param1 = datas["param1"]
		self.param2 = datas["param2"]
		self.param3 = datas["param3"]
		self.rewardGrade = datas["rewardGrade"] # 1:0-180|2:181-300|3:301-360 档次:最低值-最大值
		if self.getRewardGarade(True):
			self.currentGrade = self.getRewardGarade(True)[0]

	def getRewardGarade( self, isUseToShow ):
		"""
		获得该策略点奖励档次 返回"(奖励档次,最大值)"
		isUseToShow 是否用于客户端显示
		YES:如果超过最大值  就显示最大值和当前档次的奖励
		NO:用于给玩家奖励 不在任何档次中就无奖励
		"""
		rewardGradeList = self.rewardGrade.split("|")
		rewardGradeDict = {}
		for rewardGrade in rewardGradeList:
			rewardGradeDict[int(rewardGrade.split(":")[0])] = rewardGrade.split(":")[1]

		curGrade = -1
		curLower = -1
		curUpper = -1
		curValue = self.getValue()
		lowerList = []
		upperList = []
		isFindLower = False
		isFindUpper = False
		for grade,value in rewardGradeDict.items():
			lower = int(value.split("-")[0])
			upper = int(value.split("-")[1])
			lowerList.append(lower)
			upperList.append(upper)
		for grade,value in rewardGradeDict.items():
			lower = int(value.split("-")[0])
			upper = int(value.split("-")[1])
			if curValue >= lower and curValue <= upper:
				curGrade = grade
				curUpper = int(value.split("-")[1])
				isFindUpper = True
			if curValue > lower:
				index = lowerList.index(lower)
				if len(lowerList) > index + 1:
					curLower = lowerList[index + 1]
					isFindLower = True

			if isFindLower and isFindUpper:
				break

		if not isUseToShow:
			return (curGrade,curUpper,curLower)
		if curLower == -1 or curUpper == -1:
			maxUpper = max(upperList)
			if curValue > maxUpper:
				curLower = max(lowerList)
				curUpper = max(upperList)
			else:
				curLower = min(lowerList)
				curUpper = min(upperList)
			tempStr = "%i-%i"%(curLower,curUpper)
			for grade,value in rewardGradeDict.items():
				if value == tempStr:
					curGrade = grade
					break
		return (grade,curUpper,curLower)

	def isSameToCurrentGrade( self, grade ):
		"""
		是否为该档次
		"""
		if grade == self.currentGrade:
			return True
		self.currentGrade = grade
		return False

	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_NONE

	def getValue( self ):
		return self.value

	def increaseVal( self, value ):
		if value == 0:
			return False
		
		self.value += value
		return True

	def decreaseVal( self, value ):
		if value == 0:
			return False
		
		if self.value == 0:
			return False
		
		self.value = max( 0, self.value - value )
		return True

	def setIsReward( self, isReward ):
		self.isReward = isReward

	def setIsSuccess( self, isSuccess ):
		self.isSuccess = isSuccess

	def getPackToString( self, rewardDict,conditionDict,isEnd = 0 ):
		"""
		打包数据
		传isEnd 让客户端通过这个判断该策略点是否结束
		conditionDict 数据 {(条件ID):值,(条件ID):值}
		rewardDict {奖励类型：奖励值}
		("*":策略点值，"?":策略点上限值，"#":策略点下限值,"(1)":条件1值，"(2)":条件2值)
		"""
		tempDict = {}
		tempDict["index"] =  self.index
		tempDict["describe"] = self.describe
		tempDict["valueMap"] = {}
		tempDict["valueMap"]["?"] = self.getRewardGarade(True)[1]
		if self.describe.count("#"):
			tempDict["valueMap"]["#"] = self.getRewardGarade(True)[2]
		tempDict["valueMap"]["*"] = self.getValue()
		tempDict["valueMap"].update(conditionDict)
		tempDict["isEnd"] = isEnd
		tempDict["rewardDict"] = rewardDict
		tempDict["isSuccess"] = int(self.isSuccess)
		tempDict["IsTimeType"] = int(self.getType() == Define.SPACE_STRATEGYPOINT_TIME)
		return json.dumps(tempDict)

class SStrategy_onRoleAddBuff( SpaceStrategyPointBase ):
	"""
	玩家增加Buff
	"""
	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_ROLE_ADDBUFF

	def checkBuffID( self, buffID ):
		buffIDList = [int(i) for i in self.param1.split("|")]
		return buffID in buffIDList

class SStrategy_onKillMonster( SpaceStrategyPointBase ):
	"""
	杀怪
	"""
	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_KILLMONSTER

	def checkScriptID( self, scriptID ):
		scriptIDList = self.param1.split("|")
		return scriptID in scriptIDList

class SStrategy_onTriggerBox( SpaceStrategyPointBase ):
	"""
	触发箱子
	"""
	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_TRIGGER_BOX

	def checkBoxScriptID( self, scriptID ):
		scriptIDList = self.param1.split("|")
		return scriptID in scriptIDList


class SStrategy_onMonsterHPChange( SpaceStrategyPointBase ):
	"""
	怪物血量改变
	"""
	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_MONSTER_HP_CHANGED

	def checkMonsterHP( self, monsterEntity ):
		if self.param1 != monsterEntity.scriptID:
			return False
		return float( monsterEntity.HP ) /monsterEntity.HP_Max < float(self.param2)

class SStrategy_onRoleReceiveDamage( SpaceStrategyPointBase ):
	"""
	玩家受到伤害
	"""
	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_ROLE_RECEIVEDAMAGE

	def checkScriptID( self, casterID ):
		entity = KBEngine.entities.get(casterID)
		scriptIDList = self.param1.split("|")
		if entity:
			if entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				return False
			return entity.scriptID in scriptIDList

class SStrategy_onTime( SpaceStrategyPointBase ):
	"""
	计时
	"""
	def __init__( self ):
		SpaceStrategyPointBase.__init__( self )
		self.startTime = 0.0
		self.endTime = 0.0

	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_TIME

	def setStartTime( self, time ):
		"""
		设置开始时间
		"""
		self.startTime = time

	def setEndTime( self, time ):
		"""
		设置结束时间
		"""
		self.endTime = time

	def getValue( self ):
		if self.isReward:
			self.value = int(round(self.endTime - self.startTime))
		else:
			self.value = int(round(time.time() - self.startTime))
		return self.value

SpaceStrategyDataType.MAP_STRATEGY_TYPE_TO_STRATEGY_CLASS( Define.SPACE_STRATEGYPOINT_ROLE_ADDBUFF, SStrategy_onRoleAddBuff )
SpaceStrategyDataType.MAP_STRATEGY_TYPE_TO_STRATEGY_CLASS( Define.SPACE_STRATEGYPOINT_KILLMONSTER, SStrategy_onKillMonster )
SpaceStrategyDataType.MAP_STRATEGY_TYPE_TO_STRATEGY_CLASS( Define.SPACE_STRATEGYPOINT_TRIGGER_BOX, SStrategy_onTriggerBox )
SpaceStrategyDataType.MAP_STRATEGY_TYPE_TO_STRATEGY_CLASS( Define.SPACE_STRATEGYPOINT_MONSTER_HP_CHANGED,SStrategy_onMonsterHPChange )
SpaceStrategyDataType.MAP_STRATEGY_TYPE_TO_STRATEGY_CLASS( Define.SPACE_STRATEGYPOINT_ROLE_RECEIVEDAMAGE,SStrategy_onRoleReceiveDamage )
SpaceStrategyDataType.MAP_STRATEGY_TYPE_TO_STRATEGY_CLASS( Define.SPACE_STRATEGYPOINT_TIME,SStrategy_onTime )
