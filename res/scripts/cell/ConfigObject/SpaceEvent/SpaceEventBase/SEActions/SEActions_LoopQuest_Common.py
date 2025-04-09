# -*- coding: utf-8 -*-

# 副本事件行为
import time
import Math
import KBEDebug
import KBEngine
import csconst
import Functions
import KBEMath
import Reward.RewardBasicValueData as RewardBase
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
from ConfigObject import PatrolRouteLoader
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
from MsgLogger import g_logger
import LogDefine
from ConfigObject.Drop import DropItem
import csdefine
import csstatus
import random

def calcRewardDatas(rewardDatas):
	"""
	"""
	rewardItemDatas = []
	for data in rewardDatas:
		type = data["type"]
		amount = data["amount"]
		goodsid = data["goodsid"]
		# 物品奖励
		if type == csdefine.REWARD_TYPE_ITEM:
			rewardItemDatas.append( data )
	return rewardItemDatas

class SEAction330(SEActionBase):
	"""
	环任务副本通关(统计)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.entryIndex = int( section["param1"].strip() ) - 1
		self.questID = section["param2"].strip()
		self.msgInfo = section["param3"].strip()
		self.countDown = int(section["param4"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		num = spaceEntity.getSpaceStatisticsNum( self.entryIndex )
		rewardStr = ""
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( num )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeExpRatio, gradeMoneyRatio = quest.getGradeReward( roleCell )
				gradeScore = quest.getGradeScore( roleCell )
				expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
				
				expBase = RewardBase.datas[roleCell.level]["exp"]
				exp = int( expRatio * gradeExpRatio * expBase )
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeMoneyRatio * moneyBase )
				if money != 0:
					rewardStr += "0" + ":" + str(money) + "|"
				if exp != 0:
					rewardStr += "1" + ":" + str(exp) + "|"
					
				itemStr = ""
				rewardID, buff = quest.getGradeRewardIDAndBuff( roleCell )
				if rewardID:
					items = []
					rewardDatas = RewardMgr.g_rewardMgr.getReward(rewardID, {"player" : roleCell, "spaceLevel": spaceEntity.spaceLevel, })
					rewardItemDatas = calcRewardDatas( rewardDatas )
					for data in rewardItemDatas:
						itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
						if roleCell.addItem(itemInst, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT) != csstatus.ITEM_GO_ON:
							items.append( itemInst )
						
						if itemStr : itemStr += "|"
						itemStr += "{}:{}".format(itemInst.id, itemInst.getAmount())
						g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
						LogDefine.ACTIVE_REWARD_TYPE_ITEM, itemInst.id, spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
						
					#没有加成功的物品通过邮件发送
					if len(items):
						roleCell.sendRemainItemWithMail(items, csdefine.REMAIN_ITEM_SPACE_COPY, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT)
				
				if buff:
					buffList = [int(buffID) for buffID in buff.split("|")]
					for buffID in buffList:
						roleCell.addBuff(roleCell, buffID)
				
				roleCell.client.ShowLoopQuestSpaceWin( self.msgInfo, str(num), rewardStr, gradeScore, self.countDown, itemStr, buff )
				#添加环任务副本通关日志
				useTime = int( time.time() - spaceEntity.lifeStartTime )
				if money != 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_MONEY, str(money), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				if exp != 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_EXP, str(exp), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
		spaceEntity.getScript().onLoopQuestSpaceSuccess( spaceEntity, self.countDown )

class SEAction331(SEActionBase):
	"""
	环任务副本通关(时间)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = section["param1"].strip()
		self.msgInfo = section["param2"].strip()
		self.countDown = int(section["param3"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		useTime = int( time.time() - spaceEntity.lifeStartTime )
		limtTime = spaceEntity.lifeTime - useTime
		rewardStr = ""
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( limtTime )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeExpRatio, gradeMoneyRatio = quest.getGradeReward( roleCell )
				gradeScore = quest.getGradeScore( roleCell )
				expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
				
				expBase = RewardBase.datas[roleCell.level]["exp"]
				exp = int( expRatio * gradeExpRatio * expBase )
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeMoneyRatio * moneyBase )
				if money != 0:
					rewardStr += "0" + ":" + str(money) + "|"
				if exp != 0:
					rewardStr += "1" + ":" + str(exp) + "|"
				min = int( useTime / 60 )
				sec = useTime % 60
				_time = ""
				if min:
					_time += str( min ) + "分"
				if sec:
					_time += str( sec ) + "秒"
					
				itemStr = ""
				rewardID, buff = quest.getGradeRewardIDAndBuff( roleCell )
				if rewardID:
					items = []
					rewardDatas = RewardMgr.g_rewardMgr.getReward(rewardID, {"player" : roleCell, "spaceLevel": spaceEntity.spaceLevel, })
					rewardItemDatas = calcRewardDatas( rewardDatas )
					for data in rewardItemDatas:
						itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
						if roleCell.addItem(itemInst, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT) != csstatus.ITEM_GO_ON:
							items.append( itemInst )
						
						if itemStr : itemStr += "|"
						itemStr += "{}:{}".format(itemInst.id, itemInst.getAmount())
						g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
						LogDefine.ACTIVE_REWARD_TYPE_ITEM, itemInst.id, spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
						
					#没有加成功的物品通过邮件发送
					if len(items):
						roleCell.sendRemainItemWithMail(items, csdefine.REMAIN_ITEM_SPACE_COPY, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT)
				
				if buff:
					buffList = [int(buffID) for buffID in buff.split("|")]
					for buffID in buffList:
						roleCell.addBuff(roleCell, buffID)
					
				roleCell.client.ShowLoopQuestSpaceWin( self.msgInfo, _time, rewardStr, gradeScore, self.countDown, itemStr, buff )
				
				#添加环任务副本通关日志
				if money != 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_MONEY, str(money), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				if exp != 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_EXP, str(exp), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
		spaceEntity.getScript().onLoopQuestSpaceSuccess( spaceEntity, self.countDown )

class SEAction332(SEActionBase):
	"""
	环任务显示不同阶段的奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questID = section["param1"]
		self.entryIndex = 0
		if section["param2"]:
			self.entryIndex = int( section["param2"].strip() ) - 1

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		num = spaceEntity.getSpaceStatisticsNum( self.entryIndex )
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( num )
			if self.questID:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeExpRatio, gradeMoneyRatio = quest.getGradeReward( roleCell )
				expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
				
				expBase = RewardBase.datas[roleCell.level]["exp"]
				exp = int( expRatio * gradeExpRatio * expBase )
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeMoneyRatio * moneyBase )
				roleCell.client.ShowDynamicRewards( money, exp )

class SEAction333(SEActionBase):
	"""
	环任务开始倒计时进度条
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._time = int(section["param1"])
		self._changeTime = [ int(i) for i in section["param2"].split("|") ]
		self._changeColor = [ int(i) for i in section["param3"].split("|") ]
		self._type = int(section["param4"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if self._type == -1:
			endTime = str(self._time * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime())
		else:
			endTime = str(self._time)
		for roleCell in spaceEntity._spaceRoles:
			roleCell.client.OnStartReckonByTime( endTime, self._changeTime, self._changeColor, self._type )

class SEAction334(SEActionBase):
	"""
	环任务点击退出按钮则弹出二次确认界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._result = int(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for roleCell in spaceEntity._spaceRoles:
			roleCell.client.ShowLoopQuestResult( self._result )

class SEAction339(SEActionBase):
	"""
	进入某范围自动接环任务
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			if player.loopQuest["loopQuestList"]:
				questID = player.loopQuest["loopQuestList"][0]
				if player.hasQuest(questID):
					return
				if player.hadFinishedQuest( questID ):	# 由于目前环任务个数不足，策划要求临时处理：环任务阔以反复接已完成过的任务
					player.questLogger.erase(questID)
					player.client.onRemoveQuestLog(questID)
					player.removeQuestRecordAIIDS(questID)
				loopQuestList = list(player.loopQuest["loopQuestList"])
				loopQuestList.remove( questID )
				random.shuffle( loopQuestList )
				loopQuestList.append(questID)
				player.loopQuest["loopQuestList"] = loopQuestList
				questID = player.loopQuest["loopQuestList"][0]
				player.acceptQuest( questID )

class SEAction376(SEActionBase):
	"""
	环任务秘境 按玩家身上环任务ID去选择传送点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.questIDList = section["param1"].split("|")
		self.scriptIDList = section["param2"].split("|")
		self.posList = []
		self.dirList = []
		_posStrList = section["param3"].split("|")
		_dirStrList = section["param4"].split("|")

		if len( self.scriptIDList ) == len( _posStrList ) and len( _posStrList ) == len( _dirStrList ) and len( _dirStrList ) == len(self.questIDList):
				for posStr in _posStrList:
					tempList = posStr.split()
					kbePos = KBEMath.Unreal2KBEnginePosition( ( float(tempList[0]), float(tempList[1]), float(tempList[2]) ) )
					self.posList.append( kbePos )
				for dirStr in _dirStrList:
					tempList = dirStr.split()
					kbeDir = KBEMath.Unreal2KBEngineDirection( ( float(tempList[0]), float(tempList[1]), float(tempList[2]) ) )
					self.dirList.append( kbeDir )
		else:
			KBEDebug.ERROR_MSG("SEAction376 Param Num is different")
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		player = spaceEntity._spaceRoles[0]
		questID = player.loopQuest["loopQuestList"][0]

		if str(questID) in self.questIDList:
			index = self.questIDList.index( str(questID) )
			player.gotoSpace( self.scriptIDList[index], Math.Vector3(self.posList[index]), self.dirList[index] )
		else:
			KBEDebug.ERROR_MSG( "SEAction376 config error:player questID not in questIDList ")

SEActionBase.setActionClass("SEAction330", SEAction330)
SEActionBase.setActionClass("SEAction331", SEAction331)
SEActionBase.setActionClass("SEAction332", SEAction332)
SEActionBase.setActionClass("SEAction333", SEAction333)
SEActionBase.setActionClass("SEAction334", SEAction334)
SEActionBase.setActionClass("SEAction339", SEAction339)
SEActionBase.setActionClass("SEAction376", SEAction376)