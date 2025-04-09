# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
from ConfigObject.SpaceCopyLLBZRewardsLoader import g_SpaceCopyLLBZRewards
from ConfigObject.Reward.RewardBase import RewardMgr


class SEAction337( SEActionBase ):
	"""
	玲珑宝珠 结算
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]	# 阶段目标ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityList = spaceEntity.getEntityMailBoxRecord(self._scriptID)
		if not len(entityList):
			return
		entity = entityList[0]
		HPRate = int(entity.HP * 100 / entity.HP_Max)
		rate = HPRate - (HPRate % 10)
		for player in spaceEntity._spaceRoles:
			exp = g_SpaceCopyLLBZRewards.getLLBZExpRewards(player.level)
			money = g_SpaceCopyLLBZRewards.getLLBZMoneyRewards(player.level)
			potential = g_SpaceCopyLLBZRewards.getLLBZPotentialRewards(player.level)
			player.addExp(rate * exp, csdefine.EXP_ADD_REASON_SPACE_SENTLEMENT)
			if "exp" not in spaceEntity.spaceRewards:
				spaceEntity.spaceRewards["exp"] = 0
			spaceEntity.spaceRewards["exp"] += rate * exp
			player.addMoney(rate * money, csdefine.EXP_ADD_REASON_SPACE_SENTLEMENT)
			if "money" not in spaceEntity.spaceRewards:
				spaceEntity.spaceRewards["money"] = 0
			spaceEntity.spaceRewards["money"] += rate * money
			player.addPotential( rate * potential, csdefine.POTENTIAL_ADD_REASON_SPACE_SENTLEMENT )
			if "potential" not in spaceEntity.spaceRewards:
				spaceEntity.spaceRewards["potential"] = 0
			spaceEntity.spaceRewards["potential"] += rate * potential

		#界面结算
		rewardStr = ""
		for key, value in spaceEntity.spaceRewards.items():
			rewardStr += str(key)+":"+str(value)+"|"
		for e in spaceEntity._spaceRoles:
			if e.getClient():
				e.client.CLIENT_ShowLLBZRewards(rewardStr, HPRate)

class SEAction338( SEActionBase ):
	"""
	玲珑宝珠 给副本内所有玩家发送奖励 (参与副本结算)
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rewardID = section["param1"]

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			rewardDatas = RewardMgr.g_rewardMgr.getReward( self.rewardID, {"player":player} )
			for rewardData in rewardDatas:
				RewardMgr.g_rewardMgr.doReward( rewardData, player.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_SPACE_EVENT )
				if rewardData["type"] == "item":
					if rewardData["goodsid"] not in spaceEntity.spaceRewards:
						spaceEntity.spaceRewards[rewardData["goodsid"]] = 0
					spaceEntity.spaceRewards[rewardData["goodsid"]] += rewardData["amount"]
				elif rewardData["type"] == "money":
					if "money" not in spaceEntity.spaceRewards:
						spaceEntity.spaceRewards["money"] = 0
					spaceEntity.spaceRewards["money"] += rewardData["amount"]
				elif rewardData["type"] == "exp":
					if "exp" not in spaceEntity.spaceRewards:
						spaceEntity.spaceRewards["exp"] = 0
					spaceEntity.spaceRewards["exp"] += rewardData["amount"]
				elif rewardData["type"] == "potential":
					if "potential" not in spaceEntity.spaceRewards:
						spaceEntity.spaceRewards["potential"] = 0
					spaceEntity.spaceRewards["potential"] += rewardData["amount"]


SEActionBase.setActionClass("SEAction337", SEAction337)
SEActionBase.setActionClass("SEAction338", SEAction338)