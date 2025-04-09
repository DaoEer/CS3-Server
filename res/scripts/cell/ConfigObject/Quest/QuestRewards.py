# -*- coding: utf-8 -*-
#
import csdefine
import KBEDebug
import ItemFactory
import Functions
import csstatus
from ConfigObject.Quest.QuestBase.QuestReward import QuestRewardBase
from Reward import RewardBasicValueData
from ConfigObject.Reward.RewardBase import RewardMgr


# ----------------------------------------------------------
# 任务奖励类型扩展 继承父类QuestRewardBase
# ----------------------------------------------------------
class QuestRewardMoney( QuestRewardBase ):
	"""金币奖励"""
	def __init__(self):
		self._value = 0

	def init(self, data):
		self._value = 0
		self._extraValue = 0
		if data["param1"].strip():
			self._value = data["param1"]
		if data["param2"].strip():
			self._extraValue = float(data["param2"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		basicValue = RewardBasicValueData.datas.get(player.getLevel(), {}).get("money", 0)
		money = int( self._value ) + round(basicValue * self._extraValue)
		if money:
			player.addBindMoney(money, csdefine.MONEY_ADD_REASON_QUEST_REWARD )

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_MONEY

	def sendClientData( self, player ):
		basicValue = RewardBasicValueData.datas.get(player.getLevel(), {}).get("money", 0)
		money = int( self._value ) + round(basicValue * self._extraValue)
		return { str( csdefine.QUEST_REWARD_TYPE_MONEY): str( money ) }

class QuestRewardExp( QuestRewardBase ):
	"""经验奖励"""
	def __init__(self):
		self._value = 0

	def init(self, data):
		self._value = 0
		self._extraValue = 0
		if data["param1"].strip():
			self._value = data["param1"]
		if data["param2"].strip():
			self._extraValue = float(data["param2"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		basicValue = RewardBasicValueData.datas.get(player.getLevel(), {}).get("exp", 0)
		exp = int(self._value) + round(basicValue * self._extraValue)
		if exp:
			player.addExp(exp, csdefine.EXP_ADD_REASON_QUEST_REWARD)

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_EXP
		
	def sendClientData( self, player ):
		basicValue = RewardBasicValueData.datas.get(player.getLevel(), {}).get("exp", 0)
		exp = int(self._value) + round(basicValue * self._extraValue)
		return { str( csdefine.QUEST_REWARD_TYPE_EXP): str( exp ) }

class QuestRewardItem( QuestRewardBase ):

	"""物品奖励"""

	def __init__(self):
		self._itemID = 0
		self._amount = 0

	def init(self, data):
		self._itemID = 0 if not data["param1"] else int(data["param1"])
		self._amount = 0 if not data["param2"] else int(data["param2"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		# 根据物品ID获得物品实例
		if self._itemID and self._amount:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(self._itemID, self._amount)
			if itemInst:
				itemInst.setBindType(None)
				player.addItem(itemInst, csdefine.ITEM_ADD_BY_QUEST)

	def getItemIdAndAmount(self, player):
		return self._itemID, self._amount

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_ITEM

	def sendClientData(self, player):
		if self._itemID and self._amount:
			dynamicDatas = {}
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(self._itemID, self._amount)
			if itemInst.isEquip():
				dynamicDatas = {
					"amount": str(itemInst.amount),
					"bindType": str(itemInst.bindType),
					"hardiness": str(itemInst.dynamicData["hardiness"]),
					"combatPower": str(itemInst.dynamicData["combatPower"]),
					"attackProperties": itemInst.dynamicData["attackPropertiesStr"],
					"attachProperties": itemInst.dynamicData["attachPropertiesStr"]
				}
			else:
				dynamicDatas = {
					"amount": str(itemInst.amount),
					"bindType": str(itemInst.bindType)
				}
			datas = str(self._itemID) + "|" + Functions.toJsonString(dynamicDatas).replace("|", "/")
			return {str(csdefine.QUEST_REWARD_TYPE_ITEM): datas}
		else:
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardItem config error, as itemstr(%s)" % self._itemID)
			return {}

class QuestRewardSkill( QuestRewardBase ):
	"""技能奖励"""
	def __init__(self):
		self._allSkillsID = []

	def init(self, data):
		params = data["param1"].split("|")
		for i in params:
			if i != "":
				self._allSkillsID.append(int(i))

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		for rewardSkillID in self._allSkillsID:
			# 玩家直接学习技能
			player.presentedSkill( rewardSkillID )

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_SKILL

	def sendClientData( self, player ):
		datas = ""
		for skillID in self._allSkillsID:
			datas = str( skillID ) + "|"
		return { str( csdefine.QUEST_REWARD_TYPE_SKILL): datas }
		
class QuestRewardSkillByProfession( QuestRewardBase ):
	"""根据职业奖励技能"""
	def __init__(self):
		self._allSkillsID = []

	def init(self, data):
		params = data["param1"].split("|")
		for i in params:
			if i != "":
				self._allSkillsID.append(int(i))

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		profession = player.getProfession()
		lenSkillList = len( self._allSkillsID )
		if profession == csdefine.CLASS_FIGHTER and  lenSkillList >= 1:
			rewardSkillID = self._allSkillsID[0]
		elif profession == csdefine.CLASS_SWORDMAN and  lenSkillList >= 2:
			rewardSkillID = self._allSkillsID[1]
		elif profession == csdefine.CLASS_ARCHER and  lenSkillList >= 3:
			rewardSkillID = self._allSkillsID[2]
		elif profession == csdefine.CLASS_MAGE and  lenSkillList >= 4:
			rewardSkillID = self._allSkillsID[3]
		else:
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardSkillByProfession player(profession:%i) can not learn skill, as skillIDList(%s)"%(profession, str( self._allSkillsID)) )
			return
			
		player.presentedSkill( int(rewardSkillID) )

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_SKILL
			
	def sendClientData( self, player ):
		profession = player.getProfession()
		lenSkillList = len( self._allSkillsID )
		if profession == csdefine.CLASS_FIGHTER and  lenSkillList >= 1:
			rewardSkillID = self._allSkillsID[0]
		elif profession == csdefine.CLASS_SWORDMAN and  lenSkillList >= 2:
			rewardSkillID = self._allSkillsID[1]
		elif profession == csdefine.CLASS_ARCHER and  lenSkillList >= 3:
			rewardSkillID = self._allSkillsID[2]
		elif profession == csdefine.CLASS_MAGE and  lenSkillList >= 4:
			rewardSkillID = self._allSkillsID[3]
		else:
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardSkillByProfession player(profession:%i) can not learn skill, as skillIDList(%s)"%(profession, str( self._allSkillsID)) )
			return {}
		return { str( csdefine.QUEST_REWARD_TYPE_SKILL): str( rewardSkillID ) + "|" }

class QuestRewardXiuwei( QuestRewardBase ):
	"""修为奖励"""
	def __init__(self):
		self._xiuwei = 0

	def init(self, data):
		self._xiuwei = 0 if not data["param1"] else int(data["param1"])
		self._extraValue = 0
		if data["param2"].strip():
			self._extraValue = float(data["param2"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		# 增加玩家修为
		basicValue = RewardBasicValueData.datas.get(player.getLevel(), {}).get("xiuwei", 0)
		xiuwei = self._xiuwei + round(basicValue * self._extraValue)
		player.addXiuwei( xiuwei, csdefine.XIUWEI_ADD_REASON_QUEST_REWARD )

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_XIUWEI

	def sendClientData( self, player ):
		basicValue = RewardBasicValueData.datas.get(player.getLevel(), {}).get("xiuwei", 0)
		xiuwei = self._xiuwei + round(basicValue * self._extraValue)
		return { str( csdefine.QUEST_REWARD_TYPE_XIUWEI): str( xiuwei ) }

class QuestRewardPotential( QuestRewardBase ):
	"""潜能奖励"""
	def __init__(self):
		self._potential = 0

	def init(self, data):
		self._potential = 0 if not data["param1"] else int(data["param1"])
		self._extraValue = 0
		if data["param2"].strip():
			self._extraValue = float(data["param2"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		# 增加玩家潜能
		basicValue = RewardBasicValueData.datas.get(player.getLevel(), {}).get("potential", 0)
		potential = self._potential + round(basicValue * self._extraValue)
		player.addPotential( potential, csdefine.POTENTIAL_ADD_REASON_QUEST_REWARD )

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_POTENTIAL

	def sendClientData( self, player ):
		basicValue = RewardBasicValueData.datas.get(player.getLevel(), {}).get("potential", 0)
		potential = self._potential + round(basicValue * self._extraValue)
		return { str( csdefine.QUEST_REWARD_TYPE_POTENTIAL): str( potential ) }
		
class QuestRewardItemByProfession( QuestRewardBase ):
	"""根据职业奖励物品"""
	def __init__(self):
		self._itemID = ""
		self._amount = 0

	def init(self, data):
		self._itemID = str(data["param1"])
		self._amount = str(data["param2"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		# 根据物品ID获得物品实例
		itemID, amount = self.getItemIdAndAmount(player)
		if itemID and amount:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem( itemID, amount )
			if itemInst:
				itemInst.setBindType(None)
				player.addItem(itemInst, csdefine.ITEM_ADD_BY_QUEST)
		else:
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardItemByProfession player(profession:%i) can not add item, as itemstr(%s)"%(player.getProfession(), self._itemID))

	def getItemIdAndAmount(self, player):
		if not self._itemID.strip():
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardItemByProfession player(profession:%i) item not config, as itemstr(%s)" % (player.getProfession(), self._itemID))
			return
		itemID = 0
		amount = 1
		itemIDList = self._itemID.split("|")
		itemAountList = []
		if self._amount.strip():
			itemAountList = self._amount.split("|")
		lenList = len(itemIDList)
		profession = player.getProfession()
		if profession == csdefine.CLASS_FIGHTER and lenList >= 1:
			itemID = itemIDList[0]
			if len(itemAountList) >= 1:
				amount = int(itemAountList[0])
		elif profession == csdefine.CLASS_SWORDMAN and lenList >= 2:
			itemID = itemIDList[1]
			if len(itemAountList) >= 2:
				amount = int(itemAountList[1])
		elif profession == csdefine.CLASS_ARCHER and lenList >= 3:
			itemID = itemIDList[2]
			if len(itemAountList) >= 3:
				amount = int(itemAountList[2])
		elif profession == csdefine.CLASS_MAGE and lenList >= 4:
			itemID = itemIDList[3]
			if len(itemAountList) >= 4:
				amount = int(itemAountList[3])
		else:
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardItemByProfession player(profession:%i) config error, as itemstr(%s)" % (profession, self._itemID))
			return
		return itemID, amount
	
	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_ITEM

	def sendClientData( self, player ):
		itemID, amount = self.getItemIdAndAmount(player)
		dynamicDatas = {}
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount)
		if itemInst.isEquip():
			dynamicDatas = {
				"amount": str(itemInst.amount),
				"bindType": str(itemInst.bindType),
				"hardiness": str(itemInst.dynamicData["hardiness"]),
				"combatPower": str(itemInst.dynamicData["combatPower"]),
				"attackProperties": itemInst.dynamicData["attackPropertiesStr"],
				"attachProperties": itemInst.dynamicData["attachPropertiesStr"]
			}
		else:
			dynamicDatas = {
				"amount": str(itemInst.amount),
				"bindType": str(itemInst.bindType)
			}
		datas = str(itemID) + "|" + Functions.toJsonString(dynamicDatas).replace("|", "/")
		return { str( csdefine.QUEST_REWARD_TYPE_ITEM): datas }

class QuestRewardChooseItem( QuestRewardBase ):
	"""奖励多种物品，由玩家自行多选一"""
	def __init__(self):
		self._itemID = ""
		self._amount = 0
		self._chooseItemID = 0
		self._chooseItemAmount = 0
		self._index = 0

	def init(self, data):
		self._itemID = str(data["param1"])
		self._amount = str(data["param2"])
		if data["param3"].strip():
			self.setIndex(int(data["param3"]))
	
	def setIndex( self, index ):
		self._index = index
	
	def getIndex( self ):
		return self._index

	def check(self, player, params = {}):
		if self._chooseItemID == 0 or self._chooseItemAmount == 0:
			return False
		return True
	
	def chooseItem( self, itemInfo ):
		itemID, amount = itemInfo.split("|")
		self._chooseItemID = itemID
		self._chooseItemAmount = amount
	
	def do(self, player, params = {}):
		# 根据物品ID获得物品实例
		if not self._chooseItemID or not self._chooseItemAmount:
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardChooseItem (chooseItemID:%s, chooseAmount:%s) item not choose, as itemstr(%s)"%(self._chooseItemID, self._chooseItemAmount, self._itemID + "|" + self._amount))
			return
			
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem( self._chooseItemID, int( self._chooseItemAmount ) )

		if itemInst:
			itemInst.setBindType(None)
			player.addItem(itemInst, csdefine.ITEM_ADD_BY_QUEST)
		else:
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardChooseItem (chooseItemID:%s, chooseAmount:%si) itemID is not exist, as itemstr(%s)"%(self._chooseItemID, self._chooseItemAmount, self._itemID + "|" + self._amount))

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE

	def sendClientData( self, player ):
		if not self._itemID.strip():
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardChooseItem item not config")
			return {}
		itemIDList = self._itemID.split("|")
		itemAountList = []
		if self._amount.strip():
			itemAountList = self._amount.split("|")
		datas = ""
		for i in range( len(itemIDList) ):
			itemID = itemIDList[ i ].strip()
			amount = 1
			if len( itemAountList ) >= i + 1:
				amount = int( itemAountList[i] )
			datas = datas + str( itemID ) + ":" + str( amount ) + "|"
		if datas:
			datas = datas[:len( datas ) - 1]
		else:
			KBEDebug.ERROR_MSG("QuestRwards::QuestRewardChooseItem config error, as itemstr(%s)"%(self._itemID+"|"+self._amount))
			return {}
		return { "datas": datas, "index": self.getIndex() }		


class QuestRewardTitle( QuestRewardBase ):
	"""称号奖励"""
	def __init__(self):
		self.titleID = 0

	def init(self, data):
		self.titleID = 0 if not data["param1"] else int(data["param1"])

	def check(self, player, params = {}):
		return True

	def do(self, player, params = {}):
		# 增加玩家称号
		player.addTitle(self.titleID)

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_TITLE

	def sendClientData( self, player ):
		return { str( csdefine.QUEST_REWARD_TYPE_TITLE): str( self.titleID ) }
		
class QuestRewardTongContribute( QuestRewardBase ):
	"""帮贡奖励"""
	def __init__(self):
		self._value = 0

	def init(self, data):
		self._value = data["param1"]

	def check(self, player, params = {}):
		if player.tongDBID:
			return True
		return False

	def do(self, player, params = {}):
		contribute = int( self._value )
		if contribute and player.tongMB:
			player.tongMB.addContribution(player.playerDBID, contribute)

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_CONTRIBUTE
		
	def sendClientData( self, player ):
		return { str( csdefine.QUEST_REWARD_TYPE_CONTRIBUTE): str( self._value ) }
		
class QuestRewardTongMoney( QuestRewardBase ):
	"""帮会资金奖励"""
	def __init__(self):
		self._value = 0

	def init(self, data):
		self._value = data["param1"]

	def check(self, player, params = {}):
		if player.tongDBID:
			return True
		return False

	def do(self, player, params = {}):
		tongMoney = int( self._value )
		if tongMoney and player.tongMB:
			player.tongMB.addTongMoney(tongMoney, csdefine.TONG_MONEY_ADD_REASON_PERSON )
			player.statusMessage( csstatus.TONG_GET_MONEY_BY_SELF, Functions.moneyToStr( tongMoney ) )

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_TONG_MONEY

	def sendClientData( self, player ):
		return { str( csdefine.QUEST_REWARD_TYPE_TONG_MONEY): str( self._value ) }
				
class QuestRewardByRewardID( QuestRewardBase ):
	"""根据奖励ID奖励"""
	def __init__(self):
		self._rewardID = 0

	def init(self, data):
		self._rewardID = data["param1"]

	def check(self, player, params = {}):
		return True
	
	def doReward(self, rewardID, player, params = {}):
		datas = RewardMgr.g_rewardMgr.getReward(rewardID, {"player": player})
		RewardMgr.g_rewardMgr.doRewards(datas, player.id, csdefine.ADD_REWARD_REASON_COMMON_TYPE_QUEST)
	
	def do(self, player, params = {}):
		self.doReward(self._rewardID, player, params)
		
	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_REWARD_ID

	def sendClientData( self, player ):
		return { str(csdefine.QUEST_REWARD_TYPE_REWARD_ID): str( self._rewardID ) }
		
class QuestRewardBarracksExp( QuestRewardBase ):
	"""
	养兵经验奖励
	"""
	def __init__(self):
		self._value = 0
		
	def init(self, data):
		self._value = int(data["param1"])
		
	def check(self, player, params = {}):
		return True
		
	def do(self, player, params = {}):
		player.addBarracksExp(self._value)

	def getRewardType(self):
		return csdefine.QUEST_REWARD_TYPE_BARRACKS_EXP

	def sendClientData( self, player ):
		return { str( csdefine.QUEST_REWARD_TYPE_BARRACKS_EXP): str( self._value ) }