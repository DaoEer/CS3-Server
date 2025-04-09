# -*- coding: utf-8 -*-

# 副本事件行为  晶石狩猎场
import Math
import Define
import csdefine
import csconst
import csstatus
import random
import KBEMath
import KBEDebug
import KBEngine
import Functions
import time
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase


class SEAction80( SEActionBase ):
	"""
	晶石狩猎场 玩家被击杀获得积分(金精)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._ratio = float(section["param1"])

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		spaceEntity.getScript().spaceEvent_addCount( spaceEntity,dieEntity.id,1 )
		dieEntityIntegral = spaceEntity.memberDatas.getIntegral(triggerID)
		if dieEntityIntegral == None:
			return
		integral = int(self._ratio * dieEntityIntegral)
		spaceEntity.reducePlayerIntegral( dieEntity, integral )
		spaceEntity.addPlayerIntegral( killEntity,integral, True )

class SEAction81( SEActionBase ):
	"""
	晶石狩猎场 击杀超过某次数,玩家获得Buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._count = int( section["param1"] )
		self._buffID = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if eventParams["newValue"] > self._count:
			entity = KBEngine.entities.get( eventParams["countKey"], None )
			if not entity:
				return
			entity.addBuff(entity,self._buffID)

class SEAction105( SEActionBase ):
	"""
	晶石狩猎场 点晶石销毁销毁对应陷阱
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		boxEntity = KBEngine.entities.get(eventParams["entityID"])
		if not boxEntity:
			return
		trapID = boxEntity.queryTemp("trapID")
		if not trapID:
			return
		trapEntity = KBEngine.entities.get(trapID,None)
		if not trapEntity:
			return
		spaceEntity = trapEntity.getCurrentSpace()
		data = trapEntity.queryTemp("rewardCamp")
		if spaceEntity:
			spaceEntity.campTotalMoney( data[0],trapEntity.queryTemp("rewardMoney") )
		trapEntity.destroySelf()

class SEAction106( SEActionBase ):
	"""
	晶石狩猎场 随机刷点晶石
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.spawnList = section["param1"].split("|")	#刷新点的Index "1;2;3|4;5;6"
		self.index = int(section["param2"])		#区间 填1 表示在 1;2;3中取，填2 表示 在1;2;3;4;5;6中取
		self.spawnAmount = [int(amount) for amount in section["param3"].split("|")] #生成数量 也是根据区间来定

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		totalSpawnIndex = []
		for i in range(0,self.index):
			totalSpawnIndex.extend([int(data) for data in self.spawnList[i].split(";")])
		amount = self.spawnAmount[self.index - 1]
		if len(totalSpawnIndex) < amount:
			KBEDebug.ERROR_MSG("SEAction106 config is error")
			return
		random.shuffle(totalSpawnIndex)
		spawnPointList = random.sample(totalSpawnIndex,amount)
		for index in spawnPointList:
			entity = spaceEntity.onRequestSpawnEntity(index)

class SEAction107( SEActionBase ):
	"""
	晶石狩猎场 玩家被击杀/击杀数增加
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		spaceEntity.memberDatas.kill( triggerID, eventParams["killerID"] )

class SEAction114( SEActionBase ):
	"""
	晶石狩猎场 强制弹出金钱排名
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.client.CLIENT_ShowRankList()

class SEAction422( SEActionBase ):
	"""
	CST-11308 晶石狩猎场机缘玩法，记录当前时间
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._tempName = section["param1"] #记录标签名字
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
			
		spaceEntity.setTemp(self._tempName + "_time", time.time())
		
class SEAction423( SEActionBase ):
	"""
	CST-11308 晶石狩猎场机缘玩法，根据时间获得金精奖励
	@param1: 记录标签名字
	@param2: 时间奖励配置，时间:奖励金精数|时间:奖励金精数...
	"""
	def init( self, section ):
		
		SEActionBase.init( self, section )
		self._tempName = section["param1"] 
		self._integralRewardInfo = {}
		for rewardInfo in section["param2"].split("|"):
			t, value = rewardInfo.split(":")
			self._integralRewardInfo[int(t)] = int(value)
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
			
		tempTime = spaceEntity.queryTemp(self._tempName + "_time", 0)
		if not tempTime:
			KBEDebug.ERROR_MSG("SEAction423 confit param1 error")
			return
		
		value = 0
		timekeys = list(self._integralRewardInfo.keys())
		timekeys.sort()
		subTime = int(time.time() - tempTime)
		for key in timekeys:
			if subTime <= key:
				value  = self._integralRewardInfo[key]
				break
		if value > 0:
			for player in spaceEntity._spaceRoles:
				player.addSparHunTingIntegral(value)

class SEAction455( SEActionBase ):
	"""
	CST-11308 晶石狩猎场机缘玩法结算
	"""
	def init( self, section ):
		SEActionBase.init( self, section)
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
			
		spaceEntity.JSSLC_JiYuanSpaceCopyJieSuan()

class SEAction471( SEActionBase ):
	"""
	CST-13721 晶石狩猎场 击杀功勋奖励
	"""
	def init(self, section):
		SEActionBase.init(self, section)

	def do(self, spaceEntity, triggerID, eventParams):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID, None)
		killEntity = KBEngine.entities.get(eventParams["killerID"], None)
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		amount = spaceEntity.getScript().getKillRoleFeat()
		killEntity.addFeatsRecord(amount, csdefine.FEATS_ADD_REASON_JSSLC_KILL_ROLE)	#记录增加
			

SEActionBase.setActionClass("SEAction80", SEAction80)
SEActionBase.setActionClass("SEAction81", SEAction81)
SEActionBase.setActionClass("SEAction105", SEAction105)
SEActionBase.setActionClass("SEAction106", SEAction106)
SEActionBase.setActionClass("SEAction107", SEAction107)
SEActionBase.setActionClass("SEAction114", SEAction114)
SEActionBase.setActionClass("SEAction422", SEAction422)
SEActionBase.setActionClass("SEAction423", SEAction423)
SEActionBase.setActionClass("SEAction455", SEAction455)
SEActionBase.setActionClass("SEAction471", SEAction471)