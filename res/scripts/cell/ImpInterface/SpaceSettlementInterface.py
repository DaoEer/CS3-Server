# -*- coding: utf-8 -*-

# 副本结算接口

import time
import random
import Define
import csdefine
import csstatus
import KBEDebug
import KBEngine
import ItemFactory
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr

from ConfigObject.SpaceSettlement.SpaceSettlementObj import SpaceSettlementObj
from SpaceSettlementConfig import Datas as g_settmentConfig
from MsgLogger import g_logger
import LogDefine

VALUE_TYPE_REASON = {
	csdefine.REWARD_TYPE_MONEY		: csdefine.MONEY_ADD_REASON_SPACE_SENTLEMENT,		# 金币奖励
	csdefine.REWARD_TYPE_EXP		: csdefine.EXP_ADD_REASON_SPACE_SENTLEMENT,			# 经验奖励
	csdefine.REWARD_TYPE_XIUWEI		: csdefine.XIUWEI_ADD_REASON_SPACE_SENTLEMENT,		# 修为奖励
	csdefine.REWARD_TYPE_POTENTIAL	: csdefine.POTENTIAL_ADD_REASON_SPACE_SENTLEMENT,	# 潜能奖励
	csdefine.REWARD_TYPE_ITEM		: csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT,			# 物品奖励
}

REWARD_BOX_NUM = 6	#奖励箱子数量
AUTO_CHOOSE_REWARD_TIME = 30	#自动选择宝箱时间

SPACE_PASS_LEVEL_RD = 1 #入道
SPACE_PASS_LEVEL_CC = 2 #出尘
SPACE_PASS_LEVEL_WD = 3 #问鼎
SPACE_PASS_LEVEL_CF = 4	#超凡

class SpaceSettlementInterface:
	"""
	"""
	def __init__( self ):
		self._settlementObj = None

	def initData( self, configData ):
		"""
		virtual method
		"""
		if self.scriptID not in g_settmentConfig:
			return
		obj = SpaceSettlementObj()
		obj.init( self, g_settmentConfig[ self.scriptID ] )
		self._settlementObj = obj

	def spaceSettlement_onPlayerEnter( self, selfEntity, playerMB ):
		"""
		玩家进副本
		"""
		if not self._settlementObj:
			return
		playerMB.cell.spaceSettlement_addEvent( self._settlementObj.getLinkEvents() )

	def spaceSettlement_onPlayerLeave( self, selfEntity, playerMB ):
		"""
		玩家出副本
		"""
		if not self._settlementObj:
			return
		playerMB.cell.spaceSettlement_clearEvent()

	def spaceSettlement_onPlayerDie( self, selfEntity ):
		"""
		玩家死亡
		"""
		if not self._settlementObj:
			return
		self._settlementObj.onPlayerDie( selfEntity )

	def spaceSettlement_onChildSpaceFailure( self, selfEntity ):
		"""
		子副本失败
		"""
		if not self._settlementObj:
			return
		self._settlementObj.onChildSpaceFailure( selfEntity )

	def spaceSettlement_onReceiveDamage( self, selfEntity, value ):
		"""
		玩家接受伤害
		"""
		if not self._settlementObj:
			return
		self._settlementObj.onPlayerReceiveDamage( selfEntity, value )

	def spaceSettlement_onTriggerBox( self, selfEntity, boxScriptID ):
		"""
		触发箱子
		"""
		if not self._settlementObj:
			return
		self._settlementObj.onTriggerBox( selfEntity, boxScriptID )

	def spaceSettlement_onSpaceSuccess( self, selfEntity ):
		"""
		副本通关
		"""
		if not self._settlementObj:
			return
		self._settlementObj.onSpaceSuccess( selfEntity )
		self.spaceSettlement_showResult( selfEntity )
		selfEntity.addTimerCallBackForScript( AUTO_CHOOSE_REWARD_TIME, "spaceSettlement_autoReward", () )

	def spaceSettlement_onSpaceFailure( self, selfEntity ):
		"""
		副本失败
		"""
		if not self._settlementObj:
			return
		self._settlementObj.onSpaceFailure( selfEntity )
		self.spaceSettlement_showResult( selfEntity )

	def spaceSettlement_showResult( self, selfEntity ):
		"""
		显示结算界面
		"""
		score = self._settlementObj.getScore( selfEntity )
		scoreLevel = self._settlementObj.getScoreLevel( selfEntity )
		dataInfo = self._settlementObj.getShowInfo( selfEntity )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceSettlementWin( score, scoreLevel, dataInfo[0], dataInfo[1] )

	def spaceSettlement_openRewdBox( self, selfEntity, playerMB, playerName, boxIndex ):
		"""
		玩家开宝箱
		"""
		if boxIndex not in range(REWARD_BOX_NUM):	#箱子下标非法
			return
		
		if boxIndex in selfEntity.settlementRewardRecd:
			return
		
		for boxIndex, info in selfEntity.settlementRewardRecd.items():
			if playerName == info["playerName"]:
				return
		
		rewardID = self._settlementObj.getRewardID( selfEntity )
		if not rewardID:
			return
		
		player = KBEngine.entities.get( playerMB.id )
		if not player or not player.isReal():
			return
		
		if selfEntity.settlementLockReward:
			return
		
		selfEntity.settlementLockReward = 1		#加个锁，避免多个玩家同时开宝箱
		self.__doRewardToPlayer( selfEntity, rewardID, boxIndex, player )
		selfEntity.settlementLockReward = 0

	def spaceSettlement_autoReward( self, selfEntity ):
		"""
		自动给未选择奖励的玩家分配奖励
		"""
		if selfEntity.settlementLockReward:
			selfEntity.addTimerCallBackForScript( 0.1, "spaceSettlement_autoReward", () )	#有人在选，那我待会再来
			return
		selfEntity.settlementLockReward = 1
		
		rewardID = self._settlementObj.getRewardID( selfEntity )
		if not rewardID:
			return
		
		hasChooseIndex = []
		hasChoosePlayer = []
		for boxIndex, info in selfEntity.settlementRewardRecd.items():
			hasChooseIndex.append( boxIndex )
			hasChoosePlayer.append( info["playerName"] )
		
		remainBoxIndex = list( set(range(REWARD_BOX_NUM)) ^ set(hasChooseIndex) )
		if len(remainBoxIndex) == 0:	#没有剩余的箱子了
			return
		
		# 在副本内未选的玩家，系统自动选
		for e in selfEntity._spaceRoles:
			if e.getName() in hasChoosePlayer:
				continue
			index = random.choice( remainBoxIndex )
			self.__doRewardToPlayer( selfEntity, rewardID, index, e )
			remainBoxIndex.remove( index )
			hasChoosePlayer.append( e.getName() )
			if len(remainBoxIndex) == 0:
				break
		
		# 给不在副本内的玩家发邮件
		# 开出剩余的箱子
		for index in remainBoxIndex:
			self.__openRemainRewdBox( selfEntity, rewardID, index )

	def __doRewardToPlayer( self, selfEntity, rewardID, boxIndex, player ):
		"""
		将某个箱子奖励给某玩家
		"""
		_values = []			#开出的数值奖励
		_items = []				#开出的物品奖励
		_recordData = []		#开出的奖励记录到副本
		_playerName = player.getName()
		
		# 奖励
		self.__getRewardDatas( rewardID, _values, _items, player )
		for data in _values:
			RewardMgr.g_rewardMgr.doReward( data, player.id, VALUE_TYPE_REASON[ data["type"] ] )
			_recordData.append( (data["type"], data["amount"]) )

		if player.addItemListCheck(_items) == csstatus.ITEM_GO_ON:
			for data in _items:
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem( data["goodsid"], data["amount"] )
				player.addItem( itemInst, VALUE_TYPE_REASON[ data["type"] ] )
				_recordData.append( (data["type"], data["goodsid"], data["amount"] ) )
		else:
			for data in _items:
				_recordData.append((data["type"], data["goodsid"], data["amount"]))
			player.sendRemainItemWithMail(_items, csdefine.REMAIN_ITEM_SPACE_COPY, VALUE_TYPE_REASON[ data["type"] ], selfEntity.getSpaceName())


		# 添加记录
		if boxIndex not in selfEntity.settlementRewardRecd:
			selfEntity.settlementRewardRecd[ boxIndex ] = { "playerName":_playerName, "rewardInfo":_recordData }
		
		# 通知客户端
		for e in selfEntity._spaceRoles:
			e.client.UpdateSpaceSettlementRewdBox( boxIndex, _playerName, self.__getBoxRewardClientDatas(_recordData) )

	def __openRemainRewdBox( self, selfEntity, rewardID, boxIndex ):
		"""
		打开多出来的宝箱
		"""
		_values = []			#开出的数值奖励
		_items = []				#开出的物品奖励
		_recordData = []		#开出的奖励记录到副本
		_playerName = ""
		
		# 获取奖励
		self.__getRewardDatas( rewardID, _values, _items, None )
		for data in _values:
			_recordData.append( (data["type"], data["amount"]) )
		for data in _items:
			_recordData.append( (data["type"], data["goodsid"], data["amount"] ) )
		
		# 添加记录
		if boxIndex not in selfEntity.settlementRewardRecd:
			selfEntity.settlementRewardRecd[ boxIndex ] = { "playerName":_playerName, "rewardInfo":_recordData }
		
		# 通知客户端
		for e in selfEntity._spaceRoles:
			e.client.UpdateSpaceSettlementRewdBox( boxIndex, _playerName, self.__getBoxRewardClientDatas(_recordData) )

	def __getRewardDatas( self, rewardID, rewardValues, rewardItems, owner = None ):
		"""
		根据奖励ID提取奖励数据
		"""
		params = {}
		if owner != None:
			params[ "player" ] = owner
		
		dataList = RewardMgr.g_rewardMgr.getReward( rewardID, params )
		if not dataList:
			return
		
		for data in dataList:
			if data["type"] == csdefine.REWARD_TYPE_NOTHING:
				continue
			
			if data["type"] == csdefine.REWARD_TYPE_ITEM:			#物品奖励
				rewardItems.append( data )
			
			else:													#数值奖励
				rewardValues.append( data )

	def __getBoxRewardClientDatas( self, recordData ):
		"""
		将某个箱子的奖励打包成客户端显示数据
		"""
		resultList = []
		for tempTuple in recordData:
			if tempTuple[0] == csdefine.REWARD_TYPE_ITEM:
				resultList.append( "%s|%s|%s" % ( tempTuple[0], tempTuple[1], tempTuple[2] ) )
			else:
				resultList.append( "%s|%s" % ( tempTuple[0], tempTuple[1] ) )
		return resultList

#---------------------------第二版 副本结算 JIRA 6369------------------------------
	def spaceSettlement_onAddPotential( self, selfEntity, playerRole, potential ):
		"""
		记录玩家增加的潜能
		"""
		if selfEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_POTENTIAL:
			if playerRole.playerDBID not in selfEntity.recordAddPotential:
				selfEntity.recordAddPotential[playerRole.playerDBID] = potential
			else:
				selfEntity.recordAddPotential[playerRole.playerDBID] += potential

	def spaceSettlement_onAddExp( self,selfEntity, playerRole, exp ):
		"""
		记录玩家增加的经验
		"""
		if selfEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_CHUAN_CHENG:
			if playerRole.playerDBID not in selfEntity.recordAddExp:
				selfEntity.recordAddExp[playerRole.playerDBID] = exp
			else:
				selfEntity.recordAddExp[playerRole.playerDBID] += exp

	def spaceSettlement_onPlayerDie6369( self, selfEntity ):
		"""
		记录玩家的死亡次数
		"""
		if selfEntity.getScript().getSpaceType() in [csdefine.SPACE_TYPE_POTENTIAL,csdefine.SPACE_TYPE_CHUAN_CHENG, csdefine.SPACE_TYPE_JSSLC_CHANCE_COPY]:
			selfEntity.recordPlayerDieNumber += 1

	def spaceSettlement_onSpaceSuccess6369( self, selfEntity ):
		"""
		副本通关 显示结算界面
		"""
		if selfEntity.getScript().getSpaceType() not in [csdefine.SPACE_TYPE_POTENTIAL,csdefine.SPACE_TYPE_CHUAN_CHENG]:
			return
		costTime = int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
		time = selfEntity.lifeTime/4
		level = None
		if costTime > 0 and costTime <= time:
			level = SPACE_PASS_LEVEL_CF
		elif costTime > time and costTime <= (time * 2):
			level = SPACE_PASS_LEVEL_WD
		elif costTime > (time*2) and costTime <= (time*3):
			level = SPACE_PASS_LEVEL_CC
		else:
			level = SPACE_PASS_LEVEL_RD

		if selfEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_POTENTIAL:
			rewardValue = selfEntity.recordAddPotential
			rewardType = csdefine.SPACE_TYPE_POTENTIAL
		else:
			rewardValue = selfEntity.recordAddExp
			rewardType = csdefine.SPACE_TYPE_CHUAN_CHENG
		for role in selfEntity._spaceRoles:
			if role.playerDBID in rewardValue:
				value = rewardValue[role.playerDBID]
			else:
				value = 0
			if selfEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_CHUAN_CHENG:
				g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, role.accountDBID, role.playerDBID,
									  role.getLevel(), LogDefine.ACTIVE_REWARD_TYPE_EXP, str(value),
										  selfEntity.lifeStartTime, costTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS,
										selfEntity.scriptID)
			if selfEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_POTENTIAL:
				g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, role.accountDBID, role.playerDBID,
										  role.getLevel(), LogDefine.ACTIVE_REWARD_TYPE_POTENTIAL, str(value),
										  selfEntity.lifeStartTime, costTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS,
										  selfEntity.scriptID)
			if role.getClient():
				role.client.CLIENT_ShowSpaceSettlementWin(rewardType, value, int(costTime), selfEntity.recordPlayerDieNumber, level )


