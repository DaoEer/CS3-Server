# -*- coding- : utf-8 -*-

import random
import KBEngine
import KBEDebug
import csdefine
import math
from Reward import RewardBasicValueData
from Reward import RewardEquipData
from Reward import RewardQuestData
from ConfigObject.SpaceCopyQianNengLoopRewardLoader import g_SpaceCopyQianNengRewardsLoader

blDataType = {
	csdefine.REWARD_TYPE_EXP_BL: csdefine.REWARD_TYPE_EXP,	# 一倍基准经验
	csdefine.REWARD_TYPE_POTENTIAL_BL: csdefine.REWARD_TYPE_POTENTIAL,	# 一倍基准潜能
	csdefine.REWARD_TYPE_XIUWEI_BL: csdefine.REWARD_TYPE_XIUWEI,	# 一倍基准修为
	csdefine.REWARD_TYPE_MONEY_BL: csdefine.REWARD_TYPE_MONEY,	# 一倍基准金钱
	csdefine.REWARD_TYPE_BINDMONEY_BL : csdefine.REWARD_TYPE_BINDMONEY	#一倍基准绑金
	}

REWARD_ENTITY_TYPE_PLAYER		= "player"		#玩家
REWARD_ENTITY_TYPE_DIE			= "dieEntity" 	#击杀对象
REWARD_ENTITY_TYPE_GIFT			= "gift"		#礼包
REWARD_ENTITY_TYPE_OWNERLIST	= "ownerList"	#礼包
REWARD_ENTITY_TYPE_RATIO		= "ratio" 		#道具奖励系数
REWARD_ENTITY_TYPE_SPACE_LEVEL  = "spaceLevel" 	#副本等级

REWARD_TYPE_TONG_LEVEL			= "tongLevel"	#帮会等级

#GM命令调试奖励
DEBUG_REWARD_CON = "screenCon"
weightRandomNum = []
rateRandomNum = []
tmpSelectList = []
tmpRewardList = []


def isDebugingReward():
	return KBEngine.cellAppData.get("DEBUG_REWARD_FLG", None)


def writeRewardInfosToLogFile(type, datas, rewardAmount, rewardSelected, parentRewardID, randomNumList, screenCon):
	if not isDebugingReward():
		return

	tmpWeightList, tmpRateList = getWeightAndRate(datas)

	writeInfosToLogFile(type, datas, tmpWeightList, tmpRateList, rewardAmount, rewardSelected, parentRewardID, randomNumList,screenCon)


def getWeightAndRate(listDatas):
	rateLists = []
	weightLists = []
	weightSum = 0

	for i in range(len(listDatas)):
		data = listDatas[i]
		if data["weight"] == "":
			continue
		weight = float(data["weight"])
		weightLists.append(weight)
		weightSum += weight

	for i in range(len(weightLists)):
		rate = format(weightLists[i] / weightSum, '.2f')
		rateLists.append(rate)

	return weightLists, rateLists


def writeInfosToLogFile(type, listDatas, weightLists, rateLists, rewardAmount, rewardSelected, parentRewardID, randomNumList, screenCon):
	if not listDatas:
		clearDebugCache()
		KBEDebug.DEBUG_MSG_FOR_REWARD("Can not find content of gift({}) of RewardData.py, screen condition is {}!".format(parentRewardID, screenCon))
		return

	KBEDebug.DEBUG_MSG_FOR_REWARD("The num of getting reward in this time is {}：".format(rewardAmount))
	KBEDebug.DEBUG_MSG_FOR_REWARD("Get child reward({}) by {}".format(parentRewardID, screenCon))
	if type == 1: #权重
		if not rewardSelected:
			KBEDebug.DEBUG_MSG_FOR_REWARD("Final reward is Null!")
			return
		seletedDataLen = len(listDatas)
		rateListsLen = len(rateLists)
		for i in range(seletedDataLen):
			if i <= rateListsLen:
				infos = "type: %s,  goodsid: %s, amount: %s, weight: %s, rate: %s" % (
					listDatas[i]["type"], listDatas[i]["goodsid"], listDatas[i]["amount"], weightLists[i], rateLists[i])
				KBEDebug.DEBUG_MSG_FOR_REWARD(infos)

		for index, data in enumerate(rewardSelected):
			infos = "Selected type: %s,  goodsid: %s, amount: %s, random num: %.2f" % (
				data["type"], data["goodsid"], data["amount"], randomNumList[index])
			KBEDebug.DEBUG_MSG_FOR_REWARD(infos)
	elif type == 2: #概率
		seletedDataLen = len(listDatas)
		rateListsLen = len(randomNumList)
		for i in range(seletedDataLen):
			if i <= rateListsLen:
				infos = "type: %s,  goodsid: %s, amount: %s, weight: %s, rate: %s, random num: %.2f" % (
					listDatas[i]["type"], listDatas[i]["goodsid"], listDatas[i]["amount"], listDatas[i]["weight"], listDatas[i]["rate"], randomNumList[i])
				KBEDebug.DEBUG_MSG_FOR_REWARD(infos)

		if not rewardSelected:
			KBEDebug.DEBUG_MSG_FOR_REWARD("Not selected gift!")
			return
		else:
			for i in range(len(rewardSelected)):
				infos = "Selected type: %s,  goodsid: %s, amount: %s" % (
					rewardSelected[i]["type"], rewardSelected[i]["goodsid"], rewardSelected[i]["amount"])
				KBEDebug.DEBUG_MSG_FOR_REWARD(infos)

	clearDebugCache()


def clearDebugCache():
	weightRandomNum.clear()
	rateRandomNum.clear()
	tmpSelectList.clear()
	tmpRewardList.clear()

def getRewardForRate( rate ):
	"""
	基于概率生成奖励
	"""
	x = random.uniform(0,1)
	if isDebugingReward():
		rateRandomNum.append(x)
	if x <= rate:
		return True
	else:
		return False
		
def getRewardForWeight( rewardIndexs, weightList ):
	"""
	基于权重获取
	"""
	weightValue = 0
	sumWeight = 0
	for value in weightList:
		sumWeight += value
	x = random.uniform( 0, sumWeight )
	if isDebugingReward():
		weightRandomNum.append(x)

	for index, weight in zip( rewardIndexs, weightList ):
		weightValue += weight
		if x <= weightValue:
			return index
	return -1
	
class RewardRule( object ):
	"""
	奖励规则父类
	"""
	def __init__( self, configSection, data ):
		self._datas = configSection
		self._param1 = data["param1"].strip()
		self._param2 = data["param2"].strip()
		self._param3 = data.get( "param3","" )
		
	def extractReward( self, rewardData, level ):
		"""
		提取奖励需要的数据
		"""
		#return data: { "type":, "goodsid":"", "amount": 0 }
		type = rewardData["type"]
		reward = {}
		reward["type"] = type
		if type == csdefine.REWARD_TYPE_NOTHING:#空类型
			reward["goodsid"] = ""
			reward["amount"] = 0		
		elif type in blDataType:#如果是倍率类型，则换算成相应的数值类型
			reward["type"] = blDataType[ type ]
			reward["goodsid"] = rewardData["goodsid"]
			if level in RewardBasicValueData.datas:
				reward["amount"] = int( float( rewardData["amount"] ) * RewardBasicValueData.datas[ level ][ blDataType[type] ] )
			else:
				reward["amount"] = 0
		else:
			reward["goodsid"] = rewardData["goodsid"]
			reward["amount"] = int( rewardData["amount"] )
			
		return reward
		
class RewardForLevelToBasicValue( RewardRule ):
	"""
	根据等级获取基准倍率
	"""
	def __init__( self, configSection, data ):
		RewardRule.__init__(self, configSection, data )
	
	def fetch( self, args ):
		dieEntity = args[REWARD_ENTITY_TYPE_DIE]
		datas = RewardBasicValueData.datas
		valueData = {}
		valueData["exp"] = 0
		valueData["potential"] = 0
		valueData["xiuwei"] = 0
		valueData["money"] = 0
		valueData["tongMoney"] = 0
		valueData["feats"] = 0
		valueData["campMorale"] = self._datas["campMorale"]
		valueData["tongContribute"] = self._datas["tongContribute"]
		level = dieEntity.getLevel()
		if level in datas:
			blData =datas[ level ]
			if self._datas["expRate"]:
				spaceRate = 1.0
				spaceEntity = dieEntity.getCurrentSpace()
				if spaceEntity and spaceEntity.getScript().getBunchSpaceObj():
					index = spaceEntity.bunchStage - 1
					spaceRate = spaceEntity.getScript().getBunchSpaceObj().getReWardRateByIndex(index)
				valueData["exp"] = int( blData["exp"] * float( self._datas["expRate"] ) * spaceRate )
			if self._datas["potentialRate"]:
				#潜能副本 CST-11294
				spaceRate = 1.0
				spaceEntity = dieEntity.getCurrentSpace()
				if spaceEntity and spaceEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_POTENTIAL:
					player = args[ REWARD_ENTITY_TYPE_PLAYER ]
					if player.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
						loop, index = player.getPotentialSpaceLoopAndIndex()
						spaceRate = g_SpaceCopyQianNengRewardsLoader.getRewardRate(loop, index)
				valueData["potential"] = int( blData["potential"] * float( self._datas["potentialRate"] ) * spaceRate )
			if self._datas["xiuweiRate"]:
				valueData["xiuwei"] = int( blData["xiuwei"] * float( self._datas["xiuweiRate"] ) )
			
		return valueData

class RewardToWeight( RewardRule ):
	"""
	#获取一个权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardRule.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		level = 0
		number = 1
		if self._param1:
			number = int( self._param1 )
		tempData = []
		tempData.extend( self._datas )
		if REWARD_ENTITY_TYPE_PLAYER in args:
			player = args[ REWARD_ENTITY_TYPE_PLAYER ]
			level = player.getLevel()
		for i in range( number ):
			rewardIndexs = []
			weightList = []
			for j in range( len( tempData ) ):
				data = tempData[j]
				weight =data["weight"]
				if not weight.strip():
					continue
				rewardIndexs.append( j )
				weightList.append( float( weight ) )
			if rewardIndexs and weightList:
				index = getRewardForWeight( rewardIndexs, weightList )
				rewardList.append( self.extractReward( tempData[ index ], level ) )
				tempData.pop( index )

		writeRewardInfosToLogFile(1, self._datas, number, rewardList, rewardID, weightRandomNum, "RewardToWeight")
		return rewardList

class RewardForLevelToWeight( RewardToWeight ):
	"""
	根据等级生成权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToWeight.__init__( self, configSection, data )
			
	def doReward( self, level, rewardID = 0, conArgs = "No screen condition args"):
		"""
		执行生成奖励
		"""
		reward = None
		rewardIndexs = []
		weightList = []

		for i in range( len( self._datas ) ):
			data = self._datas[i]
			tempLevel =data["level"]
			if not tempLevel.strip() or int( tempLevel ) != level:
				continue
			weight =data["weight"]
			if not weight.strip():
				continue
			rewardIndexs.append( i )
			weightList.append( float( weight ) )
			tmpSelectList.append(data)

		if rewardIndexs and weightList:
			index = getRewardForWeight( rewardIndexs, weightList )
			reward = self.extractReward( self._datas[ index ], level )

		tmpRewardList.append(reward)
		writeRewardInfosToLogFile(1, tmpSelectList, 1 if not self._param1 else self._param1, tmpRewardList, rewardID, weightRandomNum, conArgs)
		return reward


class RewardForDieLevelToWeight( RewardForLevelToWeight ):
	"""
	#根据被击杀的对象等级获取权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardForLevelToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList =[]
		if isDebugingReward():
			level = args.get(DEBUG_REWARD_CON, 0)
		else:
			if self._param3 and int(self._param3) == 1:
				level = args.get(REWARD_ENTITY_TYPE_SPACE_LEVEL,0)
			else:
				dieEntity = args[ REWARD_ENTITY_TYPE_DIE ]
				level = dieEntity.level

		reward = self.doReward(level, rewardID, "RewardForDieLevelToWeight: level({})".format(level))
		if reward:
			rewardList.append( reward )
		return rewardList
	
class RewardForTongLevelToWeight( RewardForLevelToWeight ):
	"""
	#根据帮会等级获取权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardForLevelToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList =[]
		if isDebugingReward():
			level = args.get(DEBUG_REWARD_CON, 0)
		else:
			if REWARD_TYPE_TONG_LEVEL not in args:
				KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
				return rewardList

			level = args[REWARD_TYPE_TONG_LEVEL]
		reward = self.doReward(level, rewardID, "RewardForTongLevelToWeight: level({})".format(level))
		if reward:
			rewardList.append( reward )
		return rewardList


class RewardForRoleProfessionToWeight( RewardToWeight ):
	"""
	#根据触发奖励条件的玩家职业获取权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		rewardIndexs = []
		weightList = []
		if REWARD_ENTITY_TYPE_PLAYER not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		player = args[ REWARD_ENTITY_TYPE_PLAYER ]
		profession = player.profession
		for i in range( len( self._datas ) ):
			data = self._datas[i]
			tempProfession =data["profession"]
			if not tempProfession.strip() or int( tempProfession ) != profession:
				continue
			weight =data["weight"]
			if not weight.strip():
				continue
			rewardIndexs.append( i )
			weightList.append( float( weight ) )
			tmpSelectList.append(data)
		if rewardIndexs and weightList:
			index = getRewardForWeight( rewardIndexs, weightList )
			rewardList.append( self.extractReward( self._datas[ index ], player.getLevel() ) )

		writeRewardInfosToLogFile(1, tmpSelectList, 1 if not self._param1 else self._param1, rewardList, rewardID, weightRandomNum,
				"RewardForRoleProfessionToWeight: profession({})".format(profession))
		return rewardList


class RewardEquipForRLAndRPToWeight( RewardToWeight ):
	"""
	#根据触发奖励条件的玩家等级和职业获取权重随机奖励（param可配置指定品质或部位）
	"""
	def __init__( self, configSection, data ):
		RewardToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		rewardIndexs = []
		weightList = []
		if REWARD_ENTITY_TYPE_PLAYER not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		player = args[ REWARD_ENTITY_TYPE_PLAYER ]
		
		equipDatas = RewardEquipData.datas
		level = player.getLevel()
		profession = player.profession
		for i in range( len( equipDatas ) ):
			data = equipDatas[i]
			tempProfession =data["profession"]
			tempLevel = data["level"]
			if not tempLevel.strip() or int( tempLevel ) != level:
				continue
			if not tempProfession.strip() or int( tempProfession ) != profession:
				continue
			if self._param1 and self._param1 != data["quality"]:
				continue
			if self._param2 and self._param2 != data["eq_wieldType"]:
				continue
			weight =data["weight"]
			if not weight.strip():
				continue
			rewardIndexs.append( i )
			weightList.append( float( weight ) )
			tmpSelectList.append(data)
		if rewardIndexs and weightList:
			index = getRewardForWeight( rewardIndexs, weightList )
			rewardList.append( self.extractReward( equipDatas[ index ], level ) )

		selectCons = "RewardEquipForRLAndRPToWeight: level({}), profession({}), quality({}), eq_wieldType({})".format(level, profession, self._param1, self._param2)
		writeRewardInfosToLogFile(1, tmpSelectList, 1, rewardList, rewardID, weightRandomNum, selectCons)
		return rewardList

		
class RewardEquipForRLToWeight( RewardToWeight ):
	"""
	#根据触发奖励条件的玩家等级获取权重随机奖励（param可配置指定品质或部位）
	"""
	def __init__( self, configSection, data ):
		RewardToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		rewardIndexs = []
		weightList = []
		if REWARD_ENTITY_TYPE_PLAYER not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		player = args[ REWARD_ENTITY_TYPE_PLAYER ]
		
		equipDatas = RewardEquipData.datas
		level = player.getLevel()
		for i in range( len( equipDatas ) ):
			data = equipDatas[i]
			tempLevel = data["level"]
			if not tempLevel.strip() or int( tempLevel ) != level:
				continue
			if self._param1 and self._param1 != data["quality"]:
				continue
			if self._param2 and self._param2 != data["eq_wieldType"]:
				continue
			weight =data["weight"]
			if not weight.strip():
				continue
			rewardIndexs.append( i )
			weightList.append( float( weight ) )
			tmpSelectList.append(data)
		if rewardIndexs and weightList:
			index = getRewardForWeight( rewardIndexs, weightList )
			rewardList.append( self.extractReward( equipDatas[ index ], level ) )

		selectCons = "RewardEquipForRLToWeight: level({}), quality({}), eq_wieldType({})".format(level, self._param1, self._param2)
		writeRewardInfosToLogFile(1, tmpSelectList, 1, rewardList, rewardID, weightRandomNum, selectCons)
		return rewardList

class RewardForRoleLevelToWeight( RewardForLevelToWeight ):
	"""
	#根据触发奖励条件的玩家等级获取权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardForLevelToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if REWARD_ENTITY_TYPE_PLAYER not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		player = args[ REWARD_ENTITY_TYPE_PLAYER ]
		level = player.getLevel()
		reward = self.doReward(level, rewardID, "RewardForRoleLevelToWeight: level({})".format(level))
		if reward:
			rewardList.append( reward )
		return rewardList
		

class RewardForGiftLevelToWeight( RewardForLevelToWeight ):
	"""
	#根据礼包等级获取权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if isDebugingReward():
			level = args.get(DEBUG_REWARD_CON, 0)
		else:
			if REWARD_ENTITY_TYPE_GIFT not in args:
				KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
				return rewardList
			itemGift = args[ REWARD_ENTITY_TYPE_GIFT ]
			level = itemGift.getLevel()

		reward = self.doReward( level, rewardID, "RewardForGiftLevelToWeight: level({})".format(level) )
		if reward:
			rewardList.append( reward )
		return rewardList
		

class RewardForMonsterIDToWeight( RewardToWeight ):
	"""
	#根据怪物ID获取权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardIndexs = []
		weightList = []
		rewardList = []
		if isDebugingReward():
			scriptID = str(args.get(DEBUG_REWARD_CON, 0))
		else:
			if REWARD_ENTITY_TYPE_DIE not in args:
				KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
				return rewardList
			monster = args[ REWARD_ENTITY_TYPE_DIE ]
			scriptID = monster.getScriptID()
		for i in range( len( self._datas ) ):
			data = self._datas[i]
			tempID =data["scriptid"]
			if tempID != scriptID:
				continue
			weight =data["weight"]
			if not weight.strip():
				continue
			rewardIndexs.append( i )
			weightList.append( float( weight ) )
			tmpSelectList.append(data)
		if rewardIndexs and weightList:
			level = 0
			if REWARD_ENTITY_TYPE_PLAYER in args:
				player = args[ REWARD_ENTITY_TYPE_PLAYER ]
				level = player.getLevel()
			index = getRewardForWeight( rewardIndexs, weightList )
			rewardList.append( self.extractReward( self._datas[ index ], level ) )

		writeRewardInfosToLogFile(1, tmpSelectList, 1, rewardList, rewardID, weightRandomNum,
								  "RewardForMonsterIDToWeight: scriptID({})".format(scriptID))

		return rewardList
	
	
class RewardEquipForDieLevelToWeight( RewardToWeight ):
	"""
	#根据被击杀对象等级获取权重随机装备奖励
	"""
	def __init__( self, configSection, data ):
		RewardToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		rewardIndexs = []
		weightList = []
		if isDebugingReward():
			level = args.get(DEBUG_REWARD_CON, 0)
		else:
			if self._param3 and int(self._param3) == 1:
				level = args.get(REWARD_ENTITY_TYPE_SPACE_LEVEL,0)
			else:
				dieEntity = args[ REWARD_ENTITY_TYPE_DIE ]
				level = dieEntity.level
		equipDatas = RewardEquipData.datas
		for i in range( len( equipDatas ) ):
			data = equipDatas[i]
			tempLevel = data["level"]
			if not tempLevel.strip() or int( tempLevel ) != level:
				continue
			if self._param1 and self._param1 != data["quality"]:
				continue
			if self._param2 and self._param2 != data["eq_wieldType"]:
				continue
			weight =data["weight"]
			if not weight.strip():
				continue
			rewardIndexs.append( i )
			weightList.append( float( weight ) )
			tmpSelectList.append(data)
		if rewardIndexs and weightList:
			level = 0
			if REWARD_ENTITY_TYPE_PLAYER in args:
				player = args[ REWARD_ENTITY_TYPE_PLAYER ]
				level = player.getLevel()
			index = getRewardForWeight( rewardIndexs, weightList )
			rewardList.append( self.extractReward( equipDatas[ index ], level ) )

		selectCons = "RewardEquipForDieLevelToWeight: level({}), quality({}), eq_wieldType({})".format(level, self._param1, self._param2)
		writeRewardInfosToLogFile(1, tmpSelectList, 1, rewardList, rewardID, weightRandomNum, selectCons)
		return rewardList
		
class RewardEquipForDieLevelAndRPToWeight( RewardToWeight ):
	"""
	#根据被击杀对象等级和职业获取权重随机装备奖励
	"""
	def __init__( self, configSection, data ):
		RewardToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		rewardIndexs = []
		weightList = []
		if isDebugingReward():
			level = args.get(DEBUG_REWARD_CON, 0)
		else:
			if self._param3 and int(self._param3) == 1:
				level = args.get(REWARD_ENTITY_TYPE_SPACE_LEVEL,0)
			else:
				dieEntity = args[ REWARD_ENTITY_TYPE_DIE ]
				level = dieEntity.level

			if REWARD_ENTITY_TYPE_PLAYER not in args:
				KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
				return rewardList
		
		player = args[ REWARD_ENTITY_TYPE_PLAYER ]
		profession = player.profession
		equipDatas = RewardEquipData.datas
		for i in range( len( equipDatas ) ):
			data = equipDatas[i]
			tempLevel = data["level"]
			tempProfession =data["profession"]
			
			if not tempLevel.strip() or int( tempLevel ) != level:
				continue
			if not tempProfession.strip() or int( tempProfession ) != profession:
				continue
			if self._param1 and self._param1 != data["quality"]:
				continue
			if self._param2 and self._param2 != data["eq_wieldType"]:
				continue
			weight =data["weight"]
			if not weight.strip():
				continue
			rewardIndexs.append( i )
			weightList.append( float( weight ) )
			tmpSelectList.append(data)
		if rewardIndexs and weightList:
			level = player.getLevel()
			index = getRewardForWeight( rewardIndexs, weightList )
			rewardList.append( self.extractReward( equipDatas[ index ], level ) )

		selectCons = "RewardEquipForDieLevelAndRPToWeight: level({}), quality({}), profession({}), eq_wieldType({})".format(level, profession, self._param1, self._param2)
		writeRewardInfosToLogFile(1, tmpSelectList, 1, rewardList, rewardID, weightRandomNum, selectCons)
		return rewardList


class RewardToRate( RewardRule ):
	"""
	#获取概率随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardRule.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		level = 0
		if REWARD_ENTITY_TYPE_PLAYER in args:
			player = args[ REWARD_ENTITY_TYPE_PLAYER ]
			level = player.getLevel()
		rewardList = []
		for data in  self._datas :
			rate =data["rate"]
			if not rate.strip():
				continue
			tmpSelectList.append(data)
			if getRewardForRate( float( rate ) ):
				rewardList.append( self.extractReward( data, level ) )

		writeRewardInfosToLogFile(2, tmpSelectList, len(tmpSelectList), rewardList, rewardID, rateRandomNum, "RewardToRate")
		return rewardList
		
		
class RewardForLevelToRate( RewardToRate ):
	"""
	根据等级生成概率随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToRate.__init__( self, configSection, data )
		
	def doReward( self, level, rewardID = 0, conArgs = "No condition args"):
		"""
		执行生成奖励
		"""
		rewardList = []
		for data in  self._datas :
			tempLevel =data["level"]
			if not tempLevel.strip() or int( tempLevel ) != level:
				continue
			rate =data["rate"]
			if not rate.strip():
				continue
			tmpSelectList.append(data)
			if getRewardForRate( float( rate ) ):
				rewardList.append( self.extractReward( data, level ) )

		writeRewardInfosToLogFile(2, tmpSelectList, len(tmpSelectList), rewardList, rewardID, rateRandomNum, conArgs)
		return rewardList	
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if REWARD_TYPE_LEVEL not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		
		level = args[ REWARD_TYPE_LEVEL ]
		rewardList = self.doReward( level )
		return rewardList	
		

class RewardForMonsterIDToRate( RewardToRate ):
	"""
	#根据怪物ID获取概率随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToRate.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if isDebugingReward():
			scriptID = str(args.get(DEBUG_REWARD_CON, 0))
		else:
			if REWARD_ENTITY_TYPE_DIE not in args:
				KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
				return rewardList
			monster = args[ REWARD_ENTITY_TYPE_DIE]
			scriptID = monster.getScriptID()
		
		level = 0
		if REWARD_ENTITY_TYPE_PLAYER in args:
			player = args[ REWARD_ENTITY_TYPE_PLAYER ]
			level = player.getLevel()
			
		for data in  self._datas :
			tempID =data["scriptid"]
			if tempID != scriptID:
				continue
			rate =data["rate"]
			if not rate.strip():
				continue
			tmpSelectList.append(data)
			if getRewardForRate( float( rate ) ):
				rewardList.append( self.extractReward( data, level ) )

		writeRewardInfosToLogFile(2, tmpSelectList, len(tmpSelectList), rewardList, rewardID, rateRandomNum, "RewardForMonsterIDToRate:scriptID({})".format(scriptID))
		return rewardList	
	

class RewardForDieLevelToRate( RewardForLevelToRate ):
	"""
	#根据被击杀对象等级获取概率随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToRate.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if isDebugingReward():
			level = args.get(DEBUG_REWARD_CON, 0)
		else:
			if REWARD_ENTITY_TYPE_DIE not in args:
				KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
				return rewardList
			dieEntity = args[ REWARD_ENTITY_TYPE_DIE ]
			level =dieEntity.level
		rewardList = self.doReward(level, rewardID, "RewardForDieLevelToRate: level({})".format(level))
		return rewardList	


class RewardForRoleLevelToRate( RewardForLevelToRate ):
	"""
	#根据玩家等级获取概率随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToRate.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []

		if REWARD_ENTITY_TYPE_PLAYER not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		player = args[ REWARD_ENTITY_TYPE_PLAYER]
		level =player.level
		rewardList = self.doReward( level, rewardID, "RewardForRoleLevelToRate: level({})".format(level))
					
		return rewardList	


class RewardForGiftLevelToRate( RewardForLevelToRate ):
	"""
	#根据礼包等级获取概率随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToRate.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if isDebugingReward():
			level = args.get(DEBUG_REWARD_CON, 0)
		else:
			if REWARD_ENTITY_TYPE_GIFT not in args:
				KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
				return rewardList
			itemGift = args[ REWARD_ENTITY_TYPE_GIFT]
			level = itemGift.getLevel()

		rewardList = self.doReward( level, rewardID, "RewardForGiftLevelToRate: level({})".format(level))
				
		return rewardList	
		

class RewardForRoleProfessionToRate( RewardToRate ):
	"""
	#根据玩家职业获取概率随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToRate.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if REWARD_ENTITY_TYPE_PLAYER not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		player = args[ REWARD_ENTITY_TYPE_PLAYER ]
		profession = player.profession
		
		level = player.getLevel()
			
		for data in  self._datas :
			tempProfession =data["profession"]
			if not tempProfession.strip() or int( tempProfession ) != profession:
				continue
			rate =data["rate"]
			if not rate.strip():
				continue
			tmpSelectList.append(data)
			if getRewardForRate( float( rate ) ):
				rewardList.append( self.extractReward( data, level ) )

		writeRewardInfosToLogFile(2, tmpSelectList, len(tmpSelectList), rewardList, rewardID, rateRandomNum,
				"RewardForRoleProfessionToRate: profession({})".format(profession))
		return rewardList	
		
		
class RewardForRLevelAndRProfessionToRate( RewardToRate ):
	"""
	#根据玩家等级和职业获取概率随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardToRate.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if REWARD_ENTITY_TYPE_PLAYER not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		player = args[ REWARD_ENTITY_TYPE_PLAYER ]
		level = player.getLevel()
		profession = player.profession
			
		for data in  self._datas :
			tempProfession =data["profession"]
			tempLevel = data["level"]
			if not tempLevel.strip() or int( tempLevel ) != level:
				continue
			if not tempProfession.strip() or int( tempProfession ) != profession:
				continue
			rate = data["rate"]
			if not rate.strip():
				continue
			tmpSelectList.append(data)
			if getRewardForRate( float( rate ) ):
				rewardList.append( self.extractReward( data, level ) )

		writeRewardInfosToLogFile(2, tmpSelectList, len(tmpSelectList), rewardList, rewardID, rateRandomNum,
				"RewardForRLevelAndRProfessionToRate: level({}), profession({})".format(level, profession))
		return rewardList	
		

class RewardForQuestIDAndMonsterIDToRate( RewardToRate ):
	"""
	#根据怪物ID和任务ID获取概率随机奖励，仅用于掉落
	"""
	def __init__( self, configSection, data ):
		RewardToRate.__init__( self, configSection, data )
		
	def fetch( self, args ):
		"""
		执行生成奖励
		"""
		rewardDatas = {}
		if REWARD_ENTITY_TYPE_OWNERLIST not in args or REWARD_ENTITY_TYPE_DIE not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardDatas
		ownerList = args[ REWARD_ENTITY_TYPE_OWNERLIST ]
		monster = args[ REWARD_ENTITY_TYPE_DIE ]
		questDatas = RewardQuestData.datas
		scriptID = monster.getScriptID()
		
		for data in questDatas:
			if data["scriptid"] == scriptID:
				questID = data["questid"]
				rate = data["rate"]
				for id in ownerList:
					player = KBEngine.entities.get( id, None )
					if not player:
						continue
					questList = player.questTable.keys()
					if int( questID ) in questList and player.queryQuestStatus( int( questID ) ) != csdefine.QUEST_DONE:
						if getRewardForRate( rate ):
							if id not in rewardDatas:
								rewardDatas[ player.playerDBID ] = []
							rewardDatas[ player.playerDBID ].append( self.extractReward( data, player.getLevel() ) )
		
		return rewardDatas	
		

class RewardForPseudoRandom( RewardRule ):
	"""
	伪随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardRule.__init__( self, configSection, data )
	
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		if REWARD_ENTITY_TYPE_PLAYER not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		player = args[ REWARD_ENTITY_TYPE_PLAYER ]
		
		rRecordIDList = []
		if player.rewardRecord:
			rRecordIDList = player.rewardRecord.split("|")
		_rRecordIDs = {}
		for record in rRecordIDList:
			recordList = record.split(":")
			_rRecordIDs[ recordList[0] ] = int( recordList[1] )
		if not rewardID in _rRecordIDs and self._param1:
			from ConfigObject.Reward.RewardBase import RewardMgr
			rewardList = RewardMgr.g_rewardMgr.getReward( self._param1, args )
			if player.rewardRecord:
				player.rewardRecord += "|" + rewardID + ":" + str( 1 )
			else:
				player.rewardRecord = rewardID + ":" + str( 1 )
		else:
			sequence = _rRecordIDs.get( rewardID, 0 )
			firstIndex = -1
			index = -1
			flag = False
			for i in range( len( self._datas ) ):
				data = self._datas[i]
				tempSequence = int( data["sequence"] )
				if tempSequence == 1:
					firstIndex = i
				if tempSequence == sequence + 1:
					index = i
					_rRecordIDs[rewardID] = tempSequence
					flag = True
					break
			if not flag:
				index = firstIndex
				_rRecordIDs[rewardID] = 1
			if self._datas[ index ]["precious"] == "1":
				_rRecordIDs[rewardID] = 0
			sequencestr = ""
			for key, value in _rRecordIDs.items():
				sequencestr += "|" + key + ":" + str( value )
			player.rewardRecord = sequencestr[1: len( sequencestr )]
			rewardList.append( self.extractReward( self._datas[ index ], player.level ) )
		return rewardList

class RewardForYCJMDBossDieLevelToWeight( RewardForLevelToWeight ):
	"""
	CST-8727 根据勇闯夺命岛Boss被击杀的等级获取权重随机奖励
	"""
	def __init__( self, configSection, data ):
		RewardForLevelToWeight.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList =[]
		if REWARD_ENTITY_TYPE_DIE not in args:
			KBEDebug.ERROR_MSG("the reward data is error: %s " % str( args ) )
			return rewardList
		dieEntity = args[ REWARD_ENTITY_TYPE_DIE ]
		level = dieEntity.getYCJMDBossLevel()
		reward = self.doReward( level )
		if reward:
			rewardList.append( reward )
		return rewardList

class RewardForNumber( RewardRule ):
	"""
	数量修正 受两个参数影响：1.初始概率X；2.道具奖励系数Y，执行时的最终概率为：X*Y
	"""
	def __init__( self, configSection, data ):
		RewardRule.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		level = 0
		ratio = 1	# 道具奖励系数
		rewardList = []
		spaceRewardRate = 1.0
		if REWARD_ENTITY_TYPE_PLAYER in args:
			player = args[ REWARD_ENTITY_TYPE_PLAYER ]
			level = player.getLevel()
			spaceEntity = player.getCurrentSpace()
			if spaceEntity:
				spaceRewardRate = spaceEntity.queryTemp("spaceRewardRate", 1.0)
		if REWARD_ENTITY_TYPE_RATIO in args:
			ratio = float(args[REWARD_ENTITY_TYPE_RATIO ])
		for data in  self._datas :
			rate = data["rate"]
			if not rate.strip():
				continue
			XY = ratio * float(rate) * spaceRewardRate
			if math.floor( XY ) > 0.0:
				tempRewardList = self.extractReward( data, level )
				tempRewardList["amount"] *= int(math.floor( XY )) 
				rewardList.append( tempRewardList )
			if getRewardForRate( float( XY - math.floor( XY ) ) ):
				rewardList.append( self.extractReward( data, level ) )
		return rewardList

class RewardForRare( RewardRule ):
	"""
	稀有度修正  可配置多种道具，数量不限，要求所有种类道具概率之和为100%，同时会受道具奖励系数extraRewardID（不可以为0）的影响
	"""
	def __init__( self, configSection, data ):
		RewardRule.__init__( self, configSection, data )
		
	def fetch( self, rewardID, args ):
		"""
		执行生成奖励
		"""
		rewardList = []
		rewardRateDict = {}
		ratio = 1	# 道具奖励系数
		level = 0
		start = 0.0
		if REWARD_ENTITY_TYPE_PLAYER in args:
			player = args[ REWARD_ENTITY_TYPE_PLAYER ]
			level = player.getLevel()
		if REWARD_ENTITY_TYPE_RATIO in args:
			ratio = float(args[REWARD_ENTITY_TYPE_RATIO ])
		for i in range( len( self._datas ) ):
			rewardRateDict[int(self._datas[i]["priority"])] = self._datas[i]

		if rewardRateDict:
			priorityList = sorted( rewardRateDict.keys(), key = lambda x:x )
			x = random.uniform(0,1)
			endRate = x/ratio
			if endRate > 1.0:
				rewardList.append(self.extractReward( rewardRateDict[priorityList[-1]], level ))
				return rewardList
			for priority in priorityList:
				if start < endRate <= ( float(rewardRateDict[priority]["rate"]) + start ):
					rewardList.append( self.extractReward( rewardRateDict[priority], level ))
					return rewardList
				else:
					start += float(rewardRateDict[priority]["rate"])
		return rewardList


