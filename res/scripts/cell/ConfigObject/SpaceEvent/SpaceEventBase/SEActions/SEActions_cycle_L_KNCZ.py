# -*- coding: utf-8 -*-

# 副本事件行为  狂牛冲撞
import csdefine
import random
import time
import KBEDebug
import KBEngine
import Reward.RewardBasicValueData as RewardBase
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
from MsgLogger import g_logger
import LogDefine
from ConfigObject.Drop import DropItem
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
import csstatus

class SEAction258( SEActionBase ):
	"""
	CST-6120 显示生存时间
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
		self.questID = 0
		self.surverTime = 0
		
		self.questID = int(section["param1"])
		self.surverTime = int( section["param2"])
	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		quest = g_QuestLoader.getScript( int(self.questID) )
		gradeRatioDatas = quest.getAllGradeReward()
		if gradeRatioDatas is None :return
		
		for roleCell in spaceEntity._spaceRoles:
			gradeList = []
			expList = []
			moneyList = []
			expRatio, moneyRatio = quest.getLoopRewardRadio( roleCell )
			expBase = RewardBase.datas[roleCell.level]["exp"]
		
			for gradeRatio in gradeRatioDatas:
				gradeList.append( gradeRatio["upper"] )
				exp = int( expRatio * gradeRatio["expRatio"] * expBase )
				expList.append(exp)
				money = 0
				if roleCell.loopQuest["isRewardMoney"]:
					moneyBase = RewardBase.datas[roleCell.level]["money"]
					money = int( moneyRatio * gradeRatio["moneyRatio"] * moneyBase )
				moneyList.append(money)
				
			gradeList.sort()
			expList.sort()
			moneyList.sort()
			roleCell.client.CLIENT_showSurvivalTime( self.surverTime, gradeList, expList, moneyList )

class SEAction259( SEActionBase ):
	"""
	生存界面开始倒计时
	"""	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
			
		spaceEntity.lifeStartTime = time.time()
		for e in spaceEntity._spaceRoles:
			e.client.CLIENT_startSurvivalTime()
			
class SEAction260( SEActionBase ):
	"""
	生存界面停止倒计时
	"""	
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		surverTime = int(time.time() - spaceEntity.lifeStartTime)
		
		for e in spaceEntity._spaceRoles:
			e.setLoopQuestTaskCompleteNum(surverTime)
			e.client.CLIENT_endSurvivalTime(surverTime)
			
class SEAction447(SEActionBase):
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
		
		useTime = int(time.time() - spaceEntity.lifeStartTime)
		rewardStr = ""
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setLoopQuestTaskCompleteNum( useTime )
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
					rewardItemDatas = self.calcRewardDatas( rewardDatas )
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

	def calcRewardDatas(self, rewardDatas):
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

SEActionBase.setActionClass("SEAction258", SEAction258)
SEActionBase.setActionClass("SEAction259", SEAction259)
SEActionBase.setActionClass("SEAction260", SEAction260)
SEActionBase.setActionClass("SEAction447", SEAction447)
