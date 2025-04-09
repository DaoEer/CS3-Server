# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# 日志管理器
#-----------------------------------------------------------------------------------

import time
import pickle
import KBEDebug
import LogDefine

class MsgLogger( object ):
	_instance = None
	def __init__( self ):
		pass
	
	@staticmethod
	def instance():
		if not MsgLogger._instance:
			MsgLogger._instance = MsgLogger()
		return MsgLogger._instance
		
	#---------------------------------------------------------------
	# 任务
	#---------------------------------------------------------------
	def questLog( self, action, roleDBID, roleName, questID, questName, roleLevel, roleGrade, useTime = "" ):
		"""
		添加任务日志
		action: 任务的接受、放弃或者完成
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_QUEST, action, roleDBID, roleName, questID, questName, roleLevel, roleGrade, useTime )
		
	def acceptQuestLog( self, roleDBID, roleName, questID, questName, roleLevel, roleGrade ):
		"""
		接受任务
		@param: 角色DBID，角色名，任务ID，角色等级，角色权限
		"""
		self.questLog( LogDefine.LT_QUEST_ACCEPT, roleDBID, roleName, questID, questName, roleLevel, roleGrade )
		
	def completeQuestLog( self, roleDBID, roleName, questID, questName, roleLevel, roleGrade ):
		"""
		完成任务
		@param: 角色DBID，角色名，任务ID，角色等级，角色权限
		"""
		self.questLog( LogDefine.LT_QUEST_COMPLETE, roleDBID, roleName, questID, questName, roleLevel, roleGrade )
		
	def abandonQuestLog( self, roleDBID, roleName, questID, questName, roleLevel, roleGrade ):
		"""
		放弃任务
		@param: 角色DBID，角色名，任务ID，角色等级，角色权限
		"""
		self.questLog( LogDefine.LT_QUEST_ABANDON, roleDBID, roleName, questID, questName, roleLevel, roleGrade )
		
	#---------------------------------------------------------------
	# 物品
	#---------------------------------------------------------------
	def itemLog( self, action, roleDBID, roleName, itemID, itemUID, itemName, itemNum, param1 = "", param2 = "", param3 = "", itemInst = None):
		"""
		物品日志
		action:物品的操作,获得,或者失去
		reason:原因
		"""
		itemData = self.getItemBlobData(itemInst)
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_ITEM, action, roleDBID, roleName, itemID, itemUID, itemName, itemNum, param1, param2, param3, pickle.dumps(itemData))

	def itemAddLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemNum, roleGrade, reason, itemInst):
		"""
		添加物品日志
		@param: 角色DBID，角色名，角色权限，物品ID，物品UID，物品名字，物品数量，获得物品原因（途径）
		"""
		self.itemLog( LogDefine.LT_ITEM_ADD, roleDBID, roleName, itemID, itemUID, itemName, itemNum, roleGrade, reason, "", itemInst )

	#order为每次操作的消耗（金钱、材料）识别字，因为消耗和实际操作的日志分开写，所以用order来识别每次的操作和消耗
	def itemDelLog(self, roleDBID, roleName, itemID, itemUID, itemName, itemNum, roleGrade, reason, order = "", itemInst = None):
		"""
		删除物品日志
		@param: 角色DBID，角色名，角色ID，物品ID，物品UID，物品名字，物品数量，角色权限，删除物品原因，order
		"""
		self.itemLog(LogDefine.LT_ITEM_DEL, roleDBID, roleName, itemID, itemUID, itemName, itemNum, roleGrade, reason, order, itemInst)
		
	def itemTranStoreLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemNum, itemInst):
		"""
		转入仓库
		@param: 角色DBID，角色名，任务ID，物品ID，物品UID，物品名字，物品数量
		"""
		self.itemLog(LogDefine.LT_ITEM_TRAN_STORE, roleDBID, roleName, itemID, itemUID, itemName, itemNum, "", "", "", itemInst)
		
	def itemTalkStoreLog(self, roleDBID, roleName, itemID, itemUID, itemName, itemNum, itemInst):
		"""
		取出仓库
		@param: 角色DBID，角色名，任务ID，物品ID，物品UID，物品名字，物品数量
		"""
		self.itemLog(LogDefine.LT_ITEM_TALK_STORE, roleDBID, roleName, itemID, itemUID, itemName, itemNum, "", "", "", itemInst)
		
	#---------------------------------------------------------------
	# 货币
	#---------------------------------------------------------------
	def coinLog( self, action, accountDBID, roleDBID, roleName, oldValue, newValue, reason, order = "" ):
		"""
		添加货币日志
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_COIN, action, accountDBID, roleDBID, roleName, oldValue, newValue, reason, order)
		
	#order为每次操作的消耗（金钱、材料）识别字，因为消耗和实际操作的日志分开写，所以用order来识别每次的操作和消耗
	def moneyChangeLog( self, accountDBID, roleDBID, roleName, oldMoney, newMoney, reason, order = "" ):
		"""
		玩家金钱改变
		@param: 账号dbid，角色DBID，角色名，原金币值，新金币值，改变原因, order
		"""
		self.coinLog( LogDefine.LT_MONEY_CHANGE, accountDBID, roleDBID, roleName, oldMoney, newMoney, reason, order )
	
	def xianshiChangeLog( self, accountDBID, roleDBID, roleName, oldXianshi, newXianshi, reason, order = "" ):
		"""
		玩家仙石改变
		"""
		self.coinLog( LogDefine.LT_XIANSHI_CHANGE, accountDBID, roleDBID, roleName, oldXianshi, newXianshi, reason, order )
		
	def lingshiChangeLog( self, accountDBID, roleDBID, roleName, oldLingshi, newLingshi, reason, order = ""):
		"""
		玩家灵石改变
		#order：1为消耗仙石的订单号，2为充值的兑换时游戏服务器生成的订单号，不是充值的订单号
		"""
		self.coinLog( LogDefine.LT_LINGSHI_CHANGE, accountDBID, roleDBID, roleName, oldLingshi, newLingshi, reason )
		
	def xuanshiChangeLog( self, accountDBID, roleDBID, roleName, oldXuanshi, newXuanshi, reason, order = "" ):
		"""
		玩家玄石改变
		#order为充值的兑换时游戏服务器生成的订单号，不是充值的订单号
		"""
		self.coinLog( LogDefine.LT_XUANSHI_CHANGE, accountDBID, roleDBID, roleName, oldXuanshi, newXuanshi, reason, order )
		
	def bindMoneyChangeLog( self, accountDBID, roleDBID, roleName, oldBindMoney, newBindMoney, reason, order = "" ):
		"""
		玩家金钱改变
		@param: 账号dbid，角色DBID，角色名，原值，新值，改变原因, order
		"""
		self.coinLog( LogDefine.LT_BINDMONEY_CHANGE, accountDBID, roleDBID, roleName, oldBindMoney, newBindMoney, reason, order )
		
		
	#---------------------------------------------------------------
	# 属性
	#---------------------------------------------------------------
	def proLog( self, type, roleDBID, roleName, param1 = "", param2 = "", param3 = "", param4 = "", param5 = "" ):
		"""
		添加角色属性改变日志
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_PRO, type, roleDBID, roleName, param1, param2 , param3, param4, param5 )

	def expChangeLog( self, roleDBID, roleName, oldExp, oldLevel, nowExp, nowLevel, reason ):
		"""
		角色经验改变
		@param: 角色DBID，角色名，原经验值，玩家原等级，新经验值，玩家新等级，经验改变原因
		"""
		self.proLog( LogDefine.LT_PRO_EXP_CHANGE, roleDBID, roleName, oldExp, oldLevel, nowExp, nowLevel, reason )
		
	#order为每次操作的消耗（金钱、材料）识别字，因为消耗和实际操作的日志分开写，所以用order来识别每次的操作和消耗
	def potentialChangeLog( self, roleDBID, roleName, oldPotential, nowPotential, reason, order = "" ):
		"""
		潜能改变
		@param: 角色DBID，角色名，原潜能值，新潜能值，潜能改变原因
		"""
		self.proLog( LogDefine.LT_PRO_POTENTIAL_CHANGE, roleDBID, roleName, oldPotential, nowPotential, reason, order )

	# 修为
	def xiuweiChangeLog( self, roleDBID, roleName, oldValue, newValue, reason = "" ):
		"""
		修为增长
		@param: 角色DBID，角色名，原修为值，新修为值，修为改变原因
		"""
		self.proLog( LogDefine.LT_PRO_XIUWEI_ADD, roleDBID, roleName, oldValue, newValue, reason )
	
	# 等级
	def roleUpgradeLog( self, roleDBID, roleName, oldLevel, newLevel, upTime ):
		"""
		玩家升级
		@param: 角色DBID，角色名，原等级，新等级，升级时间
		"""
		self.proLog( LogDefine.LT_PRO_LEVEL_UPGRADE, roleDBID, roleName, oldLevel, newLevel, upTime )
		
	def roleKillingChangeLog( self, roleDBID, roleName, oldKilling, newKilling):
		"""
		玩家杀气值改变
		@param: 角色DBID，角色名，原杀气值，新杀气值，升级时间
		"""
		self.proLog( LogDefine.LT_PRO_KILLING_CHANGE, roleDBID, roleName, oldKilling, newKilling)
		
	#order为每次操作的消耗（金钱、材料）识别字，因为消耗和实际操作的日志分开写，所以用order来识别每次的操作和消耗
	def roleCreditChangeLog( self, roleDBID, roleName, oldCredit, newCredit, reason, order = ""):
		"""
		玩家功勋值改变
		@param: 角色DBID，角色名，原功勋值，新功勋值，升级时间
		"""
		self.proLog( LogDefine.LT_PRO_CREDIT_CHANGE, roleDBID, roleName, oldCredit, newCredit, reason, order)
		
		
	#---------------------------------------------------------------
	# 装备
	#---------------------------------------------------------------
	def equipLog(self, action, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst = None , param1 = "", param2 = "", param3 = "", param4 = "", param5 = "", param6 = "", param7 = "", param8 = "", param9 = "", param10 = ""):
		"""
		添加装备日志
		"""
		equipData = self.getItemBlobData(itemInst)
		KBEDebug.DATABASE_LOG_MSG(LogDefine.LOG_TYPE_EQUIP, action, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, pickle.dumps(equipData))
	
	#order为每次操作的消耗（金钱、材料）识别字，因为消耗和实际操作的日志分开写，所以用order来识别每次的操作和消耗
	def equipIntensifyLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, intensifyLevel, newIntensifyLevel, oldIntensifyData, newIntensifyData, order = "", itemInst = None ):
		"""
		装备强化
		@param: 角色DBID，角色名，装备ID，装备原uid，装备名字，装备数量，装备原强化等级，装备新强化等级，增强前强化数据，增强后强化数据
		"""
		self.equipLog( LogDefine.LT_EQUIP_INTENSIFY, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst, order, intensifyLevel, newIntensifyLevel, "", "", "", "", "", pickle.dumps(oldIntensifyData), pickle.dumps(newIntensifyData))

	def equipComposeLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, order = "", itemInst = None ):
		"""
		装备打造
		@param: 角色DBID，角色名，装备id，装备新uid，装备名字，装备数量
		"""
		self.equipLog( LogDefine.LT_EQUIP_COMPOSE, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst, order)
		
	def equipRepairLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, oldHardinessMax, newHardinessMax, repairMoney, spaceClassName, shopID, itemInst ):
		"""
		装备修理
		@param: 角色DBID，角色名，装备id，装备uid，装备名字，装备数量，装备原耐久度，装备新耐久度，修理话费金钱，修理所在地图，商店ID
		"""
		self.equipLog(LogDefine.LT_EQUIP_REPAIR, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst, oldHardinessMax, newHardinessMax, repairMoney, spaceClassName, shopID)
		
	def equipBackFrieLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, intensifyLevel, newIntensifyLevel, oldIntensifyData, newIntensifyData, order = "", itemInst = None ):
		"""
		装备回火
		@param: 角色DBID，角色名，装备id，装备原uid，装备名字，装备数量，回火前强化等级，回火后强化等级，回火前强化数据，回火后强化数据
		"""
		self.equipLog(LogDefine.LT_EQUIP_BACKFIRE, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst, order, intensifyLevel, newIntensifyLevel, "", "", "", "", "", pickle.dumps(oldIntensifyData), pickle.dumps(newIntensifyData))
		
	def equipRestoreLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, intensifyLevel, oldIntensifyData, newIntensifyData, index, order = "", itemInst = None ):
		"""
		装备还原
		@param: 角色DBID，角色名，备新id，装备uid，装备名字，装备数量，装备强化等级，还原前强化数据，还原后强化数据，还原栏位
		"""
		self.equipLog(LogDefine.LT_EQUIP_RESTORE, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst, order, intensifyLevel, "", "", "", "", "", pickle.dumps(oldIntensifyData), pickle.dumps(newIntensifyData), index )
		
	def equipSaveLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, intensifyLevel, intensifyData, index, order = "", itemInst = None ):
		"""
		装备保存
		@param: 角色DBID，角色名，装备id，装备uid，装备名字，装备数量，装备强化等级，强化数据，保存栏位
		"""
		self.equipLog(LogDefine.LT_EQUIP_SAVE, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst, order, intensifyLevel, index, "", "", "", "", "", pickle.dumps(intensifyData) )

	def equipShuffleLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, oldIntensifyData, newIntensifyData, order = "", itemInst = None ):
		"""
		装备洗练
		@param: 角色DBID，角色名，装备id，装备uid，装备名字，装备数量，装备原加强属性，装备新加强属性
		"""
		self.equipLog(LogDefine.LT_EQUIP_SHUFFLE, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst, order, "", "", "", "", "", "", "", pickle.dumps(oldIntensifyData), pickle.dumps(newIntensifyData) )
		
	def equipShuffleReplaceLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, oldAttchPro, newAttchPro, itemInst ):
		"""
		装备洗练替换
		@param: 角色DBID，角色名，装备id，装备uid，装备名字，装备数量，替换前属性，替换后属性
		"""
		self.equipLog(LogDefine.LT_EQUIP_SHUFFLE_REPLACE, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst,  "", "", "", "", "", "", "", "", pickle.dumps(oldAttchPro), pickle.dumps(newAttchPro) )
		
	def equipRecastLog( self, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, changeAttrchPro, order = "", itemInst = None):
		"""
		装备重铸
		@param: 角色DBID，角色名，装备id，装备uid，装备名字，装备数量，消耗金钱，消耗重铸宝珠，消耗重铸保护符，消耗仙石，改变属性值
		"""
		self.equipLog(LogDefine.LT_EQUIP_RECAST, roleDBID, roleName, itemID, itemUID, itemName, itemAmount, itemInst, order, "", "", "", "", "", "", "", pickle.dumps(changeAttrchPro))
		
	def equipTranStarLog( self, roleDBID, roleName, srcItemID, srcItemUID, srcItemName, srcItemAmount, dstItemID, dstItemUID, dstItemName, dstItemAmount, TranProData, order = "", itemInst = None ):
		"""
		装备传星
		@param: 角色DBID，角色名，源装备id，源装备uid，源装备名字，源装备数量，目标装备id，目标装备uid，目标装备名字，目标装备数量，传星属性数据
		"""
		self.equipLog(LogDefine.LT_EQUIP_TRAN_STAR, roleDBID, roleName, srcItemID, srcItemUID, srcItemName, srcItemAmount, itemInst, order, dstItemID, dstItemUID, dstItemName, dstItemAmount, "", "", "", pickle.dumps(TranProData))
		
	def equipOpenSaveSlotLog(self, roleDBID, roleName, intensifySaveSlotNum, order = ""):
		"""
		开启强化保存栏位
		@param: 角色DBID，角色名，栏位数，order
		"""
		self.equipLog(LogDefine.LT_EQUIP_OPEN_SAVE_SLOT, roleDBID, roleName, "", "", "", "", None, order, intensifySaveSlotNum)
		
		
	#---------------------------------------------------------------
	# 人物关系
	#---------------------------------------------------------------
	def relationLog( self, type, roleDBID, roleName, tRoleDBID, tRoleName, param1 = "", param2 = "", param3 = "" ):
		"""
		添加人物关系变化日志
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_RELATION, type, roleDBID, roleName, tRoleDBID, tRoleName, param1, param2 , param3 )

	# 师徒
	def teachBuildLog( self, masterDBID, masterName, apprenticeDBID, apprenticeName ):
		"""
		建立师徒关系
		@param: 师父DBID，师父名字，徒弟DBID，徒弟名字
		"""
		self.relationLog( LogDefine.LT_RELATION_TEACHER_BUILD, masterDBID, masterName, apprenticeDBID, apprenticeName )

	def teachRemoveLog( self, masterDBID, masterName, apprenticeDBID, apprenticeName ):
		"""
		解除师徒关系
		@param: 师父DBID，师父名字，徒弟DBID，徒弟名字
		"""
		self.relationLog( LogDefine.LT_RELATION_TEACHER_REMOVE, masterDBID, masterName, apprenticeDBID, apprenticeName )
		
	#---------------------------------------------------------------
	# 幻兽
	#---------------------------------------------------------------
	def petLog( self, action, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel ,petInst = None, param1= "", param2 = "", param3 = "", param4 = "", param5 = "", param6= "", param7 = "", param8 = "", param9 = "", param10 = ""):
		"""
		添加幻兽日志
		"""
		petData = self.getPetData(petInst)
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_PET, action, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, pickle.dumps(petData), param1, param2, param3, param4, param5,param6,param7,param8, param9, param10)
			
	def petAddLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, reason, petInst ):
		"""
		获得幻兽
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，获得原因（途径）
		"""
		self.petLog( LogDefine.LT_PET_ADD, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, reason )

	def petDelLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, reason, petInst ):
		"""
		失去幻兽
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，失去原因
		"""
		self.petLog( LogDefine.LT_PET_LOSE, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, reason)

	def skillPetLearnLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, skillID, usePotential, useMoney , petInst):
		"""
		幻兽学习技能
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，技能ID，销毁潜能，销毁金钱
		"""
		self.petLog( LogDefine.LT_PET_SKILL_LEARN, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, skillID, usePotential, useMoney)

	def petSealLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, useSealCharm, petInst):
		"""
		幻兽封印
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，消耗封印符
		"""
		self.petLog( LogDefine.LT_PET_SEAL, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, useSealCharm)
		
	def petReplaceActiveSkillLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, newSkillID, oldSkillID, skillAmount, petInst, skillBook, useItem, useMoney):
		"""
		幻兽打书 替换主动技能
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，新技能ID，旧技能ID，替换后技能数量，幻兽实例，技能书ID，启化丹消耗数，金钱消耗数
		"""
		self.petLog( LogDefine.LT_PET_REPLACE_SKILL, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, LogDefine.LT_PET_REPLACE_SKILL_ACTIVE, newSkillID, oldSkillID, skillAmount, skillBook, useItem, useMoney)
		
	def petReplacePassiveSkillLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, newSkillID, oldSkillID, skillAmount, petInst, skillBook, useItem, useMoney):
		"""
		幻兽打书 替换被动技能
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，新技能ID，旧技能ID，替换后技能数量，幻兽实例，技能书ID，启化丹消耗数，金钱消耗数
		"""
		self.petLog( LogDefine.LT_PET_REPLACE_SKILL, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, LogDefine.LT_PET_REPLACE_SKILL_PASSIVE, newSkillID, oldSkillID, skillAmount, skillBook, useItem, useMoney)
	
	def petUpgradeActiveSkillLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, skillID, oldSkillID, usePotential, useMoney, petInst):
		"""
		幻兽打书 升级主动技能
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，技能ID，原技能ID，消耗潜能点，消耗金钱，幻兽实例
		"""
		self.petLog( LogDefine.LT_PET_SKILL_UPGRADE, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, LogDefine.LT_PET_REPLACE_SKILL_ACTIVE, skillID, oldSkillID, usePotential, useMoney, 0, 0)
	
	def petUpgradePassiveSkillLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, skillID, oldSkillID, usePotential, useMoney, useBook, useSoulbead, petInst):
		"""
		幻兽打书 升级被动技能
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，技能ID，原技能ID，消耗潜能点，消耗金钱，消耗残卷数, 消耗魂珠数, 幻兽实例
		"""
		self.petLog( LogDefine.LT_PET_SKILL_UPGRADE, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, LogDefine.LT_PET_REPLACE_SKILL_PASSIVE, skillID, oldSkillID, usePotential, useMoney, useBook, useSoulbead)
	
	def petComposeLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, deputyPetName, deputyPetUName, deputyPetUid, deputyPetQuality, deputyPetLevel, oldAbility, newAbility, payMoney, payXianshi, payXianlingguo, petInst):
		"""
		幻兽合成
		@param: 角色DBID，角色名字，主幻兽名字，主幻兽品种型名，主幻兽UID，主幻兽品质，主幻兽等级，副幻兽名字，副幻兽品种型名，副幻兽UID，副幻兽品质，副幻兽等级，合成后成长度，合成前成长度，消耗金钱，消耗仙石，消耗仙灵果
		"""
		self.petLog( LogDefine.LT_PET_COMPOSE, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, deputyPetName, deputyPetUName, deputyPetUid, deputyPetQuality, deputyPetLevel, oldAbility, newAbility, payMoney, payXianshi, payXianlingguo)

	def petUpStepLog( self, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, oldStep, newStep, usePotential, petInst):
		"""
		幻兽升阶
		@param: 角色DBID，角色名字，幻兽名字，幻兽品种型名，幻兽UID，幻兽品质，幻兽等级，升阶前等阶，升阶后等阶，消耗潜能点
		"""
		self.petLog( LogDefine.LT_PET_UP_STEP, roleDBID, roleName, petName, petUname, petUid, petQuality, petLevel, petInst, oldStep, newStep, usePotential)


	#---------------------------------------------------------------
	# 交易
	#---------------------------------------------------------------
	def tradeLog( self, action, roleDBID, roleName, param1 = "", param2 = "", param3 = "", param4 = "", param5 = "", param6 = "", param7 = "", param8 = "", param9 = "", itemInst = None ):
		"""
		添加交易日志
		"""
		itemData = self.getItemBlobData(itemInst)
		KBEDebug.DATABASE_LOG_MSG(LogDefine.LOG_TYPE_TRADE, action, roleDBID, roleName, param1, param2, param3, param4, param5, param6, param7, param8, param9, pickle.dumps(itemData))

	def tradeNpcBuyLog( self, roleDBID, roleName, itemID, itemUID, itemName, amount, payMoney, payBindMoney, grade, shopNPCID, spaceClassName, itemInst ):
		"""
		在NPC商人处买东西
		@param: 角色DBID，角色名字，物品ID，物品uid，物品名字，物品数量，花费金钱，玩家权限，商店NPCID，所在地图
		"""
		self.tradeLog( LogDefine.LT_TRADE_NPC_BUY, roleDBID, roleName, itemID, itemUID, itemName, amount, payMoney, grade, shopNPCID, spaceClassName, "", itemInst )

	def tradeNpcSellLog( self, roleDBID, roleName, itemID, itemUID, itemName, amount, getMoney, grade, shopNPCID, spaceClassName, itemInst ):
		"""
		卖东西给NPC商人
		@param: 角色DBID，角色名字，物品uid，物品名字，物品数量，获得金钱，玩家权限，商店NPCID，所在地图
		"""
		self.tradeLog( LogDefine.LT_TRADE_NPC_SELL, roleDBID, roleName, itemID, itemUID, itemName, amount, getMoney, grade, shopNPCID, spaceClassName, "", itemInst )

	def tradeShopBuyLog( self, roleDBID, roleName, itemID, itemUID, itemName, amount, xianshi, lingshi, xuanshi, money, grade, itemInst ):
		"""
		在商城买东西
		@param: 角色DBID，角色名字，物品uid，物品名字，物品数量，花费金钱，玩家权限
		"""
		self.tradeLog( LogDefine.LT_TRADE_SHOP_BUY, roleDBID, roleName, itemID, itemUID, itemName, amount, xianshi, lingshi, xuanshi, money, grade, itemInst )
		
	def tradeRoleMoneyLog( self, roleDBID, roleName, tRoleDBID, tRolName, subMoney, addMoney ):
		"""
		与玩家交易金钱
		@param: 角色DBID，角色名字，目标DBID，目标名字，失去金钱，获得金钱
		"""
		self.tradeLog( LogDefine.LT_TRADE_SWAP_MONEY, roleDBID, roleName, tRoleDBID, tRolName, subMoney, addMoney )

	def tradeRoleItemLog( self, roleDBID, roleName, tRoleDBID, tRolName, itemID, itemUID, itemName, itemAmount, getMoney, payMoney, channel, itemInst ):
		"""
		与玩家交易物品
		@param: 角色DBID，角色名字，目标DBID，目标名字，物品uid，物品名字，物品数量，获得金钱，消耗金钱，交易途径（摆摊、直接交易等）
		"""
		self.tradeLog( LogDefine.LT_TRADE_SWAP_ITEM, roleDBID, roleName, tRoleDBID, tRolName, itemID, itemUID, itemName, itemAmount, getMoney, payMoney, channel, itemInst )
		
	def tradeRoleItemByTransferLog(self, roleDBID, roleName, tRoleDBID, tRolName, itemID, itemUID, itemName, itemAmount, itemInst, getMoney = 0, payMoney = 0):
		"""
		直接交易
		@param: 角色DBID，角色名字，目标DBID，目标名字，物品uid，物品名字，物品数量
		"""
		self.tradeRoleItemLog(roleDBID, roleName, tRoleDBID, tRolName, itemID, itemUID, itemName, itemAmount, getMoney, payMoney, LogDefine.LT_TRADE_TYPE_TRANSFER, itemInst )
		
	def tradeRoleItemByVendLog(self, roleDBID, roleName, tRoleDBID, tRolName, itemID, itemUID, itemName, itemAmount, getMoney, payMoney, itemInst):
		"""
		摆摊交易
		@param: 角色DBID，角色名字，目标DBID，目标名字，物品uid，物品名字，物品数量，获得金钱，消耗金钱
		"""
		self.tradeRoleItemLog(roleDBID, roleName, tRoleDBID, tRolName, itemID, itemUID, itemName, itemAmount, getMoney, payMoney, LogDefine.LT_TRADE_TYPE_VEND, itemInst )

	def tradeRolePetLog( self, roleDBID, roleName, tRoleDBID, tRolName, petDBID, tradeID, channel ):
		"""
		与玩家交易幻兽
		@param: 角色DBID，角色名字，目标DBID，目标名字，幻兽DBID，交易id，交易途径（摆摊、直接交易等）
		"""
		self.tradeLog( LogDefine.LT_TRADE_SWAP_PET, roleDBID, roleName, tRoleDBID, tRolName, petDBID, tradeID, channel )
		
	def tradeBuyBackLog( self, roleDBID, roleName, itemID, itemUID, itemName, amount, payMoney, grade, shopNPCID, spaceClassName, itemInst ):
		"""
		回购物品
		@param: 角色DBID，角色名字，物品uid，物品名字，物品数量，花费金钱，玩家权限，商店NPCID，所在地图
		"""
		self.tradeLog( LogDefine.LT_TRADE_BUY_BACK, roleDBID, roleName, itemID, itemUID, itemName, amount, payMoney, grade, shopNPCID, spaceClassName, "", itemInst )
		
	def tradeBuyBackHighLog( self, roleDBID, roleName, itemID, itemUID, itemName, amount, payMoney, grade, shopNPCID, spaceClassName, itemInst ):
		"""
		高价回购物品
		@param: 角色DBID，角色名字，物品uid，物品名字，物品数量，花费金钱，玩家权限，商店NPCID，所在地图
		"""
		self.tradeLog( LogDefine.LT_TRADE_BUY_BACK_HIGH, roleDBID, roleName, itemID, itemUID, itemName, amount, payMoney, grade, shopNPCID, spaceClassName, "", itemInst )
		
	def tradeBuyReturnItemLog( self, roleDBID, roleName, itemID, itemUID, itemName, amount, money, grade, shopNPCID, spaceClassName, itemInst ):
		"""
		退货
		@param: 角色DBID，角色名字，物品uid，物品名字，物品数量，获得金钱，玩家权限，商店NPCID，所在地图
		"""
		self.tradeLog( LogDefine.LT_TRADE_RETURN_ITEM, roleDBID, roleName, itemID, itemUID, itemName, amount, money, grade, shopNPCID, spaceClassName, "", itemInst )
		
	def tradeGivingGoodLog( self, roleDBID, roleName, tRoleDBID, tRoleName, itemID, itemName, amount, payXianshi, payXuanshi, payLingshi, payMoney, itemInst ):
		"""
		赠送
		@param: 角色DBID，角色名字，接收玩家DBID，接收角色名字，物品id，物品名字，物品数量，消耗仙石，消耗玄石，消耗灵石，消耗金钱，物品实例
		"""
		self.tradeLog( LogDefine.LT_TRADE_GIVING_GOOD, roleDBID, roleName, tRoleDBID, tRoleName, itemID, itemName, amount, payXianshi, payXuanshi, payLingshi, payMoney, itemInst )

	#---------------------------------------------------------------
	# 邮件
	#---------------------------------------------------------------
	def mailLog(self, action, senderName, receiverName, mailType, title, money, itemData, param1 = "", param2 = ""):
		"""
		添加邮件日志
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_MAIL, action, senderName, receiverName, mailType, title, money, pickle.dumps(itemData), param1, param2 )
	
	def mailSendLog( self, senderName, receiverName, mailType, title, money, bindMoney, itemData ):
		"""
		发送邮件
		@param: 发送者名字，接受者名字，邮件类型，邮件标题，金钱数值，绑定金钱, 物品数据
		"""
		self.mailLog(LogDefine.LT_MAIL_SEND, senderName, receiverName, mailType, title, money, bindMoney, itemData)

	def mailReadLog( self, senderName, receiverName, mailType, title, money, itemData, mailID ):
		"""
		阅读邮件
		@param: 发送者名字，接受者名字，邮件类型，邮件标题，金钱数值，物品数据，邮件ID
		"""
		self.mailLog( LogDefine.LT_MAIL_READ, senderName, receiverName, mailType, title, money, itemData, mailID )

	def mailExtractLog( self, senderName, receiverName, mailType, title, money, itemData, mailID ):
		"""
		提取
		@param: 发送者名字，接受者名字，邮件类型，邮件标题，金钱数值，物品数据，邮件ID
		"""
		self.mailLog( LogDefine.LT_MAIL_EXTRACT, senderName, receiverName, mailType, title, money, itemData, mailID )

	def mailRemoveLog( self, senderName, receiverName, mailType, title, money, itemData, mailID, delType ):
		"""
		删除邮件
		@param: 发送者名字，接受者名字，邮件类型，邮件标题，金钱数值，物品数据，邮件ID，删除类型（原因）
		"""
		self.mailLog( LogDefine.LT_MAIL_DEL, senderName, receiverName, mailType, title, money, itemData, mailID, delType )
	
	#---------------------------------------------------------------
	# 帮会
	#---------------------------------------------------------------
	def tongLog( self, action, tongDBID, tongName, param1 = "", param2 = "", param3 = "", param4 = "", param5 = "", param6 = "", param7 = "" ):
		"""
		添加帮会日志
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_TONG, action, tongDBID, tongName, param1, param2, param3, param4, param5, param6, param7 )
	
	def tongCreateLog( self, tongDBID, tongName, creatorDBID, creatorName  ):
		"""
		帮会创建
		@param: 帮会DIBD，帮会名，创建者DBID，创建者名字
		"""
		self.tongLog( LogDefine.LT_TONG_CREATE, tongDBID, tongName, creatorDBID, creatorName )

	def tongDismissLog( self, tongDBID, tongName, reason ):
		"""
		帮会解散
		@param: 帮会DIBD，帮会名，解散原因
		"""
		self.tongLog( LogDefine.LT_TONG_DISMISS, tongDBID, tongName, reason )

	def tongMoneyChangeLog( self, tongDBID, tongName, oldValue, newValue, reason ):
		"""
		帮会金钱改变
		@param: 帮会DIBD，帮会名，原有金钱，现有金钱，改变原因
		"""
		self.tongLog( LogDefine.LT_TONG_MONEY_CHANGE, tongDBID, tongName, oldValue, newValue, reason )

	def tongItemAddLog( self, tongDBID, tongName, roleDBID, roleName, itemUID, itemName, itemNum ):
		"""
		帮会仓库物品添加
		@param: 帮会DIBD，帮会名，添加物品的成员DBID，添加物品的成员名字，物品uid，物品名字，物品数量
		"""
		self.tongLog( LogDefine.LT_TONG_ITEM_ADD, tongDBID, tongName, roleDBID, roleName, itemUID, itemName, itemNum )

	def tongItemRemoveLog( self, tongDBID, tongName, roleDBID, roleName, itemUID, itemName, itemNum  ):
		"""
		帮会仓库物品移除
		@param: 帮会DIBD，帮会名，删除物品的成员DBID，删除物品的成员名字，物品uid，物品名字，物品数量
		"""
		self.tongLog( LogDefine.LT_TONG_ITEM_REMOVE, tongDBID, tongName, roleDBID, roleName, itemUID, itemName, itemNum )

	def tongLevelChangeLog( self, tongDBID, tongName, oldLevel, nowLevel, reason ):
		"""
		帮会等级改变
		@param: 帮会DIBD，帮会名，原等级，现等级，改变原因
		"""
		self.tongLog( LogDefine.LT_TONG_LEVEl_CHANGE, tongDBID, tongName, oldLevel, nowLevel, reason )

	def tongMemberAddLog( self, tongDBID, tongName, roleDBID, roleName, totalCount ):
		"""
		帮会加入新成员
		@param: 帮会DIBD，帮会名，新成员DBID，新成员名字，当前帮会总人数
		"""
		self.tongLog( LogDefine.LT_TONG_MEMBER_ADD, tongDBID, tongName, roleDBID, roleName, totalCount )

	def tongMemberRemoveLog( self, tongDBID, tongName, roleDBID, roleName, totalCount, reason ):
		"""
		帮会删除成员
		@param: 帮会DIBD，帮会名，删除成员DBID，删除成员名字，当前帮会总人数，删除原因
		"""
		self.tongLog( LogDefine.LT_TONG_MEMBER_LEAVE, tongDBID, tongName, roleDBID, roleName, totalCount, reason )

	def tongLeaderChangeLog( self, tongDBID, tongName, oldLeaderDBID, oldLeaderName, nowLeaderDBID, nowLeaderName, reason = "" ):
		"""
		帮会帮主改变
		@param: 帮会DIBD，帮会名，原帮主DBID，原帮主名字，新帮主DBID，新帮主名字，改变原因
		"""
		self.tongLog( LogDefine.LT_TONG_LEADER_CHANGE, tongDBID, tongName, oldLeaderDBID, oldLeaderName, nowLeaderDBID, nowLeaderName, reason )

	def tongGradeChangeLog( self, tongDBID, tongName, doRoleDBID, doRoleName, setRoleDBID, setRoleName, oldGrade, nowGrade ):
		"""
		帮会设置成员权限
		@param: 帮会DIBD，帮会名，操作者DBID，操作者名字，目标DBID，目标名字，目标原权限，目标新权限
		"""
		self.tongLog( LogDefine.LT_TONG_GRADE_CHANGE, tongDBID, tongName, doRoleDBID, doRoleName, setRoleDBID, setRoleName, oldGrade, nowGrade )	
		
	#order为每次操作的消耗（金钱、材料）识别字，因为消耗和实际操作的日志分开写，所以用order来识别每次的操作和消耗
	def tongContributeChangeLog( self, tongDBID, tongName, memberDBID, memberName, oldContribute, nowContribute, order = "", reason = "" ):
		"""
		帮会成员帮贡改变
		@param: 帮会DIBD，帮会名，改变成员DBID，改变成员名，原帮贡值，新帮贡值，改变原因
		"""
		self.tongLog( LogDefine.LT_TONG_CONTRIBUTE_CHANGE, tongDBID, tongName, memberDBID, memberName, oldContribute, nowContribute, order, reason )
		
		
	#---------------------------------------------------------------
	# 技能
	#---------------------------------------------------------------
	def skillLog( self, action, roleDBID, roleName, skillID, param1 = "", param2 = "", param3 = "", param4 = "", param5 = "", param6 = "" ):
		"""
		添加技能日志
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_SKILL, action, roleDBID, roleName, skillID, param1, param2, param3, param4, param5, param6 )

	def skillLearnLog( self, roleDBID, roleName, skillID, skillName, usePotential, rPotential ):
		"""
		角色学习新技能
		@param: 角色DIBD，角色名，技能ID，技能名字，使用潜能，剩余潜能点，
		"""
		self.skillLog( LogDefine.LT_SKILL_LEARN, roleDBID, roleName, skillID, skillName, usePotential, rPotential )

	def skillUpgradeLog( self, roleDBID, roleName, skillID, oldSkillID, skillName, usePotential, rPotential ):
		"""
		角色升级技能
		@param: 角色DIBD，角色名，新技能ID，原技能ID，技能名字，使用潜能点，剩余潜能点
		"""
		self.skillLog( LogDefine.LT_SKILL_UPGRADE, roleDBID, roleName, skillID, oldSkillID, skillName, usePotential, rPotential )
	
	#---------------------------------------------------------------
	# 充值
	#---------------------------------------------------------------
	def rechargeLog( self, accountDBID, accountName, rechargeType, coinType, value, transactionID ):
		"""
		添加充值日志
		@param: 账号DIBD，账号名字，充值方式，充值类型（金、银元宝），充值数值，订单号
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_RECHARGE, accountDBID, accountName, rechargeType, coinType, value, transactionID )
	
	#---------------------------------------------------------------
	# 账号
	#---------------------------------------------------------------
	def accountLog( self, action, accountDBID, accountName, param1= "", param2 = "", param3 = "" ):
		"""
		添加账号日志
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_ACCOUNT, action, accountDBID, accountName, param1, param2, param3 )
		
	
	def accountLogonLog( self, accountDBID, accountName, ip, intro ):
		"""
		账号登陆
		@param: 账号DIBD，账号名字，账号登录IP，字符介绍
		"""
		self.accountLog( LogDefine.LT_ACCOUNT_LOGON, accountDBID, accountName, ip, intro )

	def accountLogoutLog( self, accountDBID, accountName, ip, intro ):
		"""
		账号下线
		@param: 账号DIBD，账号名字，账号登录IP，字符介绍
		"""
		self.accountLog( LogDefine.LT_ACCOUNT_LOGOUT, accountDBID, accountName, ip, intro )

	def accountRoleAddLog( self, accountDBID, accountName, roleDBID, roleName ):
		"""
		新增角色
		@param: 账号DIBD，账号名字，角色DBID，角色名
		"""
		self.accountLog( LogDefine.LT_ACCOUNT_ROLE_ADD, accountDBID, accountName, roleDBID, roleName )

	def accountRoleDelLog( self, accountDBID, accountName, roleDBID, roleName = "" ):
		"""
		删除账号上的角色
		@param: 账号DIBD，账号名字，角色DBID，角色名
		"""
		self.accountLog( LogDefine.LT_ACCOUNT_ROLE_DEL, accountDBID, accountName, roleDBID, roleName )
		
	def accountLockLog(self, accountDBID, accountName, lockTime, reason, GMUser):
		"""
		封锁账号
		@param: 账号DIBD，账号名字，封号时长，封锁原因，操作GM用户
		"""
		self.accountLog(LogDefine.LT_ACCOUNT_LOCK, accountDBID, accountName, lockTime, reason, GMUser)
		
	def accountUnLockLog(self, accountDBID, accountName, reason, GMUser):
		"""
		解封账号
		@param: 账号DIBD，账号名字，封锁原因，操作GM用户
		"""
		self.accountLog(LogDefine.LT_ACCOUNT_UNLOCK, accountDBID, accountName, reason, GMUser)
		
		
	#---------------------------------------------------------------
	# 角色
	#---------------------------------------------------------------
	def roleLog( self, action, roleDBID, roleName, accountDBID, accountName, param1 = "", param2 = "", param3 = "", param4 = "", param5 = "", blobParam1 = {} , blobParam2 = {} , blobParam3 = {} ):
		"""
		添加角色日志
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_ROLE, action, roleDBID, roleName, accountDBID, accountName, param1, param2, param3, param4, param5, pickle.dumps(blobParam1), pickle.dumps(blobParam2), pickle.dumps(blobParam3) )
		
	def roleLogonLog( self, roleDBID, roleName, accountDBID, accountName, line, level, onlineTime, ip, mac ):
		"""
		角色上线
		@param: 角色DBID，角色名，账号DIBD，账号名字，分线，等级，本次线时间，登录IP，登录MAC地址
		#line 北京需要的是选择区服时候的分线，我们没有，目前默认为1
		"""
		self.roleLog( LogDefine.LT_ROLE_LOGON, roleDBID, roleName, accountDBID, accountName, line, level, onlineTime, ip, mac )

	def roleLogoutLog( self, roleDBID, roleName, accountDBID, accountName, line, level, onlineTime, ip, mac ):
		"""
		角色下线
		@param: 角色DBID，角色名，账号DIBD，账号名字，分线，等级，本次在线时间，登录IP，登录MAC地址
		"""
		self.roleLog( LogDefine.LT_ROLE_LOGOUT, roleDBID, roleName, accountDBID, accountName, line, level, onlineTime, ip, mac )
	
	def roleGagLog( self, roleDBID, roleName, accountDBID, accountName, gagType, gagTime, reason, GMUser ):
		"""
		角色禁言
		@param: 角色DBID，角色名，账号DIBD，账号名字，禁言频道，解除禁言时间，禁言原因，操作GM用户
		"""
		self.roleLog( LogDefine.LT_ROLE_GAG, roleDBID, roleName, accountDBID, accountName, gagType, gagTime, reason, GMUser )
		
	def roleUnGagLog( self, roleDBID, roleName, accountDBID, accountName, gagType, reason, GMUser ):
		"""
		角色解除禁言
		@param: 角色DBID，角色名，账号DIBD，账号名字，解除禁言频道，解除禁言原因，操作GM用户
		"""
		self.roleLog( LogDefine.LT_ROLE_UNGAG, roleDBID, roleName, accountDBID, accountName, gagType, reason, GMUser )
		
	def rolePropertiesLog( self, roleDBID, roleName, accountDBID, accountName, propertyData1, propertyData2, propertyData3 ):
		"""
		角色属性改变
		@param: 角色DBID，角色名，账号DIBD，账号名字，解除禁言频道，解除禁言原因，操作GM用户
		"""
		self.roleLog( LogDefine.LT_ROLE_PRO_RECORD, roleDBID, roleName, accountDBID, accountName, "", "", "", "", "", propertyData1, propertyData2, propertyData3)
		
	#---------------------------------------------------------------
	# 玩家摆摊
	#---------------------------------------------------------------
	def VendLog( self, roleDBID, roleName ):
		"""
		添加玩家摆摊日志
		@param: 角色DBID，角色名
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_VEND, roleDBID, roleName )
		
	#---------------------------------------------------------------
	# 活动、副本日志
	#---------------------------------------------------------------
	def actCopyLog(self, action, actCopyType, actCopyName, roleDBID, roleName, param1 = "", param2 = "", param3 = ""):
		"""
		活动、副本日志
		"""
		KBEDebug.DATABASE_LOG_MSG(LogDefine.LOG_TYPE_ACT_COPY, action, actCopyType, actCopyName, roleDBID, roleName, param1, param2, param3)
		
	def actCopyJoin(self, actCopyType, actCopyName, roleDBID, roleName):
		"""
		活动、副本参与
		@param: 活动、副本类型，角色dbid，角色名
		"""
		self.actCopyLog(LogDefine.LT_ACT_COPY_TYPE_JOIN, actCopyType, actCopyName, roleDBID, roleName)
	
	#---------------------------------------------------------------
	# 在线记录表
	#---------------------------------------------------------------
	def onlineRecord(self, lineNum, onlineRoleNum, onlineMacNum):
		"""
		添加玩家消费日志
		"""
		KBEDebug.DATABASE_LOG_MSG(LogDefine.LOG_TYPE_ONLINE, lineNum, onlineRoleNum, onlineMacNum)
		
	#---------------------------------------------------------------
	# 消费表
	#---------------------------------------------------------------
	def costLog(self, account_id, gid, buy_item_id, buy_item_name, item_price, buy_item_amount, gold_coin_cost, gold_coin_left, bind_coin_cost, bind_coin_left, level):
		"""
		添加玩家消费日志
		"""
		KBEDebug.DATABASE_LOG_MSG(LogDefine.LOG_TYPE_COST, account_id, gid, buy_item_id, buy_item_name, item_price, buy_item_amount, gold_coin_cost, gold_coin_left, bind_coin_cost, bind_coin_left, level)
		
	#---------------------------------------------------------------
	# 道具使用
	#---------------------------------------------------------------
	def propLog(self, line, account_id, gid, level, iid, item_name, rAmount):
		"""
		添加玩家消费日志
		"""
		KBEDebug.DATABASE_LOG_MSG(LogDefine.LOG_TYPE_PROP, line, account_id, gid, level, iid, item_name, rAmount)
		
	#---------------------------------------------------------------
	# 玩家升级
	#---------------------------------------------------------------
	def roleUpLevelLog(self, account_id, gid, level, useTime, lastUpTime):
		"""
		添加玩家消费日志
		"""
		lastUpTimeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastUpTime))
		KBEDebug.DATABASE_LOG_MSG(LogDefine.LOG_TYPE_ROLE_UP_LEVEL, account_id, gid, level, useTime, lastUpTimeStr)
		
	#---------------------------------------------------------------
	# 活动记录
	#---------------------------------------------------------------
	def roleActiveRecord(self, action, account_id, gid, level, bonus_type, bonus_name, start_time, time_used, action_status, spaceScriptID = "", line = 1):
		"""
		添加玩家消费日志
		@param line：填1 就行
		@param action：活动类型，在LogDefine文件中定义，如：ACTIVE_SPACE_TYPE_BHLDZ = 1 帮会掠夺战，如果无法明确活动类型，则使用ACTIVE_SPACE_TYPE_DEFAULT，
						通过spaceScriptID参数来确认活动类型
		@param account_id：账号DBID
		@param gid：角色等级DBID
		@param level：角色等级
		@param bonus_type：奖励类型，在LogDefine文件中定义，1金钱  2绑金  3经验  4潜能  5物品，如果是其他的奖励类型，需要添加到LogDefine中。如果没有奖励，可传空字符串
		@param bonus_name：和bonus_type相关，如果bonus_type是物品，则bonus_name是物品ID，其他天具体的奖励数值。如果没有奖励，可传空字符串
		@param start_time：填活动开始时间，时间戳
		@param time_used：活动开始到结束的消耗时间
		@param action_status：活动完成状态，LogDefine文件中定义，1成功  2失败  3放弃
		@param spaceScriptID：活动的space scriptID，在无法明确是是哪个活动(action参数是ACTIVE_SPACE_TYPE_DEFAULT)的时候用到
		"""
		actionType = action
		if action == LogDefine.ACTIVE_SPACE_TYPE_DEFAULT:
			actionType = LogDefine.ACTIVE_SPACE_SCRIPT_ID_DICT.get(spaceScriptID, spaceScriptID)
		activeName = LogDefine.ACTIVE_SPACE_NAME_DICT.get(actionType, actionType)
		bonusType = ""
		if bonus_type:
			bonusType = LogDefine.ACTIVE_REWARD_TYPE_NAME.get(int(bonus_type), bonus_type)
		startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
		KBEDebug.DATABASE_LOG_MSG(LogDefine.LOG_TYPE_ACTIVE_RECORD, line, activeName, account_id, gid, level, bonusType, bonus_name, startTime, time_used, action_status)
		
		
	#---------------------------------------------------------------
	# 物品加载记录
	#---------------------------------------------------------------
	def ItemLoadLog( self, itemID ):
		"""
		添加物品加载错误记录
		@itemID: 物品ID
		"""
		KBEDebug.DATABASE_LOG_MSG( LogDefine.LOG_TYPE_ITEM_LOAD, itemID )
		
	#================================玩家属性==================================
	def addPropertiesLog(self, player):
		"""
		添加玩家属性日志，方便GM工具查询
		"""
		#因为数据太多导致无法保存到数据库，所以要分开来
		propertyData1 = {}
		propertyData2 = {}
		propertyData3 = {}
		#基础属性，门派(阵营，职业)，等级，境界(阵营，等级，修为)，修为，杀气，功勋，潜能，金钱，战力
		propertyData1.update({"camp": player.getCamp(), "profession": player.getProfession(), "level": player.getLevel(), "xiuwei": player.getXiuwei(), "exp": player.exp,
		"killingValue": player.killingValue, "credit": player.feats, "potential": player.potential, "money": player.getMoney(), "combatPower": player.combatPower})
		#一级属性，根骨，筋力，内力，洞察，身法，移速
		propertyData1.update({"corporeity": player.corporeity, "strength": player.strength, "intellect": player.intellect, "discern": player.discern, "dexterity": player.dexterity, 
			"moveSpeed": player.moveSpeed})
		propertyData2 = {}
		#二级属性
		#气血，内息，罡气，外功攻击，内功攻击，外功防御，内功防御，罡气攻击，罡气防御
		propertyData2.update({"HP_Max": player.HP_Max, "MP_Max": player.MP_Max, "gangQiValue_Max": player.gangQiValue_Max, "damage": player.damage, 
			"magic_damage": player.magic_damage, "armor": player.armor, "magic_armor": player.magic_armor, "gangQi_damagePoint": player.gangQi_damagePoint, 
			"gangQi_armorPoint": player.gangQi_armorPoint})
		#命中率，会心 ,招架 ,闪避率 ,自愈率
		propertyData2.update({"hitrate": player.hitrate, "criticalstrike": player.criticalstrike, "parry": player.parry, "dodgerate": player.dodgerate, 
			"healingrate": player.healingrate})
		
		#以下属性服务器暂时没值
		#冰攻，雷攻，火攻，玄攻，冰抗，雷抗，火抗，玄抗，体力
		propertyData3.update({"bingGong": 0, "leiGong": 0, "huoGong": 0, "xuanGong": 0, "bingKang": 0, "leiKang": 0, "huoKang": 0, "xuanKang": 0, 
			"tiLi": 0})
			
		self.rolePropertiesLog( player.playerDBID, player.playerName, player.accountDBID, "", propertyData1, propertyData2, propertyData3)
		
	#=================================物品数据=================================
	def getItemBlobData(self, itemInst):
		"""
		"""
		itemData = {}
		if not itemInst or not itemInst.isEquip(): #如果为None或者不是装备，则不需要记录数据
			return itemData
		hardiness = round(itemInst.getHardiness() / 10000)
		maxHardness = round(itemInst.getHardinessMax() / 10000)
		itemData.update({"level": itemInst.getLevel(), "quality": itemInst.getQuality(), "hardiness": str(hardiness) + r"/" + str(maxHardness),
			"order": itemInst.getEquipPart(), "price": itemInst.getPrice(), "bindType": itemInst.bindType, "combatPower": itemInst.dynamicData["combatPower"], 
			"classes": itemInst.getReqClass(), "extra": {}})
		extraData = itemInst.getAttachPropertyDict()
		itemData["extra"].update(extraData.get("_extra", {}))
		return itemData
		
	#==================================幻兽数据================================
	def getPetData(self,petInst):
		"""
		"""
		petData = {}
		if not petInst:
			return petData
		petData.update({"name": petInst.name,"level": petInst.level, "uid": petInst.uid, "ability": petInst.ability, "step": petInst.step,"takelevel":petInst.takeLevel,
		"quality":petInst.quality,"scriptID":petInst.scriptID,"camp":petInst.camp,"corporeity":petInst.corporeity,"strength":petInst.strength,"HP_Max":petInst.HP_Max,"MP_Max":petInst.MP_Max,
		"gangQiValue_Max":petInst.gangQiValue_Max,"intellect":petInst.intellect,"discern":petInst.discern,"dexterity":petInst.dexterity,"damage":petInst.damage,"profession":petInst.profession,
		"combatPower":petInst.combatPower,"magic_damage":petInst.magic_damage,"armor":petInst.armor,"magic_armor":petInst.magic_armor,"parry":petInst.parry,
		"speed":petInst.speed,"dodgerate":petInst.dodgerate,"hitrate":petInst.hitrate,"gangQi_damagePoint":petInst.gangQi_damagePoint,"criticalstrike":petInst.criticalstrike,
		"gangQi_armorPoint":petInst.gangQi_armorPoint,"attrSkillBox": list(petInst.attrSkillBox),"passiveSkillBox": list(petInst.passiveSkillBox)})
		return petData
		
		
g_logger = MsgLogger.instance()