# -*- coding: utf-8 -*-

# 副本结算类

import KBEDebug
import csdefine
from SmartImport import smartImport


SCRIPT_PASS_TIME		= "Settlement_PassTime"
SCRIPT_RECEIVE_DAMAGE	= "Settlement_ReceiveDamage"
SCRIPT_DIE_AMOUNT		= "Settlement_DieAmount"
SCRIPT_CHILD_SPACE_FAILURE = "Settlement_childSpaceFailure"

SCORE_LEVEL_TS = 1	#通神
SCORE_LEVEL_CF = 2	#超凡
SCORE_LEVEL_WD = 3	#问鼎
SCORE_LEVEL_CC = 4	#出尘
SCORE_LEVEL_RD = 5	#入道
SCORE_LEVEL_FAILURE = 6	#未通关


class SpaceSettlementObj:
	def __init__( self ):
		self.score_ts = 0			#通神分数线
		self.score_cf = 0			#超凡分数线
		self.score_wd = 0			#问鼎分数线
		self.score_cc = 0			#出尘分数线
		self.reward_ts = ""
		self.reward_cf = ""
		self.reward_wd = ""
		self.reward_cc = ""
		self.reward_rd = ""
		self.scoreBasisItems = []	#评分项

	def init( self, spaceObj, section ):
		"""
		加载AI配置
		"""
		#分数线
		self.score_ts = int( section["score_ts"] )
		self.score_cf = int( section["score_cf"] )
		self.score_wd = int( section["score_wd"] )
		self.score_cc = int( section["score_cc"] )
		if not self.score_ts > self.score_cf > self.score_wd > self.score_cc:
			KBEDebug.ERROR_MSG( "Space settlement score line config error!", spaceObj.scriptID )
		
		#奖励ID
		self.reward_ts = section["reward_ts"]
		self.reward_cf = section["reward_cf"]
		self.reward_wd = section["reward_wd"]
		self.reward_cc = section["reward_cc"]
		self.reward_rd = section["reward_rd"]
		
		#通关时间
		try:
			scriptClass = smartImport( "ConfigObject.SpaceSettlement.SpaceSettlementItem:" + SCRIPT_PASS_TIME )
		except ImportError:
			KBEDebug.ERROR_MSG( "SpaceSettlement import error! script: %s. "%SCRIPT_PASS_TIME, spaceObj.scriptID )
		else:
			objectItem = scriptClass()
			index = len(self.scoreBasisItems)
			title = "通关时间"
			params = "%s|%s"%( section["passTime_value"], section["passTime_score"] )
			objectItem.init( index, title, params )
			self.scoreBasisItems.append( objectItem )
		
		#接受伤害
		try:
			scriptClass = smartImport( "ConfigObject.SpaceSettlement.SpaceSettlementItem:" + SCRIPT_RECEIVE_DAMAGE )
		except ImportError:
			KBEDebug.ERROR_MSG( "SpaceSettlement import error! script: %s. "%SCRIPT_RECEIVE_DAMAGE, spaceObj.scriptID )
		else:
			objectItem = scriptClass()
			index = len(self.scoreBasisItems)
			title = "收到伤害"
			params = "%s|%s"%( section["receiveDamage_value"], section["receiveDamage_score"] )
			objectItem.init( index, title, params )
			self.scoreBasisItems.append( objectItem )
		
		#死亡次数
		try:
			scriptClass = smartImport( "ConfigObject.SpaceSettlement.SpaceSettlementItem:" + SCRIPT_DIE_AMOUNT )
		except ImportError:
			KBEDebug.ERROR_MSG( "SpaceSettlement import error! script: %s. "%SCRIPT_DIE_AMOUNT, spaceObj.scriptID )
		else:
			objectItem = scriptClass()
			index = len(self.scoreBasisItems)
			title = "死亡次数"
			params = "%s"%( section["dieAmount_score"] )
			objectItem.init( index, title, params )
			self.scoreBasisItems.append( objectItem )
			
		#子副本失败次数
		try:
			scriptClass = smartImport( "ConfigObject.SpaceSettlement.SpaceSettlementItem:" + SCRIPT_CHILD_SPACE_FAILURE )
		except ImportError:
			KBEDebug.ERROR_MSG( "SpaceSettlement import error! script: %s. "%SCRIPT_CHILD_SPACE_FAILURE, spaceObj.scriptID )
		else:
			objectItem = scriptClass()
			index = len(self.scoreBasisItems)
			title = "战斗失败"
			params = "%s"%( section["childSpaceFailure_score"] )
			objectItem.init( index, title, params )
			self.scoreBasisItems.append( objectItem )
		
		
		#其他加分项
		for NUM in range(1,6):
			scriptAndTitle = section["%i_script"%NUM]
			if not scriptAndTitle:
				continue
			
			scriptStr, title = scriptAndTitle.split("|")
			try:
				scriptClass = smartImport( "ConfigObject.SpaceSettlement.SpaceSettlementItem:" + scriptStr )
			except ImportError:
				KBEDebug.ERROR_MSG( "SpaceSettlement import error! script: %s. "%scriptStr, spaceObj.scriptID )
			else:
				objectItem = scriptClass()
				index = len(self.scoreBasisItems)
				objectItem.init( index, title, section["%i_params"%NUM] )
				self.scoreBasisItems.append( objectItem )

	def getLinkEvents( self ):
		"""
		获取关联的事件
		"""
		result = []
		for item in self.scoreBasisItems:
			type = item.getEventType()
			if type not in result:
				result.append( item.getEventType() )
		return result

	def caculateScore( self, spaceEntity ):
		"""
		计算得分
		"""
		score = 0
		for item in self.scoreBasisItems:
			score += item.getScore( spaceEntity )
		return int(score)

	def caculateScoreLevel( self, score ):
		"""
		计算得分档次
		"""
		if score >= self.score_ts:
			return SCORE_LEVEL_TS
		elif score >= self.score_cf:
			return SCORE_LEVEL_CF
		elif score >= self.score_wd:
			return SCORE_LEVEL_WD
		elif score >= self.score_cc:
			return SCORE_LEVEL_CC
		else:
			return SCORE_LEVEL_RD
		return 0

	def getShowInfo( self, spaceEntity ):
		"""
		获取显示信息
		"""
		titleList = []
		valueList = []
		for item in self.scoreBasisItems:
			titleList.append( item.getTitle() )
			valueList.append( str( item.getRecord( spaceEntity ) ) )
		return (titleList, valueList)
	
	def setScore( self, spaceEntity, score ):
		"""
		"""
		spaceEntity.settlementScore = score
	
	def getScore( self, spaceEntity ):
		return spaceEntity.settlementScore
	
	def setScoreLevel( self, spaceEntity, level ):
		"""
		设置评分等级
		"""
		spaceEntity.settlementScoreLevel = level
	
	def getScoreLevel( self, spaceEntity ):
		"""
		获取评分等级
		"""
		return spaceEntity.settlementScoreLevel
	
	def hasScoreLevel( self, spaceEntity ):
		"""
		已经结算
		"""
		return spaceEntity.settlementScoreLevel != -1
	
	def getRewardID( self, spaceEntity ):
		"""
		根据评分等级获取奖励编号
		"""
		if spaceEntity.settlementScoreLevel == SCORE_LEVEL_TS:
			return self.reward_ts
		if spaceEntity.settlementScoreLevel == SCORE_LEVEL_CF:
			return self.reward_cf
		if spaceEntity.settlementScoreLevel == SCORE_LEVEL_WD:
			return self.reward_wd
		if spaceEntity.settlementScoreLevel == SCORE_LEVEL_CC:
			return self.reward_cc
		if spaceEntity.settlementScoreLevel == SCORE_LEVEL_RD:
			return self.reward_rd
		return ""
	
	def onPlayerDie( self, spaceEntity ):
		"""
		玩家死亡
		"""
		if self.hasScoreLevel( spaceEntity ):
			return
		
		for item in self.scoreBasisItems:
			if item.getEventType() == csdefine.SPACE_STMT_ROLE_DIE:
				item.addRecord( spaceEntity )
	
	def onPlayerReceiveDamage( self, spaceEntity, damageValue ):
		"""
		玩家接受伤害
		"""
		if self.hasScoreLevel( spaceEntity ):
			return
		
		for item in self.scoreBasisItems:
			if item.getEventType() == csdefine.SPACE_STMT_RECEIVE_DAMAGE:
				item.addRecord( spaceEntity, value = damageValue )
	
	def onChildSpaceFailure(self, spaceEntity):
		"""
		子副本通关失败
		"""
		if self.hasScoreLevel( spaceEntity ):
			return
		
		for item in self.scoreBasisItems:
			if item.getEventType() == csdefine.SPACE_STMT_CHILD_SPACE_FAILURE:
				item.addRecord( spaceEntity )
	
	
	def onTriggerBox( self, spaceEntity, boxScriptID ):
		"""
		触发箱子
		"""
		if self.hasScoreLevel( spaceEntity ):
			return
		
		for item in self.scoreBasisItems:
			if item.getEventType() == csdefine.SPACE_STMT_TRIGGER_BOX:
				item.addRecord( spaceEntity, param = boxScriptID )
	
	def onSpaceSuccess( self, spaceEntity ):
		"""
		副本通关
		"""
		if self.hasScoreLevel( spaceEntity ):
			return
		
		for item in self.scoreBasisItems:
			if item.getEventType() == csdefine.SPACE_STMT_SPACE_SUCCESS:
				item.addRecord( spaceEntity )
		
		score = self.caculateScore( spaceEntity )
		self.setScore( spaceEntity, score )
		scoreLevel = self.caculateScoreLevel( score )
		self.setScoreLevel( spaceEntity, scoreLevel )
		KBEDebug.DEBUG_MSG( "Space(%s) settlement result. score: %s, scoreLevel: %s."%( spaceEntity.id, score, scoreLevel ) )
	
	def onSpaceFailure( self, spaceEntity ):
		"""
		副本失败
		"""
		if self.hasScoreLevel( spaceEntity ):
			return
		self.setScoreLevel( spaceEntity, SCORE_LEVEL_FAILURE )
		KBEDebug.DEBUG_MSG( "Space(%s) settlement result. scoreLevel: %s."%( spaceEntity.id, SCORE_LEVEL_FAILURE ) )