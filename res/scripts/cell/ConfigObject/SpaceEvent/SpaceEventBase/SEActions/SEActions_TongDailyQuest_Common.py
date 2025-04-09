# -*- coding: utf-8 -*-

# 副本事件行为
import time
import KBEDebug
import KBEngine
import Reward.RewardBasicValueData as RewardBase
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
from MsgLogger import g_logger
import LogDefine
from ConfigObject.Drop import DropItem
import csdefine
import csstatus
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr

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

class SEAction117(SEActionBase):
	"""
	副本计数奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.countKey = section["param1"]
		self.questID = section["param2"].strip()
		self.msgInfo = section["param3"].strip()
		self.countDown = 0
		if section["param4"]:
			self.countDown = int( section["param4"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		if self.countKey not in spaceEntity.spaceEventCountInt:
			KBEDebug.ERROR_MSG("param1 error!")
			return
		
		num = spaceEntity.spaceEventCountInt[ self.countKey ]
		rewardStr = ""
		for roleCell in spaceEntity._spaceRoles:
			roleCell.setTongDailyQuestTaskCompleteNum( num )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeScore = quest.getGradeScore( roleCell )
				contribute, money, barracksExp, xiuweiRatio, rewardID, buff = quest.getGradeReward( roleCell )
				xiuwei = int(RewardBase.datas.get(roleCell.getLevel(), {}).get("xiuwei", 0) * xiuweiRatio)
				
				if contribute > 0:
					rewardStr += "0:{}|".format(contribute) 
				if money > 0:
					rewardStr += "1:{}|".format(money)
				if barracksExp > 0:
					rewardStr += "2:{}|".format(barracksExp)
				if xiuwei > 0:
					rewardStr += "3:{}".format(xiuwei)
					
				if rewardID:
					itemStr = ""
					items = []
					rewardDatas = RewardMgr.g_rewardMgr.getReward(rewardID, {"player" : roleCell, "spaceLevel": spaceEntity.spaceLevel, })
					rewardItemDatas = calcRewardDatas( rewardDatas )
					for data in rewardItemDatas:
						itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
						if roleCell.addItem(itemInst, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT) != csstatus.ITEM_GO_ON:
							items.append( itemInst )
						
						if itemStr : itemStr += "|"
						itemStr += "{}:{}".format(itemInst.id, itemInst.getAmount())
						
					#没有加成功的物品通过邮件发送
					if len(items):
						roleCell.sendRemainItemWithMail(items, csdefine.REMAIN_ITEM_SPACE_COPY, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT)
				
				if buff:
					buffList = [int(buffID) for buffID in buff.split("|")]
					for buffID in buffList:
						roleCell.addBuff(roleCell, buffID)
					
				roleCell.client.ShowTongDailyQuestSpaceWin( self.msgInfo, str(num), rewardStr, gradeScore, self.countDown, itemStr, buff )

class SEAction425(SEActionBase):
	"""
	帮会日常任务副本通关(统计)
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
			roleCell.setTongDailyQuestTaskCompleteNum( num )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeScore = quest.getGradeScore( roleCell )
				contribute, money, barracksExp, xiuweiRatio, rewardID, buff = quest.getGradeReward( roleCell )
				xiuwei = int(RewardBase.datas.get(roleCell.getLevel(), {}).get("xiuwei", 0) * xiuweiRatio)
				
				if contribute > 0:
					rewardStr += "0:{}|".format(contribute) 
				if money > 0:
					rewardStr += "1:{}|".format(money)
				if barracksExp > 0:
					rewardStr += "2:{}|".format(barracksExp)
				if xiuwei > 0:
					rewardStr += "3:{}".format(xiuwei)
					
				itemStr = ""
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
						
					#没有加成功的物品通过邮件发送
					if len(items):
						roleCell.sendRemainItemWithMail(items, csdefine.REMAIN_ITEM_SPACE_COPY, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT)
				
				if buff:
					buffList = [int(buffID) for buffID in buff.split("|")]
					for buffID in buffList:
						roleCell.addBuff(roleCell, buffID)
					
				roleCell.client.ShowTongDailyQuestSpaceWin( self.msgInfo, str(num), rewardStr, gradeScore, self.countDown, itemStr, buff )

				#添加帮会日常任务副本通关日志
				useTime = int( time.time() - spaceEntity.lifeStartTime )
				if contribute > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_CONTRIBUTE, str(contribute), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				if money > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_MONEY, str(money), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				if barracksExp > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_BARRACKS_EXP, str(barracksExp), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				if xiuwei > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_XIUWEI, str(xiuwei), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)

class SEAction426(SEActionBase):
	"""
	帮会日常任务副本通关(时间)
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
			roleCell.setTongDailyQuestTaskCompleteNum( limtTime )
			if self.questID and self.msgInfo:
				quest = g_QuestLoader.getScript( int(self.questID) )
				gradeScore = quest.getGradeScore( roleCell )
				
				contribute, money, barracksExp, xiuweiRatio, rewardID, buff = quest.getGradeReward( roleCell )
				xiuwei = int(RewardBase.datas.get(roleCell.getLevel(), {}).get("xiuwei", 0) * xiuweiRatio)
				
				if contribute > 0:
					rewardStr += "0:{}|".format(contribute) 
				if money > 0:
					rewardStr += "1:{}|".format(money)
				if barracksExp > 0:
					rewardStr += "2:{}|".format(barracksExp)
				if xiuwei > 0:
					rewardStr += "3:{}|".format(xiuwei)
				
				_time = ""
				if int( useTime / 60 ):
					_time += str( int( useTime / 60 ) ) + "分"
				if useTime % 60:
					_time += str( useTime % 60 ) + "秒"
				
				itemStr = ""
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
						
					#没有加成功的物品通过邮件发送
					if len(items):
						roleCell.sendRemainItemWithMail(items, csdefine.REMAIN_ITEM_SPACE_COPY, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT)
				
				if buff:
					buffList = [int(buffID) for buffID in buff.split("|")]
					for buffID in buffList:
						roleCell.addBuff(roleCell, buffID)
				
				roleCell.client.ShowTongDailyQuestSpaceWin( self.msgInfo, _time, rewardStr, gradeScore, self.countDown, itemStr, buff )
				
				#添加帮会日常任务副本通关日志
				if contribute > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_CONTRIBUTE, str(contribute), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				if money > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_MONEY, str(money), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				if barracksExp > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_BARRACKS_EXP, str(barracksExp), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)
				if xiuwei > 0:
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_XIUWEI, str(xiuwei), spaceEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, spaceEntity.scriptID)


SEActionBase.setActionClass("SEAction117", SEAction117)
SEActionBase.setActionClass("SEAction425", SEAction425)
SEActionBase.setActionClass("SEAction426", SEAction426)
