# -*- coding: utf-8 -*-

# 副本事件行为
import csdefine
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase



class SEAction429( SEActionBase ):
	"""
	帮会掠夺 设置某一方成功
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.belongType = int(section["param1"])	#0:进攻方 1:防守方

	def do( self, spaceEntity, triggerID, eventParams ):
		spaceEntity.setBelongTypeWin(self.belongType)

class SEAction446( SEActionBase ):
	"""
	活动开始后检查活动胜负情况
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.attackFlag = section["param1"]	#进攻方胜利发送消息
		self.protectFlag = section["param2"]	#防守方胜利发送消息

	def do( self, spaceEntity, triggerID, eventParams ):
		winnerType = spaceEntity.getWinnerType()
		if winnerType == csdefine.BELONG_SIDE_ATTACK:
			spaceEntity.getScript().onConditionChange(spaceEntity, "", spaceEntity.id, self.attackFlag, "")
		elif winnerType == csdefine.BELONG_SIDE_PROTECT:
			spaceEntity.getScript().onConditionChange(spaceEntity, "", spaceEntity.id, self.protectFlag, "")
	
class SEAction448( SEActionBase ):
	"""
	帮会掠夺 帮会商店的奖励
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.winnerRewardInfo = section["param1"]	#胜利方根据打赢的帮会等级获得奖励，level:giftID|level:giftID
		self.loserGiftID = section["param2"]	#帮贡和军功奖励，失败方礼包ID

	def do( self, spaceEntity, triggerID, eventParams ):
		belongType = spaceEntity.getWinnerTongBelongSide()
		attackTongDBID, protectTongDBID = spaceEntity.getBothSidesDBID()
		if belongType == csdefine.BELONG_SIDE_ATTACK:
			KBEngine.globalData["TongMgr"].tongPlunderResultReward(spaceEntity.base, attackTongDBID, protectTongDBID, self.winnerRewardInfo, self.loserGiftID)
		elif belongType == csdefine.BELONG_SIDE_PROTECT:
			KBEngine.globalData["TongMgr"].tongPlunderResultReward(spaceEntity.base, protectTongDBID, attackTongDBID, self.winnerRewardInfo, self.loserGiftID)


class SEAction459( SEActionBase ):
	"""
	帮会掠夺 触发者根据归属播放语音
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.attactSoundID = section["param1"]		#进攻方播放语音
		self.protectSoundID = section["param2"]	#防守方播放语音

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID, None)
		if trigger and trigger.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			belongType = trigger.getBelongSide()
			if belongType == csdefine.BELONG_SIDE_ATTACK:
				trigger.roleSpaceCopyPlaySound(self.attactSoundID)
			elif belongType == csdefine.BELONG_SIDE_PROTECT:
				trigger.roleSpaceCopyPlaySound(self.protectSoundID)
		
class SEAction467( SEActionBase ):
	"""
	帮会掠夺 设置活动是否允许玩家进入
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._status = int(section["param1"])		#0 不允许进入 1允许进入
		self._delayTime = float(section["param2"])#延迟时间

	def do( self, spaceEntity, triggerID, eventParams ):
		KBEngine.globalData["TongPlunderManager"].reqeustSetTongPlunderEnterStatus(self._status, self._delayTime)
		
class SEAction468( SEActionBase ):
	"""
	帮会掠夺 获得器械兑换券
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.itemIDList = section["param1"].split("|")
		self.amountList = []
		if section["param2"]:
			self.amountList = [int(i) for i in section["param2"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get( triggerID )
		if not trigger or trigger.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		for itemID in self.itemIDList:
			amount = 1
			index = self.itemIDList.index( itemID )
			if len( self.amountList ) > index:
				amount = self.amountList[index]
			trigger.addItemByID( int(itemID),amount,csdefine.ITEM_ADD_BY_SPACE_ACTION )
			
		spaceEntity.addVoucherRecord(trigger.playerDBID)



SEActionBase.setActionClass("SEAction429", SEAction429)
SEActionBase.setActionClass("SEAction446", SEAction446)
SEActionBase.setActionClass("SEAction448", SEAction448)
SEActionBase.setActionClass("SEAction459", SEAction459)
SEActionBase.setActionClass("SEAction467", SEAction467)
SEActionBase.setActionClass("SEAction468", SEAction468)