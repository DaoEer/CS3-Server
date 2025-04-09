# -*- coding: utf-8 -*-
import csdefine
from ObjectScript.Space.SpaceCopy import SpaceCopy
import Functions
import KBEMath
import random


class SpaceCopyCampYCJMD( SpaceCopy ):
	"""
	阵营战场“勇闯绝命岛” JIRA CST-9960
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.landBuffID = 0
		self.birthInfos = []
		self.flyPathList = []
		self.loserRewardMailID = 0 #失败方奖励邮件ID
		self.winnerRewardMailID = 0 #胜利方奖励邮件ID
		self.killExpRate = 0 #玩家击杀经验奖励系数
		self.killExploits = 0#玩家击杀军功奖励
		self.finalExpDict = {} #结算经验奖励 按等级和胜负区分
		self.finalLostExploits = 0 #结算军功奖励 失败方
		self.finalWinExploits = 0 #结算军功奖励 胜利方
		self.outRewardMailDict = {} #把数值结算奖励通过邮件发给出局的玩家
		self.colorScheme = csdefine.MODEL_COLOR_SCHEME_MS	# 默认美术变色方案

	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		
		BuffIDstr = configData["SpaceData"].get( "ParachuteLandBuff", "" )
		if BuffIDstr:
			self.landBuffID = int(BuffIDstr)

		birthPosInfosStr = configData["SpaceData"].get("birthPosList","")
		birthPosInfos = birthPosInfosStr.split("|") if birthPosInfosStr else []
		
		birthDirInfosStr = configData["SpaceData"].get("birthDirList","")
		birthDirInfos = birthDirInfosStr.split("|") if birthDirInfosStr else []
		birthPosList = []
		birthDirList = []
		for enterPosInfo in birthPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( tuple(pos) )
			birthPosList.append(pos)
		for enterDirInfo in birthDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEngineDirection( tuple(dir) )
			birthDirList.append(dir)
		for i in range(0,len(birthPosList)):
			self.birthInfos.append( (Math.Vector3(birthPosList[i]), Math.Vector3(birthDirList[i])) )

		flyPathStr = configData["SpaceData"].get("flyPathStr","")
		if flyPathStr:
			self.flyPathList = flyPathStr.split("|")

		self.tempCampBuffs = configData['SpaceData'].get('tempCampBuffs', {})
		self.loserRewardMailID = configData["SpaceData"].get("loserRewardMailID", 0)
		self.winnerRewardMailID = configData["SpaceData"].get("winnerRewardMailID", 0)
		self.killExpRate = configData["SpaceData"].get("killExpRate", 0)
		self.killExploits = configData["SpaceData"].get("killExploits", 0)
		finalExpDict = configData["SpaceData"].get("finalExpDict", {})
		for level, expList in finalExpDict.items():
			self.finalExpDict[int(level)] = expList
		self.finalLostExploits = configData["SpaceData"].get("finalLostExploits", 0)
		self.finalWinExploits = configData["SpaceData"].get("finalWinExploits", 0)
		outRewardMailDict = configData["SpaceData"].get("outRewardMailDict", {})
		for level, mailIDList in outRewardMailDict.items():
			self.outRewardMailDict[int(level)] = mailIDList
			
		self.colorScheme = configData["SpaceData"].get("colorScheme", 1)

	def onCampYCJMDPlayerParachuteLand(self, player):
		"""
		玩家开始下落
		"""
		player.addBuff(player, self.landBuffID)

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		packDict["playerDBID"] = playerEntity.playerDBID
		return packDict


	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.setBirthInfos( self.birthInfos )
		selfEntity.flyPath = self.getFlyPathRandom()

	def getFlyPathRandom(self):
		"""
		随机一条飞行路线
		"""
		return random.choice(self.flyPathList) if self.flyPathList else ""

	def getTempCampBuff(self, tempCamp):
		return self.tempCampBuffs.get(str(tempCamp), 0)

	def getLoserRewardMailID(self):
		return self.loserRewardMailID

	def getWinnerRewardMailID(self):
		return self.winnerRewardMailID

	def getKillExpRate(self):
		return self.killExpRate

	def getKillExploits(self):
		return self.killExploits

	def getFinalExpDict(self, level, index):
		level = level//10*10
		if level in self.finalExpDict:
			return self.finalExpDict[level][index]
		return 0

	def getFinalWinExploits(self):
		return self.finalWinExploits

	def getFinalLostExploits(self):
		return self.finalLostExploits

	def getOutRewardMailID(self, level, index):
		"""
		获取失败出局的奖励邮件ID
		"""
		level = level//10*10
		if level in self.outRewardMailDict:
			return self.outRewardMailDict[level][index]
		return 0
		
	def getColorScheme( self ):
		"""获取模型变色方案"""
		return self.colorScheme