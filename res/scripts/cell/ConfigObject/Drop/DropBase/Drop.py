# -*- coding- : utf-8 -*-

import KBEDebug
import csdefine
import random
import Define
import Math
import copy
from ConfigObject.Drop.DropBase import DropType

from ConfigObject.Reward.RewardBase import RewardMgr

DROP_TYPE_DIRECT	=	1	#直接获得
DROP_TYPE_DROPBOX	=	2	#能过掉落箱子去拾取


def getRewardForRate( rate ):
	"""
	基于概率生成奖励
	"""
	if rate >= 1.0:
		return True
		
	x = random.uniform(0,1)
	if x <= rate:
		return True
	else:
		return False
		
def getRewardForWeight( rewardIndexs, weightList ):
	"""
	基于权重获取
	"""
	weightValue = 0
	sumWeight = 0
	for value in weightList:
		sumWeight += value
	x = random.randint( 0, sumWeight )
	for index, weight in zip( rewardIndexs, weightList ):
		weightValue += weight
		if x < weightValue:
			return index
	return -1

class Drop( object ):
	def __init__( self, dtConfig ):
		self.initData( dtConfig )

	def initData( self, dtConfig ):
		#DItemBase.initData( self, dtConfig )
		self._dropDatas = dtConfig
		#怪物所有权
		self.ownership = dtConfig.get("ownership", Define.MONSTER_OWNER_FIRST_DAMAGE)
		#宝箱编号
		self.dropBoxID = dtConfig.get("dropBoxID", "")
		
		self._dropValuesDatas = {}
		self._dropItemDatas = []
		self._dropPetDatas = {}
		self._allocationItemDatas = {}
		self._allocationDatas = {}
	
	def getDropItemDict( self ):
		"""获取掉落物品 {itemID:amount}"""
		temp = {}
		for data in self._dropItemDatas:
			if data["type"] == "item":
				if not data["goodsid"] in temp:
					temp[data["goodsid"]] = 0
				temp[data["goodsid"]] += data["amount"]
		return temp
	
	def onDrop( self, dieEntity, killer, args ):
		"""
		分别执行直接掉落和掉落到宝箱
		"""
		DropType.DTypeBase.getObject( DROP_TYPE_DIRECT )( self._dropValuesDatas, {} ).doDrop( self._allocationDatas, dieEntity, killer, args )
		DropType.DTypeBase.getObject( DROP_TYPE_DROPBOX )( self._dropItemDatas, {"dropBoxID" : self.dropBoxID} ).doDrop( self._allocationItemDatas, dieEntity, killer, args )

	def doDrop( self, dieEntity, killer, args ):
		"""
		执行掉落功能
		"""
		self._dropValuesDatas.clear()
		self._dropItemDatas.clear()
		self._allocationItemDatas.clear()
		self._allocationDatas.clear()
		
		#防沉迷，计算收益
		#gameYield = killer.wallow_getLucreRate()
		gameYield = 1
		info = {"player": killer, "dieEntity": dieEntity}
		
		#获取基准倍率数据，计算数值型奖励
		valueDatas = self.getBasicRewardValue( dieEntity, killer )
		if valueDatas:
			for key, value in valueDatas.items():
				self._dropValuesDatas[ key ] = int(value * gameYield)
		
		#取任务奖励
		questDatas = {}
		if self._dropDatas["questdrops"] == "1":
			questDatas = self.getQuestReward( dieEntity )
		for dbid, datas in questDatas.items():
			self.onQuestDataProcessed( dbid, datas, info )

		#幻兽掉落
		
		self.dropPet(dieEntity, killer, args)
		
		#获取掉落
		self.getDropReward( dieEntity, killer, args )	
		
		self.onDrop( dieEntity, killer, args )


	def dropPet(self, dieEntity, killer, args):
		"""
		掉幻兽
		"""
		#"petDrops":"scriptID;0.1;120"  脚本ID;掉落倍率;持有时间（第一次归属玩家持有时间，过了这个时间后所有玩家可拾取）
		if not  "petDrops" in self._dropDatas:
			return

		if not self._dropDatas["petDrops"]:
			return
		scriptID, rate,  keepTime =  self._dropDatas["petDrops"].split(";")
		if getRewardForRate(float(rate)):
			params = {}
			params["keepTime"] = float(keepTime)
			params["keeperDBID"] = killer.playerDBID
			dieEntity.createEntityByScriptID(scriptID, tuple(Math.Vector3(dieEntity.position)), tuple(Math.Vector3(dieEntity.direction), ), params)

	def getDropReward( self, dieEntity, killer, args ):
		"""
		获取掉落奖励
		"""
		if not self._dropDatas["drops"]:
			return
			
		try:
			#like : 1:100001:1:0.1;2:100002:1:0.1
			#奖励所有权:奖励编号:奖励编号执行次数:单次执行概率;···
			drops = self._dropDatas["drops"].split(";")
			self.getDropRewardForRate( drops, dieEntity, killer )
		except:
			KBEDebug.ERROR_MSG("Drop:getDropReward error, (%s)" %(self._dropDatas["drops"]))
		
	def getDropRewardForRate( self, drops, dieEntity, killer ):
		"""
		获取掉落随机奖励
		"""
		owners = dieEntity.calculateBootyOwner()
		ownerList = list(owners.values())
		
		#防沉迷，计算收益
		#gameYield = killer.wallow_getLucreRate()
		gameYield = 1
		#没收益、没人，后面就不要继续了吧
		if gameYield <= 0 or len(ownerList) <= 0:
			return
			
		for drop in drops:
			#like 1:510001:2:0.1
			if not drop:	
				continue
			
			try:
				drop = drop.split(":")
				dropType = int( drop[0] )
				rewardID = drop[1]
				number = int( drop[2] )
				rate = float( drop[3] ) * gameYield
			except:
				KBEDebug.ERROR_MSG("Drop:getDropRewardForRate error, dieEntity scriptID(%s), drops(%s)" %(dieEntity.getScriptID(), drops))
				return
			
			#奖励所有权为0，奖励总体执行一轮
			if dropType == 0:
				#奖励执行几次
				for i in range( number ):
					if not getRewardForRate( rate ):
						continue
			
					rewardData = RewardMgr.g_rewardMgr.getReward( rewardID, {"player": killer, "dieEntity": dieEntity} )	
					self.onDropDataProcessedForAllOwner(ownerList, rewardData, {"player": killer, "dieEntity": dieEntity})
					
			#否则，每个拥有奖励所有权的玩家执行一轮
			else:
				for owner in ownerList:
					#奖励执行几次
					for i in range( number ):
						if not getRewardForRate( rate ):
							continue
			
						rewardData = RewardMgr.g_rewardMgr.getReward( rewardID, {"player": killer, "dieEntity": dieEntity} )	
						self.onDropDataProcessedForSingle(owner, rewardData, {"player": killer, "dieEntity": dieEntity})
				
	def onDropDataProcessedForAllOwner( self, ownerList, datas, args ):
		"""
		根据drops生成的奖励分类: value, item
		"""
		if not datas:
			return
			
		for data in datas:
			type = data["type"]
			amount = data["amount"]
			goodsid = data["goodsid"]
			
			# 物品奖励
			if type == csdefine.REWARD_TYPE_ITEM:
				#怪物所有权是第一种，则拥有奖励所有权的队员按照队伍设定的分配规则，分配奖品，同原规则
				if self.ownership == Define.MONSTER_OWNER_FIRST_DAMAGE:
					self._dropItemDatas.append( data )
				#怪物所有权是第二种，则在所有拥有奖励所有权的玩家中，随机分配每个奖品的拾取权
				else:
					dbid = random.choice(ownerList)
					if dbid not in self._allocationItemDatas:
						self._allocationItemDatas[ dbid ] = []
					self._allocationItemDatas[ dbid ].append( data )
			# 子奖励表
			elif type == csdefine.REWARD_TYPE_CREWARD:
				dropDatas = RewardMgr.g_rewardMgr.getReward( goodsid, args )
				self.onDropDataProcessedForAllOwner( ownerList, dropDatas, args )
			#空奖励
			elif type == csdefine.REWARD_TYPE_NOTHING:
				continue
			#其他奖励应该是数值奖励？？
			else:
				if type not in self._dropValuesDatas:
					self._dropValuesDatas[ type ] = 0
					
				self._dropValuesDatas[type] += amount
				
	def onDropDataProcessedForSingle( self, ownerDBID, datas, args ):
		"""
		根据drops生成的奖励分类: value, item
		"""
		if not datas:
			return
			
		for data in datas:
			type = data["type"]
			amount = data["amount"]
			goodsid = data["goodsid"]
			
			# 物品奖励
			if type == csdefine.REWARD_TYPE_ITEM:
				if ownerDBID not in self._allocationItemDatas:
					self._allocationItemDatas[ ownerDBID ] = []
				self._allocationItemDatas[ ownerDBID ].append( data )
			# 子奖励表
			elif type == csdefine.REWARD_TYPE_CREWARD:
				dropDatas = RewardMgr.g_rewardMgr.getReward( goodsid, args )
				self.onDropDataProcessedForSingle( ownerDBID, dropDatas, args )
			#空奖励
			elif type == csdefine.REWARD_TYPE_NOTHING:
				continue
			#其他奖励应该是数值奖励？？
			else:
				if ownerDBID not in self._allocationDatas:
					self._allocationDatas[ ownerDBID ] = {}
					
				if type not in self._allocationDatas[ ownerDBID ]:
					self._allocationDatas[ ownerDBID ][ type ] = 0
					
				self._allocationDatas[ ownerDBID ][type] += amount
					
	def onQuestDataProcessed( self, dbid, datas, args ):
		"""
		根据questID和MonsterID生成的奖励分类: value, item
		"""
		if not datas:
			return
			
		for data in datas:
			type = data["type"]
			amount = data["amount"]
			goodsid = data["goodsid"]
			
			# 物品奖励
			if type == csdefine.REWARD_TYPE_ITEM:
				if dbid not in self._allocationItemDatas:
					self._allocationItemDatas[ dbid ] = []
				self._allocationItemDatas[ dbid ].append( data )
			# 子奖励表
			elif type == csdefine.REWARD_TYPE_CREWARD:
				dropDatas = RewardMgr.g_rewardMgr.getReward( goodsid, args )
				self.onQuestDataProcessed(dbid, dropDatas, args)			
			#空奖励
			elif type == csdefine.REWARD_TYPE_NOTHING:
				continue
			#其他奖励应该是数值奖励？？
			else:
				if dbid not in self._allocationDatas:
					self._allocationDatas[ dbid ] = {}
					
				if type not in self._allocationDatas[ dbid ]:
					self._allocationDatas[ dbid ][ type ] = 0
					
				self._allocationDatas[ dbid ][type] += amount
	
	def getBasicRewardValue( self, dieEntity, killer ):
		"""
		获取基准倍率数据
		"""
		obj = RewardMgr.g_rewardMgr.getRewardScript( "RewardForLevelToBasicValue" )
		data = {"param1": "", "param2": ""}
		if obj:
			info = {"dieEntity": dieEntity, "player" : killer}
			dropData = copy.deepcopy( self._dropDatas )
			dropData["xiuweiRate"] *= killer.kmg_xiuweiRate				# CST-13701
			valueData = obj( dropData, data ).fetch( info )
			return valueData
		return None
		
	def getQuestReward( self, dieEntity ):
		"""
		获取掉落任务随机奖励
		"""
		owners = dieEntity.calculateBootyOwner()
		info = {"ownerList": list(owners.keys()), "dieEntity": dieEntity}
		obj = RewardMgr.g_rewardMgr.getRewardScript( "RewardForQuestIDAndMonsterIDToRate" )
		data = {"param1": "", "param2": ""}
		rewardData = obj( {}, data ).fetch( info )
		return rewardData
		
	
