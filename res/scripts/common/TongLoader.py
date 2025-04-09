# -*- coding:utf-8 -*-

# 帮会数据加载
import csdefine

from KBEDebug import *
from LoadModule import *
from Tong.TongPlayType import Datas as tongPlayType
from Tong.TongBuildFunc import Datas as tongBuildFunc
from Tong.TongBuildLevel import Datas as tongBuildLevel
from Tong.TongMemberConfig import Datas as tongMemberConfig

#-----------------------帮会等级---------------------------------------
class TongLevelLoader:
	_instance = None
	
	def __init__(self):
		self.datas = {}
		self.loadConfig()
		
	@staticmethod
	def instance():
		if TongLevelLoader._instance is None:
			TongLevelLoader._instance = TongLevelLoader()
		return TongLevelLoader._instance
		
	def loadConfig(self):
		jsonDatas =	openJsonCfg("Tong/TongLevel.json")
		for data in jsonDatas:
			self.datas[data["level"]] = data
			
	def getDataByLevel(self, level):
		return self.datas.get(level, {})
		
	def getMaxLevel(self):
		if len(self.datas):
			return max(list(self.datas.keys()))
		return 0
			
g_TongLevelLoader  = TongLevelLoader.instance()


def getUpgradeUseMoney( level ):
	"""升级消耗金钱"""
	return g_TongLevelLoader.getDataByLevel(level).get("useMoney", 0)
	
def getUpgradeUseActivity( level ):
	"""升级消耗活跃度"""
	return g_TongLevelLoader.getDataByLevel(level).get("useActivity", 0)
		
def getMaxTongLevel():
	"""获取帮会最大等级"""
	return g_TongLevelLoader.getMaxLevel()
		
def getPerDayUseActivity( level ):
	"""获取每天的活跃度消耗"""
	return g_TongLevelLoader.getDataByLevel(level).get("perActivity", 0)
	
def getMinActivity( level ):
	"""获取帮会 最低活跃度"""
	return g_TongLevelLoader.getDataByLevel(level).get("minActivity", 0)

def getLockMoney(level):
	"""获取帮会掠夺战锁定帮会资金"""
	return g_TongLevelLoader.getDataByLevel(level).get("lockMoney", 0)
	
def getLowMoney(level):
	"""帮会最低维护资金"""
	return g_TongLevelLoader.getDataByLevel(level).get("lowMoney", 0)
	
def getPerActivityForLowMoney(level):
	"""帮会资金过低扣除活跃度比例"""
	return g_TongLevelLoader.getDataByLevel(level).get("perActivityForLowMoney", 0)

		
#-----------------------帮会建筑等级-------------------------------------
def getUpgradeBuildUseMoney( buildLevel, buildType ):
	"""建筑升级消耗金钱"""
	try:
		return tongBuildLevel[buildLevel][buildType]["upGradeMoney"]
	except:
		return 0
		
def getUpgradeBuildUseGrow( buildLevel, buildType ):
	"""建筑升级消耗成长度"""
	try:
		return tongBuildLevel[buildLevel][buildType]["upGradeGrow"]
	except:
		return 0
		
def getUpgrowNeedTongLevel( buildLevel, buildType ):
	"""建筑升级需要帮会等级"""
	try:
		return tongBuildLevel[buildLevel][buildType]["needTongLevel"]
	except:
		return 0

def getBuildMaxLevelByTongLevel( buildType, tongLevel ):
	"""建筑可升最大等级"""
	maxLevel = 1
	for buildLevel, config in tongBuildLevel.items():
		if config[buildType]["needTongLevel"] <= tongLevel:
			maxLevel = max( maxLevel, buildLevel )
	return maxLevel

def getMaxTongBuildLevel():
	return max( tongBuildLevel )
	
#-----------------------帮会建筑功能配置-------------------------------------
def getNagualScriptID( tongEntity ):
	"""获取神兽ScriptID"""
	type = "shenshou_" + str( tongEntity.nagualType )
	level = tongEntity.builds[csdefine.TONG_BUILDING_TYPE_SSD].getMaxLevel( tongEntity )
	if level in tongBuildFunc:
		return tongBuildFunc[level][type]
	return 0

def getNagualScriptIDByType( tongEntity, nagualType ):
	"""获取神兽ScriptID"""
	type = "shenshou_" + str( nagualType )
	level = tongEntity.builds[csdefine.TONG_BUILDING_TYPE_SSD].getMaxLevel( tongEntity )
	if level in tongBuildFunc:
		return tongBuildFunc[level][type]
	return 0

#-----------------------帮会玩法奖励配置-------------------------------------
def addRewardsByPlayType( tongEntity, playerDBID, type ):
	"""根据帮会玩法获取奖励"""
	if type in tongPlayType:
		if playerDBID in tongEntity.members:
			rewards = tongPlayType[type]
			if rewards["contribute"]:
				tongEntity.members[playerDBID].addContribution( tongEntity, rewards["contribute"] )
			if rewards["exp"]:
				tongEntity.members[playerDBID].addExp( tongEntity, rewards["exp"] )
			if rewards["activity"]:
				tongEntity.addActivity( rewards["activity"] )
			if rewards["grow"]:
				tongEntity.addGrow( rewards["grow"] )
			if rewards["money"]:
				tongEntity.addTongMoney( rewards["money"] )
		else:
			ERROR_MSG( "Player(dbid:%d) not in tong(%s)!!"%(playerDBID,tongEntity.tongName) )
	else:
		ERROR_MSG( "Add rewards err!can not find TongPlayType(type:%d) config"%type )
#-----------------------帮会帮众配置-------------------------------------
def getTitleByExp( exp ):
	"""获取帮众职位"""
	for titleID, config in tongMemberConfig.items():
		if titleID == csdefine.TONG_TITLE_1:continue
		if titleID == csdefine.TONG_TITLE_2:continue
		if titleID == csdefine.TONG_TITLE_3:continue
		if exp >= config["exp"] and config["exp"] > 0:
			return titleID
	return csdefine.TONG_TITLE_8
	
import KBEDebug
class TongLoader:
	_instance = None
	
	def __init__( self ):
		assert TongLoader._instance is None
		self._tongGrade = {}
		self._tongSkill = {}
		self.initTongGradeData( openJsonCfg("Tong/TongGradeTable.json") )
		self.initTongSkillData( openJsonCfg("Tong/TongSkill.json") )
		
	@staticmethod
	def instance():
		if TongLoader._instance is None:
			TongLoader._instance = TongLoader()
		return TongLoader._instance
		
	def initTongGradeData( self, jsonDatas ):
		"""帮会权限配置"""
		for gradeData in jsonDatas:
			temp = {}
			if gradeData["TongType"] != "TONG_TITLE_1":continue
			for key, value in gradeData.items():
				if key in [ "Name", "TongType" ]:continue
				elif key == "uiTongType":
					tongType = getattr( csdefine, value )
				else:
					grades = 0
					for grade in value:
						grades |= 1 << getattr( csdefine, grade )
					temp.update( { getattr( csdefine, key ) : grades } )
			self._tongGrade.update( { tongType : temp } )
			
			
	def initTongSkillData( self, jsonDatas ):
		"""帮会技能配置"""
		for skillData in jsonDatas:
			temp = {}
			for key, value in skillData.items():
				if key == "Name":continue
				elif key == "SkillID":
					skillID = int( value )
				else:
					temp.update( { key : value } )
			self._tongSkill.update( { skillID : temp } )
			
	def getAllSysGrades( self ):
		"""获取所有系统权限"""
		gradeList = []
		for gradeTypes in self._tongGrade.values():
			if csdefine.TONG_SYSTEM_GRADE in gradeTypes:
				gradeList.append( gradeTypes[csdefine.TONG_SYSTEM_GRADE] )
			else:
				gradeList.append(0)
		return gradeList
		
	def getSysGrades( self, titleID ):
		"""系统权限"""
		if csdefine.TONG_SYSTEM_GRADE in self._tongGrade[titleID]:
			return self._tongGrade[titleID][csdefine.TONG_SYSTEM_GRADE]
		return 0
		
	def getFobGrades( self, titleID ):
		"""禁止权限"""
		if csdefine.TONG_FORBID_GRADE in self._tongGrade[titleID]:
			return self._tongGrade[titleID][csdefine.TONG_FORBID_GRADE]
		return 0
		
	def isDefaultGrades( self, titleID, grade ):
		"""可操作权限"""
		if csdefine.TONG_DEFAULT_GRADE in self._tongGrade[titleID]:
			grades = self._tongGrade[titleID][csdefine.TONG_DEFAULT_GRADE]
			return grades & grade
		return False
	
	def getSkillReqConditionByName( self, skillID, conditionName ):
		"""根据名称，获得技能条件"""
		return self._tongSkill[skillID][conditionName]
		
	def getPreSkill( self, skillID ):
		"""获取前置技能"""
		for id, skillData in self._tongSkill.items():
			if skillData["NextSkill"] == skillID:
				return id
			if skillID == id and skillData["Level"] == 1:
				return 0
		ERROR_MSG("Cannot get preskill by skillID(%d)"%skillID)
		return -1
	
	def getItemsByResearchSkill( self, skills ):
		"""根据技能列表，获取对应的物品ID"""
		skillList = []
		for id in skills:
			items = self._tongSkill[id]["ItemIDs"]
			if items:
				skillList.extend( items )
		return skillList
	
g_TongLoader = TongLoader.instance()
