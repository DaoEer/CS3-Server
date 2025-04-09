# -*- coding: utf-8 -*-
import Math
import random
import KBEngine
import CoreInterface.NPCAmbulantInterface as NPCAmbulantInterface
import NPC
import csdefine
import ItemFactory
import KBEDebug
from ConfigObject.Reward.RewardBase import RewardMgr
from ConfigObject.SpaceCopyNPCFuDaiDataLoader import g_SpaceCopyNPCFuDaiData

ROLE_HAS_BUFF = 0
HAS_BUFF_DISTANCE = 4
MAX_LIFE_TIME = 10
MONSTER_DROP = ["10000976", "10000977", "10000978", "10000979", "10000980", "10000981", "10000982", "10000983"]
MONSTER_DROP_INTEGRAL = "10000977"
MONSTER_DROP_POTENTIAL = "10000976"
MONSTER_DROP_EQUIP = "10000979"
MONSTER_DROP_MATERIAL = "10000978"
MONSTER_SCRIPTID = "20010169"

COPY_REWARD_TYPE_INTEGRAl = "0"  # 金精
COPY_REWARD_TYPE_POTENTIAL = "1"  # 潜能
collideWithPlayerNum = 0


class NPCDropFuDai(NPC.NPC, NPCAmbulantInterface.NPCAmbulantInterface):
	"""
	福袋 金枝玉庭玩法 ： CST-5774
	"""

	def __init__(self):
		NPC.NPC.__init__(self)
		NPCAmbulantInterface.NPCAmbulantInterface.__init__(self)
		self._verify = False
		self._isOneEffect = g_SpaceCopyNPCFuDaiData.isOneEffect(self.scriptID)
		self._isOneSound = g_SpaceCopyNPCFuDaiData.isOneDropSound(self.scriptID)
		self._floorTimer = 0
		self._createTimer = 0
		self._rate = 1.0
		self.monster = None

	def CELL_onClientReady(self, srcEntityID):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		self.allClients.CLIENT_OnPlay3DSound(g_SpaceCopyNPCFuDaiData.getDropSound(self.scriptID, 0))
		if self._isOneEffect:
			self.allClients.CLIENT_OnPlayFloorEffect(g_SpaceCopyNPCFuDaiData.getEffect(self.scriptID, 0))
		spaceEntity = self.getCurrentSpace()
		if self.scriptID == MONSTER_DROP_INTEGRAL:
			self.allClients.NotifyIntegralAmount(self.integralAmount)

	# if spaceEntity:
	# 	spaceEntity.allFuDaiScriptIDList.append(self.scriptID)

	def delayStartMove(self, drag):
		randomDropFuDaiInervalTime = random.randint(0, 9)
		self._lifeTimer = self.addTimerCallBack(MAX_LIFE_TIME + randomDropFuDaiInervalTime + g_SpaceCopyNPCFuDaiData.getDestroyTime(self.scriptID), "fuDaiStandFloor", ())
		self.addTimerCallBack(randomDropFuDaiInervalTime, "startMove", (drag,))

	def startMove(self, drag):
		"""
		开始移动
		"""

		if not self._isOneSound:
			self.allClients.CLIENT_OnStop3DSound()
			self.allClients.CLIENT_OnPlay3DSound(g_SpaceCopyNPCFuDaiData.getDropSound(self.scriptID, 1))
		self.allClients.CLIENT_OnPlayParticles(self.id, g_SpaceCopyNPCFuDaiData.getEffect(self.scriptID, 0), "", 1.0, Math.Vector3(0, 0, 0))
		resistance = g_SpaceCopyNPCFuDaiData.getResistance(self.scriptID)
		rewardEffect = g_SpaceCopyNPCFuDaiData.getrewardEffect(self.scriptID)
		self.allClients.CLIENT_fuDaiStartMove(resistance, rewardEffect)

	def onFuDaiCollisionBegin(self, exposedID, playerID):
		"""
		碰撞开始
		"""
		if self.verifyDistance():
			self._verify = True
		if not self._isOneSound:
			self.allClients.CLIENT_OnStop3DSound()
		if not self._isOneEffect:
			self.allClients.CLIENT_OnStopParticles()
		if playerID:
			if self._floorTimer:
				self.popTimer(self._floorTimer)
				self._floorTimer = 0
			self.addFlag(csdefine.FLAG_UNVISIBLE)
		else:
			self.onFuDaiCollisionFloor()

	def onFuDaiCollisionFloor(self):
		"""
		福袋碰到地板
		"""
		if not self._isOneSound:
			self.allClients.CLIENT_OnPlay3DSound(g_SpaceCopyNPCFuDaiData.getDropSound(self.scriptID, 2))
		if not self._isOneEffect:
			self.allClients.CLIENT_OnPlayParticles(self.id, g_SpaceCopyNPCFuDaiData.getEffect(self.scriptID, 1), "",1.0, Math.Vector3(0, 0, 0))
		self._floorTimer = self.addTimerCallBack(g_SpaceCopyNPCFuDaiData.getDestroyTime(self.scriptID),"fuDaiStandFloor", ())

		MonsterInfo = g_SpaceCopyNPCFuDaiData.getMonster(self.scriptID)
		if MonsterInfo:
			self._createTimer = self.addTimerCallBack(MonsterInfo[1], "createMonster", (MonsterInfo,))

	def createMonster(self, MonsterInfo):
		"""
		创建盗宝小贼
		"""
		pos = self.position
		dir = (0.0, 0.0, 0.0)
		self.monster = self.createEntityByScriptID(MonsterInfo[0], pos, dir, {"spawnPos": pos, "spawnDir": dir})

	def fuDaiStandFloor(self):
		"""
		福袋停留在地板
		"""
		try:
			if not self._isOneSound:
				self.allClients.CLIENT_OnStop3DSound()
				self.allClients.CLIENT_OnPlay3DSound(g_SpaceCopyNPCFuDaiData.getDropSound(self.scriptID, 3))
			if not self._isOneEffect:
				self.allClients.CLIENT_OnStopParticles()
				self.allClients.CLIENT_OnPlayParticles(self.id, g_SpaceCopyNPCFuDaiData.getEffect(self.scriptID, 2), "",1.0, Math.Vector3(0, 0, 0))
		except:
			pass
		self.destroySelf()

	def playerGetReward(self, player, rewardID):
		"""
		福袋碰撞到玩家获得奖励
		"""
		spaceEntity = self.getCurrentSpace()
		giftData = RewardMgr.g_rewardMgr.getReward(str(rewardID), {"player": player})
		if giftData:
			for data in giftData:
				if data["type"] == csdefine.REWARD_TYPE_CREWARD:
					self.playerGetReward(player, data["goodsid"])
					continue
				if data["type"] == csdefine.REWARD_TYPE_ITEM:
					self.spaceEntityAddReward(player, data["goodsid"], data["amount"])
				elif data["type"] == csdefine.REWARD_TYPE_INTEGRAL:
					# self.spaceEntityAddReward(player, COPY_REWARD_TYPE_INTEGRAl, data["amount"])
					self.spaceEntityAddReward(player, COPY_REWARD_TYPE_INTEGRAl, data["amount"])
					continue
				elif data["type"] == csdefine.REWARD_TYPE_POTENTIAL:
					self.spaceEntityAddReward(player, COPY_REWARD_TYPE_POTENTIAL, data["amount"])
				RewardMgr.g_rewardMgr.doReward(data, player.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_JZYT)

	def onFuDaiCollisionPlayer(self, exposedID, playerID):
		"""
		exposed method
		福袋碰撞到玩家
		"""
		if self.monster:
			self.monster.monsterAISendCommand(self.monster.id, g_SpaceCopyNPCFuDaiData.getMonster(self.scriptID)[3])
		player = KBEngine.entities.get(playerID)
		if not player:
			return
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and self.scriptID in spaceEntity.allFuDaiScriptIDList:
			spaceEntity.allFuDaiScriptIDList.remove(self.scriptID)

		# 怪物掉落的金币奖励
		if self.scriptID == MONSTER_DROP_INTEGRAL:
			self.spaceEntityAddReward(player, COPY_REWARD_TYPE_INTEGRAl, self.integralAmount)
			# player.addSparHunTingIntegral(self.integralAmount)
			self.integralAmount = 0
		# 怪物掉落的潜能奖励
		elif self.scriptID == MONSTER_DROP_POTENTIAL:
			self.spaceEntityAddReward(player, COPY_REWARD_TYPE_POTENTIAL, self.potentialAmount)
			player.addPotential(self.potentialAmount)
			self.potentialAmount = 0
		# 怪物掉落的材料奖励
		elif self.scriptID == MONSTER_DROP_MATERIAL:
			self.spaceEntityAddReward(player, str(self.materialItem), 1)
			player.addItemByID(self.materialItem, 1, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT)
			self.materialItem = 0
		# 怪物掉落的装备奖励
		elif self.scriptID == MONSTER_DROP_EQUIP:
			self.spaceEntityAddReward(player, str(self.equipItem), 1)
			player.addItemByID(self.equipItem, 1, csdefine.ITEM_ADD_BY_SPACE_SENTLEMENT)
			self.equipItem = 0
		else:
			rewardID = g_SpaceCopyNPCFuDaiData.getAllRewardsList(self.scriptID)
			self.playerGetReward(player, rewardID)

		self.addTimerCallBack(2.0, "destroySelf", ())

	def monsterCollectFuDai(self, selfEntity, player, rewardID):
		"""
		怪物收取场景中所有的宝物
		"""
		spaceEntity = player.getCurrentSpace()
		key = -1
		value = -1

		giftData = RewardMgr.g_rewardMgr.getReward(str(rewardID), {"player": player})
		if giftData:
			for data in giftData:
				if data["type"] == csdefine.REWARD_TYPE_CREWARD:
					self.monsterCollectFuDai(selfEntity, player, data["goodsid"])
					continue
				elif data["type"] == csdefine.REWARD_TYPE_ITEM:
					itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(data["goodsid"])
					if itemInst.isEquip():
						if data["goodsid"] not in spaceEntity.equipRewards:
							spaceEntity.equipRewards[data["goodsid"]] = data["amount"]
						else:
							spaceEntity.equipRewards[data["goodsid"]] += data["amount"]
						key = data["goodsid"]
						value = spaceEntity.equipRewards[data["goodsid"]]
					else:
						if data["goodsid"] not in spaceEntity.materialRewards:
							spaceEntity.materialRewards[data["goodsid"]] = data["amount"]
						else:
							spaceEntity.materialRewards[data["goodsid"]] += data["amount"]
						key = data["goodsid"]
						value = spaceEntity.materialRewards[data["goodsid"]]
				elif data["type"] == csdefine.REWARD_TYPE_INTEGRAL:
					spaceEntity.integralAmount += 1
					key = 0
					value = spaceEntity.integralAmount
				elif data["type"] == csdefine.REWARD_TYPE_POTENTIAL:
					spaceEntity.potentialAmount += data["amount"]
					key = 1
					value = spaceEntity.potentialAmount
				elif data["type"] == csdefine.REWARD_TYPE_NOTHING:
					continue
				else:
					KBEDebug.ERROR_MSG("monsterCollectFuDai reward error: rewardID(%s), rewardType(%s)" % (rewardID, data["type"]))
					continue

				for e in spaceEntity._spaceRoles:
					if e.getClient():
						e.client.CLIENT_NotifyDisplayItemIcon(int(key), int(value))

	def onFuDaiCollisionMonster(self, selfEntity, player):
		"""
		怪物收取场景中所有的宝物
		"""
		if not player:
			return

		if self.scriptID in MONSTER_DROP:
			return
		spaceEntity = player.getCurrentSpace()
		entityList = spaceEntity.getEntityMailBoxRecord(MONSTER_SCRIPTID)
		if len(entityList) != 1:
			return
		spaceEntity.tempMonsterID = entityList[0].id
		selfEntity.allClients.CLIENT_OnPlayParticles(entityList[0].id,g_SpaceCopyNPCFuDaiData.getmonsterEffect(selfEntity.scriptID), "",1.0, Math.Vector3(0, 0, 0))

		rewardID = g_SpaceCopyNPCFuDaiData.getAllRewardsList(selfEntity.scriptID)
		self.monsterCollectFuDai(selfEntity, player, rewardID)

		selfEntity.destroySelf()

	def beforeDestroy(self):
		"""
		virtual method
		销毁前做一些事
		"""
		# 清理定时器
		if self._lifeTimer:
			self.popTimer(self._lifeTimer)
			self._lifeTimer = 0
		if self._floorTimer:
			self.popTimer(self._floorTimer)
			self._floorTimer = 0

		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange(spaceEntity, "", "", "FUDAI",{"spawnPos": self.spawnPos, "spawnDir": self.spawnDir})
			if self.scriptID in spaceEntity.allFuDaiScriptIDList:
				spaceEntity.allFuDaiScriptIDList.remove(self.scriptID)

		NPC.NPC.beforeDestroy(self)
		NPCAmbulantInterface.NPCAmbulantInterface.beforeDestroy(self)

	def onMoveOver(self, controllerID, userData):
		"""
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.NPCAmbulantInterface.doMoveOver(self, controllerID, userData)

	def spaceEntityAddReward(self, player, key, value):
		"""
		统计奖励
		"""
		soundID = g_SpaceCopyNPCFuDaiData.getRewardSound(self.scriptID, key)
		player.showMessagePlaySound(soundID)
		player.client.CLIENT_ShowFuDaiReward(key, value)
		spaceEntity = self.getCurrentSpace()
		spaceEntity.spaceRewardAmount += 1
		if key not in spaceEntity.spaceRewards:
			spaceEntity.spaceRewards[key] = 0
		spaceEntity.spaceRewards[key] += value

		if key == COPY_REWARD_TYPE_INTEGRAl:
			spaceEntity.integralToolAmount += value
			player.client.CLIENT_ShowCurrGotGoldAmount(value)
			if spaceEntity.playPriGradeSoundFlg and spaceEntity.integralToolAmount >= spaceEntity.getScript().goldNumAboutGrade[1]:
				player.showMessagePlaySound(spaceEntity.getScript().soundsAboutEachGrade[1])
				spaceEntity.playPriGradeSoundFlg = 0

			elif spaceEntity.playHighGradeSoundFlg and spaceEntity.integralToolAmount >= spaceEntity.getScript().goldNumAboutGrade[0]:
				player.showMessagePlaySound(spaceEntity.getScript().soundsAboutEachGrade[0])
				spaceEntity.playHighGradeSoundFlg = 0

	def verifyDistance(self):
		"""
		验证碰撞的时机是否合法
		"""
		return True

	def timeDestroy(self):
		"""
		时间到达销毁自己
		"""
		if self._lifeTimer:
			self.popTimer(self._lifeTimer)
			self._lifeTimer = 0
		self.destroySelf()

	def getRate(self, player):
		"""
		获得奖励倍率
		"""
		spaceEntity = self.getCurrentSpace()
		rate = g_SpaceCopyNPCFuDaiData.getRewardRate(self.scriptID, spaceEntity.spaceJZYTStage)
		soundID = g_SpaceCopyNPCFuDaiData.getRewardRateSoundID(self.scriptID, rate)
		player.showMessagePlaySound(soundID)
		return rate

	# def getGoldNumAboutWhichGrade(self):
	# 	"""
	# 	获取达到哪一档所需要获得金币数量
	# 	"""
	# 	spaceEntity = self.getCurrentSpace()
	# 	amountList = list(spaceEntity.getScript().rewards.keys())
	# 	amountList.sort(reverse=True)
