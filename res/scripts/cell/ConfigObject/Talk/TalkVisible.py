# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *
from ConfigObject.Talk.TalkBase import BaseNPCTalkVisible


class TVLevel(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	等级限制对话选项可见性
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.needLevel = int( visibleData[ "param1" ] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return player.getLevel() >= self.needLevel

class TVQuestStatus(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	任务状态限制对话选项可见性
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		#举例：20101100;3;1:2;2:3|20101101;3;1:3
		#表示：“任务20101100未完成，并且目标1完成目标2未完成”或者“任务20101101未完成，并且目标1未完成”的情况下条件通过
		self.questInfoList = []		
		for questInfo in visibleData["param1"].split("|"):
			questInfo = questInfo.split(";")
			if len(questInfo) >= 1:
				questData = {}
				questData["questID"] = int(questInfo[0].split(":")[0])
				questData["questStatus"] = int(questInfo[0].split(":")[1])
				questData["taskInfo"] = []
				if len(questInfo) >= 2:
					for i in range(1, len(questInfo)):
						taskData = {}
						taskInfo = questInfo[i].split(":")
						taskData["taskID"] = int(taskInfo[0])
						taskData["taskStatus"] = int(taskInfo[1])
						questData["taskInfo"].append(taskData)
				self.questInfoList.append(questData)
			else:
				ERROR_MSG("npctalk config error: '%s'" % questInfo)

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		for questInfo in self.questInfoList:
			if player.queryQuestStatus(questInfo["questID"]) == questInfo["questStatus"]:
				if questInfo["taskInfo"]:
					for taskInfo in questInfo["taskInfo"]:
						if player.queryTaskStatus(questInfo["questID"], taskInfo["taskID"]) != taskInfo["taskStatus"]:
							break
					else:
						return True
				else:
					return True
		return False
		
class TVJoinInTong(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否加入帮会
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return not player.tongMB is None
		
class TVSpaceTong(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否在所属帮会的领地
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		if player.tongMB:
			space = talkEntity.getCurrentSpace()
			try:
				return space.tongDBID == player.tongDBID
			except:
				ERROR_MSG("Check tongDBID error!!")
		return False
		
class TVLingMaiTime(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否在灵脉战场活动时间
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return KBEngine.globalData.get( "LingMaiBattle", 0 )

class TVTongFirstStarcraftSignUp(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否开启第一场帮会争霸报名
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return KBEngine.globalData.get( "firstTongStarcraftSignUp", 0 )

class TVTongFirstStarcraftStart(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否开始第一场帮会争霸
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return KBEngine.globalData.get( "firstTongStarcraftStart", 0 )

class TVTongSecondStarcraftSignUp(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否开启第二场帮会争霸报名
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		tempStr = "secondTongStarcraft_SignUp_%i"%talkEntity.getCamp()
		return KBEngine.globalData.get( tempStr, 0 )

class TVTongSecondStarcraftStart(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否开始第一场帮会争霸
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		tempStr = "secondTongStarcraft_Start_%i"%talkEntity.getCamp()
		return KBEngine.globalData.get( tempStr, 0 )

class TVShiFangChengSignUp(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否开启十方城 报名
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return KBEngine.globalData.get( "SFC_StateSignUp", 0 )

class TVShiFangChengStart(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否开启十方城
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return KBEngine.globalData.get( "SFC_StateStart", 0 )

class TVYeZhanFengQiStart(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否开启血斗凤栖镇
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		pass
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return KBEngine.globalData.get( "YZFQ_StateStart", 0 )

class TVSpaceCopyMagicMazeReward(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	幻阵迷宫 显示特殊奖励面板
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.progress = int( conditionData[ "param1" ] )
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		spaceEntity = talkEntity.getCurrentSpace()
		if spaceEntity:
			if player.id in spaceEntity.advanceAwardList:
				return False		#领过就不显示了
			if spaceEntity.progress == 0 and spaceEntity.copyIsComplet:
				return True
			elif spaceEntity.progress >= self.progress:
				return True
		return False

class TVSpaceCopyMagicMazeHide(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	幻阵迷宫 通关隐藏开始挑战框
	"""
	def __init__(self, conditionData):
		"""
		初始化
		"""
		self.progress = int( conditionData[ "param1" ] )
		
	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		spaceEntity = talkEntity.getCurrentSpace()
		if  spaceEntity:
			if spaceEntity.progress == 0 and spaceEntity.copyIsComplet:
				return False
			elif spaceEntity.progress < self.progress:
				return True
		return False

class TVTongTianDaQuestStatus(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	通天塔任务状态限制对话选项可见性
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.questID = int( visibleData[ "param1" ] )
		self.questStatus = int( visibleData[ "param2" ] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		if player.queryQuestStatus( self.questID ) == self.questStatus and not player.isInAbandonQuestList( self.questID ) and not player.isChallenge:
			return True
		return False
		
class TVPlayerOccupySpaceType( BaseNPCTalkVisible.BaseNPCTalkVisible ):
	"""
	（轮回秘境）玩家是否占领了洞府/或者持有玲珑玉令
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		BaseNPCTalkVisible.BaseNPCTalkVisible.__init__(self, visibleData)
		self.spaceType = [int(i) for i in visibleData["param1"].split("|") ]		# 0:无占领无玲珑玉令，1：占领洞府，2：有玲珑玉令, 3:高级洞府
		self.hasOwn = 1
		if visibleData["param2"]:
			self.hasOwn = int( visibleData["param2"] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if player.occupySpaceDF in self.spaceType and self.hasOwn:
			return True
		if not player.occupySpaceDF in self.spaceType and not self.hasOwn:
			return True
		return False

class TVCamp(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	满足阵营条件
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.needCamp = int( visibleData[ "param1" ] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return self.needCamp == player.getFinalCamp() or self.needCamp == csdefine.CMAP_NONE

class TVProfession(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	满足职业条件
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.needProfession = int( visibleData[ "param1" ] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return self.needProfession == player.getProfession()

class TVBelongSide(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	满足攻守方条件
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.belongSide = int( visibleData[ "param1" ] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查条件
		"""
		return self.belongSide == player.getBelongSide()

class TVOccupyTrainGround(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	满足是否占该领练兵场
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.isOccupy = True
		if visibleData["param1"]:
			self.isOccupy =  bool( int(visibleData["param1"]) )

	def isVisible(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if self.isOccupy and player.playerDBID == talkEntity.getOccupyPlayerDBID():
			return True
		if not self.isOccupy and player.playerDBID != talkEntity.getOccupyPlayerDBID():
			return True
		return False

class TVIsDeclareTrainGround(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	是否已被宣战
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.isDeclare = bool( int(visibleData["param1"]) )

	def isVisible(self, player, talkEntity, args):
		"""
		检查条件
		"""
		if talkEntity.getDeclareWarDBID() > 0 and self.isDeclare:
			return True
		if talkEntity.getDeclareWarDBID() <= 0 and not self.isDeclare:
			return True
		return False

class TVQiYuanQuestStatus(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	奇缘任务限制对话选项可见性
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.questID = int( visibleData[ "param1" ] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		if not player.hasQuest(self.questID) and not player.hadFinishedQuest(self.questID):
			return True
		return False
		
class TVGlobalDataEqualValue(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	globalData中某个key值对应的是否是某值
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self._verifyData = visibleData["param1"].split("|")

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		
		if len(self._verifyData) >= 2 and KBEngine.globalData.get(self._verifyData[0], None) == self._verifyData[1]:
			return True
		return False

class TVIsOwner(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	对话玩家是否是拥有者
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		pass

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return talkEntity.ownerDBID == player.playerDBID
		
class TVValidatePotentialSpaceReward(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	对话玩家是否满足潜能副本中礼包领取条件
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self._verifyData = int(visibleData["param1"].strip())

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return player.qianNengData.get("WinTimes", 0) >= self._verifyData

class TVDFBuildIsDestroy(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	对话玩家 洞府建筑是否被破坏
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.buildType = int( visibleData["param1"] )
		self.isDestroy = int( visibleData["param2"] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		if self.buildType in player.destroyBuilds and self.isDestroy:
			return True
		if not self.buildType in player.destroyBuilds and not self.isDestroy:
			return True
		return False
		
class TVDFBuildIsRepair(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	对话玩家 洞府建筑是否正在修复
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.buildType = int( visibleData["param1"] )

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return self.buildType in player.repairBuildTime

class TVPlayerHasItems(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	玩家是否拥有某数量的道具
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.itemIDStr = visibleData["param1"]
		self.itemAmountStr = visibleData["param2"]
		self.condition = int(visibleData["param3"])

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		itemIDList = self.itemIDStr.split("|")
		itemAmountList = self.itemAmountStr.split("|")
		for itemID, amount in zip(itemIDList, itemAmountList):
			itemList = player.getItemInstsByID(int(itemID))
			hasAmount = 0
			if len(itemList):
				for item in itemList:
					hasAmount += item.getAmount()
				if self.condition:
					if not hasAmount >= int(amount):
						return False
				else:
					if not hasAmount < int(amount):
						return False
			else:
				if not self.condition:
					continue
				return False
		return True
		
class TVLunHuiMiJingHasOpen(BaseNPCTalkVisible.BaseNPCTalkVisible):
	"""
	对话玩家 轮回秘境第二层进入
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.spaceScriptID = visibleData["param1"]

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		key = csdefine.CONTROL_SPACE_KEY + self.spaceScriptID
		if KBEngine.globalData.get(key, False):
			return True
		return False
		
class TVTongPlunderActiveStatus( BaseNPCTalkVisible.BaseNPCTalkVisible ):
	"""
	帮会掠夺战是否处于某状态，1 报名，2 开启
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.status = int(visibleData["param1"])

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return KBEngine.globalData["TongPlunderManager_Status"] == self.status

class TVGCZStatus( BaseNPCTalkVisible.BaseNPCTalkVisible ):
	"""
	攻城战开启某状态 1.报名 2.匹配 3.进入 4.开启
	"""
	def __init__(self, visibleData):
		"""
		初始化
		"""
		self.status = int(visibleData["param1"])

	def isVisible(self, player, talkEntity, args):
		"""
		检查可见性
		"""
		return self.status in KBEngine.globalData.get( "GCZStatus",[] )