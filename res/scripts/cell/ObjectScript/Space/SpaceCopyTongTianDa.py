# -*- coding: utf-8 -*-

import time
import KBEMath
import KBEDebug
import csdefine
import Const
import csconst
import Functions
import csstatus
import ItemTypeEnum
from ObjectScript.Space.SpaceCopy import SpaceCopy
from ConfigObject.SpaceCopyTTDRewardsLoader import g_SpaceCopyTTDRewards
from ConfigObject.SpaceCopyTTDRewardRatioLoader import g_SpaceCopyTTDRewardRatioLoader
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr

from MsgLogger import g_logger
import LogDefine

class SpaceCopyTongTianDa( SpaceCopy ):
	"""
	通天塔
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.buffList = []				# CST-11333，策划用于修正数值
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		
		buffList = configData["SpaceData"].get( "buffList", "" )
		if buffList:
			self.buffList = [ int(i) for i in buffList.split("|") ]

	def onEnter( self, selfEntity, playerRole, packArgs ):
		""""""
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.layerNumber = g_SpaceCopyTTDRewards.getLayerNumberByScriptID( self.scriptID )			# 因为策划可能会使用GM指令进入

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond, "onTongTinaDaSpaceFailure", () )
		selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))

	def showTimeCountDown( self, selfEntity, statusID, remainTime ):
		"""
		所有玩家显示读秒倒计时
		"""
		for roleCell in selfEntity._spaceRoles:
			if roleCell.getLevel() > roleCell.layerNumber:
				roleCell.statusMessage( statusID, remainTime )

	def onTongTinaDaSpaceFailure( self, selfEntity ):
		"""
		副本失败
		"""
		self.spaceEvent_onSpaceFailure( selfEntity )
		for roleCell in selfEntity._spaceRoles:
			roleCell.isChallenge = 1
			roleCell.client.TongTinaDaSpaceFailure( 0 )

	def onTongTinaDaSpaceSuccess( self, selfEntity, questID, taskID, lastLayerNumber ):
		"""
		副本成功
		"""
		useTime = time.time() - selfEntity.lifeStartTime
		self.spaceEvent_onSpaceSuccess( selfEntity )
		self.stopSpaceLife( selfEntity )
		for roleCell in selfEntity._spaceRoles:
			moneyRatio, expRatio, rewardRatio, extraRewardID = g_SpaceCopyTTDRewardRatioLoader.getRewardRatioData( str( roleCell.layerNumber - roleCell.getLevel() ) )
			money, exp, rewardID = g_SpaceCopyTTDRewards.getRewardData( str( roleCell.layerNumber), "topo" )
			finalMoney, finalExp = self.addMoneyAndExp( roleCell, money, exp, moneyRatio, expRatio )
			itemList1 = self.getTongTinaDaSpaceReward( selfEntity, roleCell, rewardID, rewardRatio )
			itemList2 = self.getTongTinaDaSpaceReward( selfEntity, roleCell, extraRewardID, rewardRatio )
			finalItemList = itemList1 + itemList2
			
			if roleCell.layerNumber == g_SpaceCopyTTDRewards.getMaxLayerNumber():
				roleCell.isChallenge = 1
				roleCell.client.TongTinaDaSpaceSuccess( finalMoney, finalExp, finalItemList, 2 )
			else:
				roleCell.client.TongTinaDaSpaceSuccess( finalMoney, finalExp, finalItemList, 0 )
			roleCell.layerNumber += 1
			
			g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
			LogDefine.ACTIVE_REWARD_TYPE_MONEY, str(finalMoney), selfEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, self.scriptID)
			
			g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
			LogDefine.ACTIVE_REWARD_TYPE_EXP, str(finalExp), selfEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, self.scriptID)
	

	def getTongTinaDaSpaceReward( self, selfEntity, roleCell, rewardID, rewardRatio ):
		"""
		获取奖励
		"""
		useTime = time.time() - selfEntity.lifeStartTime
		itemList = ""
		if rewardID:
			datas = RewardMgr.g_rewardMgr.getReward( rewardID, { "player":roleCell, "ratio":rewardRatio } )
			failAddItem = RewardMgr.g_rewardMgr.doRewards( datas, roleCell.id, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT )
			if failAddItem:
				roleCell.sendRemainItemWithMail( failAddItem, csdefine.REMAIN_ITEM_TONG_TIAN_TA, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT )
			for data in datas:
				if data["type"] == csdefine.REWARD_TYPE_ITEM:
					itemList += str( data["goodsid"]) + ":" + str(data["amount"] ) + "|"
					
					g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), 
					LogDefine.ACTIVE_REWARD_TYPE_ITEM, str(data["goodsid"]), selfEntity.lifeStartTime, useTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, self.scriptID)
			
		return itemList

	def addMoneyAndExp( self, roleCell, money, exp, moneyRatio, expRatio ):
		"""
		金币经验奖励
		"""
		finalMoney = int( money * moneyRatio )
		finalExp = int( exp * expRatio )
		roleCell.addMoney( finalMoney, csdefine.MONEY_ADD_REASON_SPACE_SENTLEMENT )
		roleCell.addExp( finalExp, csdefine.EXP_ADD_REASON_SPACE_SENTLEMENT )
		return finalMoney, finalExp
		
	def addShengJieItemNotify(self, selfEntity, itemInst, dropRewardOrSpaceReward, role, params):
		"""
		玩家在地图中获得圣阶物品通知
		dropRewardOrSpaceReward: 掉落:0 / 副本奖励:1
		"""
		if itemInst is None:
			return
		
		#杀怪掉落
		if dropRewardOrSpaceReward == 0:
			scriptID = params.get("scriptID", "")
			bossIDList = self._bossScriptIDList if len(self._bossScriptIDList) else self._bossIDForMessageList
			if scriptID in bossIDList:
				bossName = params.get("name", "")
				messageArg = "{}|{}|{}|{}".format(role.getName(), (selfEntity.spaceLevel - role.level), self.getSpaceName(), bossName, itemInst.getItemDir("ItemName"))
				selfEntity.globalWorld(csstatus.ITEM_ADD_IN_SPACE_WIN_BOSS_IN_TONGTIANTA, messageArg)
			else:
				messageArg = "{}|{}|{}".format(role.getName(), self.getSpaceName(), itemInst.getItemDir("ItemName"))
				selfEntity.globalWorld(csstatus.ITEM_ADD_IN_SPACE, messageArg)
		else:
			messageArg = "{}|{}|{}".format(role.getName(), self.getSpaceName(), itemInst.getItemDir("ItemName"))
			selfEntity.globalWorld(csstatus.ITEM_ADD_IN_SPACE, messageArg)
		
			if role.getClient():
				role.client.CLIENT_PlaySound(Const.SHENGJIE_ITEM_GET_SOUND)
				role.client.CLIENT_PlayEffect(Const.SHENGJIE_ITEM_GET_EFFECTID)
			
