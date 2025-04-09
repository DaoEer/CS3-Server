# -*- coding:utf-8 -*-
from LoadModule import *
import csdefine

class BuildDepleteLoader:
	"""
	建筑消耗配置
	"""
	def __init__(self):
		self.config = {}
		self.bulidMonsterData = {}

	def loadConfig( self ):
		self.bulidMonsterData = openJsonCfg("LunHuiMiJin/BulidMonsterCfg.json")
		config = openJsonCfg("LunHuiMiJin/BuildDepleteCfg.json")
		tempBuild = ["lingQuan", "gongFang", "qianKuDing", "shouLan", "lingTian","buildDepleteMoney", "buildDepletePsionic", "buildDepleteTime", "repairDepleteTime" ]
		for data in config:
			self.config[int(data["Name"])] = data
			
			for buildStr in tempBuild:
				for key in list(data[buildStr].keys()):
					data[buildStr][int(key)] = data[buildStr].pop(key)

	def reloadConfig( self ):
		self.config.clear()
		self.loadConfig()
		
	def getBuildMonsterDatas( self, group ):
		"""占领地基，生成怪物数据"""
		group = str( group )
		data = self.bulidMonsterData[group]
		scriptIDs = data["scriptID"]
		nums = data["num"]
		radius = float(data["radius"])
		return scriptIDs, nums, radius
		
	def getMaxBuildLevel( self ):
		"""获取建筑最大等级"""
		return max(self.config)

	def getBuildDepleteData( self, buildLevel, buildType ):
		"""
		获取建筑的消耗数据
		"""
		if buildLevel in self.config:
			if buildType == csdefine.LHMJ_BUIILD_LING_QUAN:
				return self.config[buildLevel]["lingQuan"]
			elif buildType == csdefine.LHMJ_BUIILD_GONG_FANG:
				return self.config[buildLevel]["gongFang"]
			elif buildType == csdefine.LHMJ_BUIILD_QIAN_KU_DING:
				return self.config[buildLevel]["qianKuDing"]
			elif buildType == csdefine.LHMJ_BUIILD_SHOU_LAN:
				return self.config[buildLevel]["shouLan"]
			elif buildType == csdefine.LHMJ_BUIILD_LING_TIAN:
				return self.config[buildLevel]["lingTian"]
		return {}

	def getBuildDepleteMoneyData( self, buildLevel, buildType ):
		"""
		获取建筑消耗的金钱
		"""
		if buildLevel in self.config and buildType in self.config[buildLevel]["buildDepleteMoney"]:
			return self.config[buildLevel]["buildDepleteMoney"][buildType]
		return 0

	def getBuildDepletePsionicData( self, buildLevel, buildType ):
		"""
		获取建筑消耗的灵能
		"""
		if buildLevel in self.config and buildType in self.config[buildLevel]["buildDepletePsionic"]:
			return self.config[buildLevel]["buildDepletePsionic"][buildType]
		return 0

	def getBuildUpgradeTime( self, buildType, buildLevel ):
		"""
		获取建筑需要的时间(单位：分钟)
		"""
		if buildLevel in self.config and buildType in self.config[buildLevel]["buildDepleteTime"]:
			return self.config[buildLevel]["buildDepleteTime"][buildType] * 60
		return 0
		
	def getBuildRepairTime( self, buildType, buildLevel ):
		"""
		获取建筑修复需要的时间(单位：分钟)
		"""
		if buildLevel in self.config and buildType in self.config[buildLevel]["repairDepleteTime"]:
			return self.config[buildLevel]["repairDepleteTime"][buildType] * 60
		return 0
		
	def getActivityRewardID( self, level, belongSide, stage, result ):
		"""获取活动奖励ID"""
		data = self.config[level]
		rewards = []
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			if stage == 1 and not result:				# 攻方第一阶段失败
				rewards.append( data["FailID"] )
			else:
				rewards.append( data["AOneSuccessID"] )
				if result:
					rewards.append( data["ATwoSuccessID"] )
				else:
					rewards.append( data["FailID"] )
		else:
			if stage == 1 and result:					# 守方第一阶段胜利，领两份奖励
				rewards.append( data["POneSuccessID"] )
				rewards.append( data["PTwoSuccessID"] )
			else:
				rewards.append( data["FailID"] )
				rewards.append( data["FailID"] )
		return rewards
				
	def getActivityGiftID( self, level, belongSide, stage, result ):
		"""下线获取的礼包奖励ID"""
		data = self.config[level]
		gifts = []
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			if stage == 1 and not result:				# 攻方第一阶段失败
				gifts.append( data["FailIGiftD"] )
			else:
				gifts.append( data["AOneSGiftID"] )
				if result:
					gifts.append( data["ATwoSGiftID"] )
				else:
					gifts.append( data["FailIGiftD"] )
		else:
			if stage == 1 and result:					# 守方第一阶段胜利，领两份奖励
				gifts.append( data["POneSGiftID"] )
				gifts.append( data["PTwoSGiftID"] )
			else:
				gifts.append( data["FailIGiftD"] )
				gifts.append( data["FailIGiftD"] )
		return gifts

g_BuildDepleteLoader = BuildDepleteLoader()