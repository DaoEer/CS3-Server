# -*- coding: utf-8 -*-
import Math
import Functions
import KBEMath
import csdefine
from ObjectScript.Space.SpaceCopy import SpaceCopy


class SpaceCopyCampFiveYCJMD( SpaceCopy ):
	"""
	阵营战场“勇闯绝命岛”（5人） JIRA CST-10463
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.birthInfos = []		# 出生点
		self.rewardSpellBoxID = 0
		self.loserRewardMailID = 0 #失败方奖励邮件ID
		self.winnerRewardMailID = 0 #胜利方奖励邮件ID
		self.killExpRate = 0 #玩家击杀经验奖励系数
		self.killFeats = 0 #玩家击杀功勋奖励
		self.killExploits = 0#玩家击杀军功奖励
		self.finalExpDict = {} #结算经验奖励 按等级和胜负区分
		self.finalWinFeats = 0 #结算功勋奖励 胜利方
		self.finalLostFeats = 0 #结算功勋奖励 失败方
		self.finalLostExploits = 0 #结算军功奖励 失败方
		self.finalWinExploits = 0 #结算军功奖励 胜利方
		self.outRewardMailDict = {} #把数值结算奖励通过邮件发给出局的玩家

	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
	
		birthPosInfos = configData["SpaceData"].get("birthPosList","").split("|")
		birthDirInfos = configData["SpaceData"].get("birthDirList","").split("|")
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
		self.rewardSpellBoxID = configData["SpaceData"].get("rewardSpellBoxID", 0)	
		self.loserRewardMailID = configData["SpaceData"].get("loserRewardMailID", 0)
		self.winnerRewardMailID = configData["SpaceData"].get("winnerRewardMailID", 0)
		self.killExpRate = configData["SpaceData"].get("killExpRate", 0)
		self.killFeats = configData["SpaceData"].get("killFeats", 0)
		self.killExploits = configData["SpaceData"].get("killExploits", 0)
		finalExpDict = configData["SpaceData"].get("finalExpDict", {})
		for level, expList in finalExpDict.items():
			self.finalExpDict[int(level)] = expList
		self.finalWinFeats = configData["SpaceData"].get("finalWinFeats", 0)
		self.finalLostFeats = configData["SpaceData"].get("finalLostFeats", 0)
		self.finalLostExploits = configData["SpaceData"].get("finalLostExploits", 0)
		self.finalWinExploits = configData["SpaceData"].get("finalWinExploits", 0)
		outRewardMailDict = configData["SpaceData"].get("outRewardMailDict", {})
		for level, mailIDList in outRewardMailDict.items():
			self.outRewardMailDict[int(level)] = mailIDList

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )

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


	def getRewardSpellBoxID( self ):
		return self.rewardSpellBoxID

	def getLoserRewardMailID(self):
		return self.loserRewardMailID

	def getWinnerRewardMailID(self):
		return self.winnerRewardMailID

	def getKillExpRate(self):
		return self.killExpRate

	def getKillFeats(self):
		return self.killFeats

	def getKillExploits(self):
		return self.killExploits

	def getFinalExpDict(self, level, index):
		level = level//10*10
		if level in self.finalExpDict:
			return self.finalExpDict[level][index]
		return 0

	def getFinalWinFeats(self):
		return self.finalWinFeats

	def getFinalLostFeats(self):
		return self.finalLostFeats 

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