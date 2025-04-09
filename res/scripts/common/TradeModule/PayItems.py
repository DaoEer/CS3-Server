# -*- coding: utf-8 -*-
import csdefine
import Functions
import csstatus
import cschannel_msgs
import csconst
import ItemTypeEnum
import json
import time
import KBEDebug
import KBEngine
from MsgLogger import g_logger
from ItemFactory import ItemFactoryInst
from TradeModule.TraceBase import PayItemBase

TRADETYPE_TO_PAYREASON_AND_STATUS = {
	csdefine.TRADE_TYPE_CREATE_TONG			 : [csdefine.MONEY_SUB_REASON_CREATE_TONG, 			 csdefine.CHANGE_XIANSHI_NORMAL,				   csstatus.NPCSHOP_ROLE_MONEY_ERROR],
	csdefine.TRADE_TYPE_LEAR_TONG_SKILL		 : [csdefine.MONEY_SUB_REASON_LEARN_TONG_SKILL,		 csdefine.CHANGE_XIANSHI_NORMAL,				   csstatus.NPCSHOP_ROLE_MONEY_ERROR],
	csdefine.TRADE_TYPE_INTENSIFY_EQUIP 	 : [csdefine.MONEY_SUB_REASON_INTENSIFY_EQUIP,		 csdefine.CHANGE_XIANSHI_BY_INTENSIFY_EQUIP,	   csstatus.EQUIP_INTENSIFY_NOT_ENOUGH_MONEY],
	csdefine.TRADE_TYPE_RESET_EQUIP			 : [csdefine.MONEY_SUB_REASON_RESET_EQUIP,			 csdefine.CHANGE_XIANSHI_BY_RESET_EQUIP,		   csstatus.EQUIP_BACKFIRE_NOT_ENOUGH_MONEY],
	csdefine.TRADE_TYPE_SAVE_INTENSIFY_EQUIP : [csdefine.MONEY_SUB_REASON_SAVE_INTENSIFY_EQUIP,	 csdefine.CHANGE_XIANSHI_BY_SAVE_INTENSIFY_EQUIP,  csstatus.EQUIP_INTENSIFY_SAVE_NOT_ENOUGH_MONEY],
	csdefine.TRADE_TYPE_OPEN_INTENSIFY_SAVE_SLOT : [csdefine.MONEY_SUB_REASON_OPEN_INTENSIFY_SAVE_SLOT,	 csdefine.CHANGE_XIANSHI_NORMAL,  csstatus.EQUIP_INTENSIFY_OPEN_SLOT__MONEY_NOT_ENOUGH],
	csdefine.TRADE_TYPE_RESET_INTENSIFY_EQUIP: [csdefine.MONEY_SUB_REASON_RESET_INTENSIFY_EQUIP, csdefine.CHANGE_XIANSHI_BY_RESET_INTENSIFY_EQUIP, csstatus.EQUIP_INTENSIFY_RESTORE_NOT_ENOUGH_MONEY],
	csdefine.TRADE_TYPE_SHUFFLE_EQUIP		 : [csdefine.MONEY_SUB_REASON_SHUFFLE_EQUIP,		 csdefine.CHANGE_XIANSHI_NORMAL,				   csstatus.NPCSHOP_ROLE_MONEY_ERROR],
	csdefine.TRADE_TYPE_RECOST_EQUIP		 : [csdefine.MONEY_SUB_REASON_RECOST_EQUIP,			 csdefine.CHANGE_XIANSHI_NORMAL,				   csstatus.NPCSHOP_ROLE_MONEY_ERROR],
	csdefine.TRADE_TYPE_TRANSFER_EQUIP		 : [csdefine.MONEY_SUB_REASON_TRANSFER_EQUIP,		 csdefine.CHANGE_XIANSHI_NORMAL,				   csstatus.NPCSHOP_ROLE_MONEY_ERROR],
	csdefine.TRADE_TYPE_COMPOSE_EQUIP		 : [csdefine.MONEY_SUB_REASON_COMPOSE_EQUIP,		 csdefine.CHANGE_XIANSHI_NORMAL,				   csstatus.NPCSHOP_ROLE_MONEY_ERROR],
	csdefine.TRADE_TYPE_UNLOCK_PASSIVESKILLBAR: [csdefine.MONEY_SUB_REASON_UNLOCK_PASSIVESKILLBAR,csdefine.CHANGE_XIANSHI_BY_UNLOCK_PASSIVESKILLBAR,csstatus.PASSIVESKILLBAR_MONEY_LOW],
	csdefine.TRADE_TYPE_NPC_SHOP			 : [csdefine.MONEY_SUB_REASON_SHOP_BUY,              csdefine.CHANGE_XIANSHI_NORMAL,					csstatus.NPCSHOP_ROLE_MONEY_ERROR],
	csdefine.TRADE_TYPE_LEARN_SKILL			 : [csdefine.MONEY_SUB_REASON_UPGRADE_SKILL,		csdefine.CHANGE_XIANSHI_NORMAL,						csstatus.CAN_NOT_MONEY_UPGRADE_SKILL],
	csdefine.TRADE_TYPE_ROLE_RARRACKS 		 : [ csdefine.MONEY_SUB_REASON_BARRACKS, csdefine.CHANGE_XIANSHI_NORMAL, csstatus.NPCSHOP_ROLE_MONEY_ERROR ],	
	csdefine.TRADE_TYPE_COMPOSE_TOOL		 : [csdefine.MONEY_SUB_REASON_COMPOSE_TOOL, csdefine.CHANGE_XIANSHI_NORMAL,							csstatus.COMPOSE_TOOL_FAIL_AS_NOEMOUGHT_MONEY],
	csdefine.TRADE_TYPE_JADE_UPGRADE		 : [csdefine.MONEY_SUB_REASON_JADE_UPGRADE, csdefine.CHANGE_XIANSHI_NORMAL,							csstatus.PET_PASSIVE_SKILL_NO_ENOUGH_MONEY],
	csdefine.TRADE_TYPE_GET_JADE			 : [csdefine.MONEY_SUB_REASON_GET_JADE, csdefine.CHANGE_XIANSHI_NORMAL,							csstatus.STORE_NO_ENOUGHMONEY],
	csdefine.TRADE_TYPE_QUENCHING_EQUIP		 : [ csdefine.MONEY_SUB_REASON_MELTHING, csdefine.CHANGE_XIANSHI_NORMAL,							csstatus.STORE_NO_ENOUGHMONEY],
	csdefine.TRADE_TYPE_BUILD_LINGQUAN		 : [ csdefine.MONEY_SUB_REASON_REFLASH_LHMJ_DONGFU,	csdefine.CHANGE_XIANSHI_NORMAL,						csstatus.STORE_NO_ENOUGHMONEY],
	csdefine.TRADE_TYPE_LINGQUAN_UPGRADE	 : [ csdefine.MONEY_SUB_REASON_REFLASH_LHMJ_BUILD, csdefine.CHANGE_XIANSHI_NORMAL,						csstatus.STORE_NO_ENOUGHMONEY],
	csdefine.TRADE_TYPE_REFRESH_TG_QUEST	 : [ csdefine.MONEY_SUB_REASON_REFLASH_TG_QUEST, csdefine.CHANGE_XIANSHI_NORMAL,						csstatus.STORE_NO_ENOUGHMONEY],
	csdefine.TRADE_TYPE_BARRACKS_REVIVE 	 : [csdefine.MONEY_SUB_REASON_BARRACKS, csdefine.CHANGE_XIANSHI_NORMAL, csstatus.NPCSHOP_ROLE_MONEY_ERROR],
	csdefine.TRADE_TYPE_LEARN_PASSIVE_SKILL	 : [csdefine.MONEY_SUB_REASON_UPGRADE_SKILL,		csdefine.CHANGE_XIANSHI_NORMAL,						csstatus.CAN_NOT_MONEY_UPGRADE_SKILL],
	csdefine.TRADE_TYPE_FEED_PET			 : [csdefine.MONEY_SUB_REASON_FEED_PET,		csdefine.CHANGE_XIANSHI_NORMAL, csstatus.STORE_NO_ENOUGHMONEY],
	csdefine.TRADE_TYPE_LEARN_CHUANCHENG_SKILL	 : [csdefine.MONEY_SUB_REASON_UPGRADE_SKILL,		csdefine.CHANGE_XIANSHI_NORMAL,						csstatus.CAN_NOT_MONEY_UPGRADE_SKILL],
	csdefine.TRADE_TYPE_MYSTERIOUS_SHOP		 : [csdefine.MONEY_SUB_REASON_SHOP_BUY,              csdefine.CHANGE_XIANSHI_NORMAL,					csstatus.NPCSHOP_ROLE_MONEY_ERROR]
}

class PayItemXianShi( PayItemBase.PayItemBase ):
	"""
	支付仙石
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return True
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if not player.hasEnoughXianShi(value):
			r = TRADETYPE_TO_PAYREASON_AND_STATUS.get(tradeType)
			player.statusMessage( r[2], "" )
			return False
		return True
		
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		r = TRADETYPE_TO_PAYREASON_AND_STATUS.get(tradeType)
		if not player.payXianShi( value, r[1], order ):
			KBEDebug.ERROR_MSG( "Trade pay xianshi(%d) err!"%value )

class PayItemMoney( PayItemBase.PayItemBase ):
	"""
	支付金钱
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
	
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return True
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if player.money < value:
			r = TRADETYPE_TO_PAYREASON_AND_STATUS.get(tradeType)
			player.statusMessage( r[2], "" )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		r = TRADETYPE_TO_PAYREASON_AND_STATUS.get(tradeType)
		if not player.subMoney( value, r[0], order ):
			KBEDebug.ERROR_MSG( "Trade pay money(%d) err!"%value )

class PayItemBindMoney( PayItemBase.PayItemBase ):
	def __init__(self):
		PayItemBase.PayItemBase.__init__(self)

	def bCellAppPay(self):
		"""是否在cell中支付"""
		return True

	def verifyPay(self, player, tradeType, value):
		"""验证支付条件"""
		if player.bindMoney < value:
			r = TRADETYPE_TO_PAYREASON_AND_STATUS.get(tradeType)
			player.statusMessage(r[2], "")
			return False
		return True

	def pay(self, player, order, tradeType, value):
		"""支付"""
		r = TRADETYPE_TO_PAYREASON_AND_STATUS.get(tradeType)
		if not player.subBindMoney(value, r[0], order):
			KBEDebug.ERROR_MSG("Trade pay bindMoney(%d) err!" % value)

class PayItemMoneyAndBindMoney( PayItemBase.PayItemBase ):
	"""
	支付金钱/绑金(混合支付,绑金优先)
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return True
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if player.money + player.bindMoney < value:
			r = TRADETYPE_TO_PAYREASON_AND_STATUS.get(tradeType)
			player.statusMessage( r[2], "" )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		r = TRADETYPE_TO_PAYREASON_AND_STATUS.get(tradeType)
		if r is None:
			KBEDebug.ERROR_MSG( "Trade pay money/bindMoney(%d) err!"%value )
		if not player.subBindMoneyAndMoney( value, r[0], order ):
			KBEDebug.ERROR_MSG( "Trade pay money/bindMoney(%d) err!"%value )
		
class PayItemPotential( PayItemBase.PayItemBase ):
	"""
	消耗潜能
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
	
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return True
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if player.potential < value:
			if tradeType == csdefine.TRADE_TYPE_JADE_UPGRADE:
				player.statusMessage( csstatus.PET_SKILL_NO_ENOUGH_POTENTIAL, "" )
			elif tradeType == csdefine.TRADE_TYPE_LEARN_SKILL:
				player.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_POTENTIAL_NOT_ENOUGH, "" )
			elif tradeType == csdefine.TRADE_TYPE_GET_JADE:
				player.statusMessage( csstatus.POTENTIAL_NO_EMOUGHT , "")
			elif tradeType == csdefine.TRADE_TYPE_LEARN_PASSIVE_SKILL:
				player.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_POTENTIAL_NOT_ENOUGH, "" )
			elif tradeType == csdefine.TRADE_TYPE_LEARN_CHUANCHENG_SKILL:
				player.statusMessage( csstatus.CAN_NOT_LEARN_SKILL_AS_POTENTIAL_NOT_ENOUGH, "" )
			else:
				player.statusMessage( csstatus.POTENTIAL_NO_EMOUGHT, "" )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		if tradeType == csdefine.TRADE_TYPE_JADE_UPGRADE:
			player.subPotential( value, csdefine.POTENTIAL_REMOVE_REASON_JADE_UPGRADE, order )
		elif tradeType == csdefine.TRADE_TYPE_LEARN_SKILL:
			player.subPotential( value, csdefine.POTENTIAL_REMOVE_REASON_STUDY_SKILL, order )
		elif tradeType == csdefine.TRADE_TYPE_GET_JADE:
			player.subPotential( value, csdefine.POTENTIAL_REMOVE_REASON_ADD_JADE, order )
		elif tradeType == csdefine.TRADE_TYPE_LEARN_PASSIVE_SKILL:
			player.subPotential( value, csdefine.POTENTIAL_REMOVE_REASON_STUDY_SKILL, order )
		elif tradeType == csdefine.TRADE_TYPE_LEARN_CHUANCHENG_SKILL:
			player.subPotential( value, csdefine.POTENTIAL_REMOVE_REASON_STUDY_SKILL, order )
	
class PayItemTongContribute( PayItemBase.PayItemBase ):
	"""
	消耗帮贡
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
	
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return True
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if player.tongContribution < value:
			player.statusMessage(csstatus.CANOT_BUY_GOODS_AS_TONGCONTRIBUTE,"")
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		player.tongMB.subContribution( player.playerDBID, value, order )
	
class PayItemFeats( PayItemBase.PayItemBase ):
	"""
	消耗功勋
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
	
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return True
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if player.feats < value:
			player.statusMessage(csstatus.CANOT_BUY_GOODS_AS_FEATS,"")
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		player.subFeats( value, tradeType )
	
class PayItemCreateTong( PayItemBase.PayItemBase ):
	"""
	创建帮会
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
	
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return False
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		return player.canCreateTong()
	
	def processExt( self, player, order, value ):
		"""
		扩展外部流程
		最后需要调用支付成功、或者失败
		"""
		player.createTong( value )
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		pass
	
class PayItemLearnTongSkill( PayItemBase.PayItemBase ):
	"""
	学习帮会技能
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
	
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return False
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if player.tongMB:
			return True
		return False
	
	def processExt( self, player, order, value ):
		"""
		扩展外部流程
		最后需要调用支付成功、或者失败
		"""
		player.tongMB.tryStudyTongSkill( player.databaseID, value )
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		pass
	
class PayItemStallBuyGoods( PayItemBase.PayItemBase ):
	"""
	摆摊购买物品
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, itemData ):
		"""验证支付条件"""
		amount = itemData.num
		if itemData.amount <= 0 or amount > itemData.amount:
			player.statusMessage( csstatus.STALL_ITEM_AMOUNT_NOT_ENOUGH,"" )
			return False
		if player.anotherRoleTradeEntity is None:
			return False
		totalPrice = itemData.price * amount
		if player.money < totalPrice:
			player.statusMessage( csstatus.NPCSHOP_ROLE_MONEY_ERROR,"" )
			return False
			
		itemInst = player.anotherRoleTradeEntity.getItemInstByUid( int(itemData.id ))
		if not itemInst.isEquip():								# 如果不是装备，需要重新创建！避免出错
			itemInst = ItemFactoryInst.createDynamicItem( itemData.itemID, amount )
		#验证背包格子
		result = player.addItemCheck( itemInst )
		if result != csstatus.ITEM_GO_ON:
			player.statusMessage( result,"" )
			return False
		
		return True
	
	def pay( self, player, order, tradeType, itemData ):
		"""支付"""
		amount = itemData.num
		totalPrice = itemData.price * amount
		another = player.anotherRoleTradeEntity
		
		player.subMoney( totalPrice, csdefine.MONEY_SUB_REASON_ROLE_TRADE, order )
		another.addMoney(totalPrice - int(totalPrice * csconst.ROLE_STALL_PRICE), csdefine.MONEY_ADD_REASON_ROLE_TRADE, order)
		#增加物品
		itemInst = another.getItemInstByUid( int(itemData.id ))
		itemInst.setLock(False)
		another.removeItemByAmount( itemInst, amount, csdefine.ITEM_REMOVE_BY_SELL, True, order )
		
		if not itemInst.isEquip():								# 如果不是装备，需要重新创建！避免出错
			uid = 0 if itemInst.getMaxAmount() > 1 else itemInst.getUid()
			itemInst = ItemFactoryInst.createDynamicItem( itemData.itemID, amount, { "uid" : itemInst.getUid() } )
		player.addItem( itemInst,csdefine.ITEM_ADD_BY_STALLTRADE )
		
		buyItemRecord = {"stallName":another.stallName, "itemName":itemInst.getItemDir("ItemName"),"amount":amount,"totalPrice":totalPrice }
		player.client.CLIENT_StallItemSuccessToClient( csdefine.STALL_SELL_ITEM,buyItemRecord )
		tempSellRecord = { "itemName":itemInst.getItemDir("ItemName"),"playerName":player.playerName,"amount":amount,"tax":int(csconst.ROLE_STALL_PRICE*100),"totalPrice":totalPrice - int(totalPrice * csconst.ROLE_STALL_PRICE),"time":str(Functions.getTime()) }
		another.client.CLIENT_AddStallRecord( csdefine.STALL_SELL_ITEM,tempSellRecord)
		#添加日志，摆摊者为another
		g_logger.tradeRoleItemByVendLog(another.playerDBID, another.getName(), player.playerDBID, player.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, 0, totalPrice, itemInst)
		
class PayItemStallSellGoods( PayItemBase.PayItemBase ):
	"""
	摆摊出售物品
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, itemData ):
		"""验证支付条件"""
		another = player.anotherRoleTradeEntity
		if another is None:
			return False
		amount = itemData.num
		totalPrice = itemData.price * amount
		if amount > itemData.amount:
			player.statusMessage( csstatus.STALL_ITEM_AMOUNT_NOT_ENOUGH,"" )
			return False
		if player.getItemAmountByIDAndBindType( itemData.itemID,False ) < amount:
			player.statusMessage( csstatus.NPCSHOP_SHOP_AMOUNT_ERROR,"" )
			return False
		#验证金钱
		if another.money < totalPrice:
			player.statusMessage( csstatus.NPCSHOP_ROLE_MONEY_ERROR,"" )
			return False
		if not player.isAddMoney( totalPrice ):
			player.statusMessage( csstatus.STALL_SELL_MONEY_LIMIT,"" )
			return False
			
		# 因为装备不能参与摆摊，所以可以直接创建实例
		itemInst = ItemFactoryInst.createDynamicItem( itemData.itemID, amount )
		if itemInst == None:
			return
		#验证背包格子
		result = another.addItemCheck( itemInst )
		if result != csstatus.ITEM_GO_ON:
			player.statusMessage( result,"" )
			return False
		return True
 	
	def pay( self, player, order, tradeType, itemData ):
		"""支付"""
		another = player.anotherRoleTradeEntity
		amount = itemData.num
		totalPrice = itemData.price * amount
		
		player.addMoney(totalPrice - int(totalPrice * csconst.ROLE_STALL_PRICE),csdefine.MONEY_ADD_REASON_ROLE_TRADE, order)
		another.subMoney( totalPrice, csdefine.MONEY_SUB_REASON_ROLE_TRADE, order )
		#减少收购物品
		itemInst = ItemFactoryInst.createDynamicItem( itemData.itemID, amount )
		another.addItem( itemInst,csdefine.ITEM_ADD_BY_STALLTRADE, order )
		#通过物品ID去减少物品
		player.removeItemsByItemID( itemData.itemID, amount, csdefine.ITEM_REMOVE_BY_SELL, csdefine.ITEM_REMOVE_BY_ONLY_NOT_BIND, order )
	
		buyItemRecord = {"stallName":another.stallName, "itemName":itemInst.getItemDir("ItemName"),"amount":amount,"totalPrice":totalPrice }
		player.client.CLIENT_StallItemSuccessToClient( csdefine.STALL_COLLECTION_ITEM, buyItemRecord )
		tempSellRecord = { "itemName":itemInst.getItemDir("ItemName"),"playerName":player.playerName,"amount":amount,"tax":0,"totalPrice":totalPrice,"time":str(Functions.getTime()) }
		another.client.CLIENT_AddStallRecord( csdefine.STALL_COLLECTION_ITEM, tempSellRecord)
		#添加日志
		g_logger.tradeRoleItemByVendLog(player.playerDBID, player.getName(), another.playerDBID, another.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, totalPrice - int(totalPrice * csconst.ROLE_STALL_PRICE), 0, itemInst)
		
class PayItemStone( PayItemBase.PayItemBase ):
	"""
	消耗灵石、仙石
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
	
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return True
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if not player.hasEnoughShiTou( int(value) ):
			player.statusMessage( csstatus.LINGSHI_TRADE_ORDER_XIANSHI_NOT_ENOUGH )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		reason = csdefine.CHANGE_XIANSHI_NORMAL
		if tradeType in csconst.PAY_TRADETYPE_TO_REASON_XIAN_SHI:
			reason = csconst.PAY_TRADETYPE_TO_REASON_XIAN_SHI[tradeType]
		else:
			KBEDebug.ERROR_MSG("Cannot find tradeType!!Please define in csconst.PAY_TRADETYPE_TO_REASON_XIAN_SHI dict")
		player.payShiTou( int(value), reason, order )
		
class PayItemCrystal( PayItemBase.PayItemBase ):
	"""
	消耗 玄晶(强化)
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_XUANJING_CLASS, ItemTypeEnum.ITEM_XUANJING )
		if hasAmountF < value:
			player.statusMessage( csstatus.EQUIP_INTENSIFY_XUANJING_NOT_ENOUGH )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_XUANJING_CLASS, ItemTypeEnum.ITEM_XUANJING )
		player.removeItemListByAmount( itemListF, value, csdefine.ITEM_REMOVE_BY_EQUIP_INTENSIFY, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemMColorCrystal( PayItemBase.PayItemBase ):
	"""
	消耗 五彩玄晶(强化)
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_XUANJING_CLASS, ItemTypeEnum.ITEM_FIVEXUANJING )
		if hasAmountF < value:
			player.statusMessage( csstatus.EQUIP_INTENSIFY_XUANJING_NOT_ENOUGH )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_XUANJING_CLASS, ItemTypeEnum.ITEM_FIVEXUANJING )
		player.removeItemListByAmount( itemListF, value, csdefine.ITEM_REMOVE_BY_EQUIP_INTENSIFY, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemSuperCrystal( PayItemBase.PayItemBase ):
	"""
	消耗 超级玄晶(强化)
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_XUANJING_CLASS, ItemTypeEnum.ITEM_SUPERXUANJING )
		if hasAmountF < value:
			player.statusMessage( csstatus.EQUIP_INTENSIFY_XUANJING_NOT_ENOUGH )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_XUANJING_CLASS, ItemTypeEnum.ITEM_SUPERXUANJING )
		player.removeItemListByAmount( itemListF, value, csdefine.ITEM_REMOVE_BY_EQUIP_INTENSIFY, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemGoodsByID( PayItemBase.PayItemBase ):
	"""
	根据物品ID，消耗 物品
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, datas ):
		"""验证支付条件"""
		for itemID, amount in datas.items():
			hasAmount = 0
			itemList = player.getItemInstsByID(itemID)
			for item in itemList:
				hasAmount += item.getAmount()
			if hasAmount < amount:
				if tradeType == csdefine.TRADE_TYPE_COMPOSE_EQUIP:
					player.statusMessage( csstatus.EQUIP_BUILD_NOT_ENOUGH_MATERIAL )
				elif tradeType == csdefine.TRADE_TYPE_INTENSIFY_EQUIP:
					player.statusMessage( csstatus.EQUIP_INTENSIFY_ATTACHMATERIAL_NOT_ENOUGH )
				elif tradeType == csdefine.TRADE_TYPE_COMPOSE_TOOL:
					player.statusMessage( csstatus.COMPOSE_TOOL_FAIL_AS_NOEMOUGHT_ITEM )
				elif tradeType == csdefine.TRADE_TYPE_PRAY_EQUIP:
					player.statusMessage( csstatus.CANNOT_PRAY_AS_NO_ITEM )
				elif tradeType == csdefine.TRADE_TYPE_QUENCHING_EQUIP:
					player.statusMessage( csstatus.QUENCHING_FAIL_AS_NOEMOUGHT_ITEM )
				elif tradeType == csdefine.TRADE_TYPE_EVOLUTION_PET:
					player.statusMessage( csstatus.EVOLUTION_PET_FAIL_NO_ITEM )
				elif tradeType == csdefine.TRADE_TYPE_BUILD_LINGQUAN:
					player.statusMessage( csstatus.BUILD_DONGFU_NOT_ENOUGH_DATA )
				elif tradeType == csdefine.TRADE_TYPE_LINGQUAN_UPGRADE:
					player.statusMessage( csstatus.BUILD_UPGRADE_NOT_ENOUGH_DATA, cschannel_msgs.CAI_LIAO )
				elif tradeType == csdefine.TRADE_TYPE_ACCEPT_LBC_TASK:
					player.statusMessage( csstatus.TRAIN_SOLDIER_GROUND_NO_ITEM )
				elif tradeType == csdefine.TRADE_TYPE_LEARN_PASSIVE_SKILL:
					player.statusMessage( csstatus.CAN_NOT_MATERIAL_UPGRADE_SKILL )
				return False
		return True
	
	def pay( self, player, order, tradeType, datas ):
		"""支付"""
		for itemID, amount in datas.items():
			itemList = player.getItemInstsByID(itemID)
			player.removeItemListByAmount(itemList, amount, tradeType, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
	
class PayItemGoodsByUID( PayItemBase.PayItemBase ):
	"""
	根据物品UID，消耗 物品
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, datas ):
		"""验证支付条件"""
		for itemUID, amount in datas.items():
			item = player.getItemInstByUid(itemUID)
			if item.getAmount() < amount:
				return False
		return True
	
	def pay( self, player, order, tradeType, datas ):
		"""支付"""
		for itemUID, amount in datas.items():
			item = player.getItemInstByUid(itemUID)
			player.removeItemByAmount(item, amount, csdefine.ITEM_REMOVE_BY_SYS )
	
class PayItemBindGoodsByID( PayItemBase.PayItemBase ):
	"""
	根据物品ID，消耗 绑定物品
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, datas ):
		"""验证支付条件"""
		for itemID, amount in datas.items():
			hasAmount = 0
			itemList = player.getItemInstsByID(itemID)
			for item in itemList:
				if item.isBinded():
					hasAmount += item.getAmount()
			if hasAmount < amount:
				if tradeType == csdefine.TRADE_TYPE_COMPOSE_EQUIP:
					player.statusMessage( csstatus.EQUIP_BUILD_NOT_ENOUGH_MATERIAL )
				return False
		return True
	
	def pay( self, player, order, tradeType, datas ):
		"""支付"""
		for itemID, amount in datas.items():
			itemList = player.getItemInstsByID(itemID)
			player.removeItemListByAmount(itemList, amount, tradeType, csdefine.ITEM_REMOVE_BY_ONLY_IS_BIND, order )
			
class PayItemUnBindGoodsByID( PayItemBase.PayItemBase ):
	"""
	根据物品ID，消耗 不绑定物品
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, datas ):
		"""验证支付条件"""
		for itemID, amount in datas.items():
			hasAmount = 0
			itemList = player.getItemInstsByID(itemID)
			for item in itemList:
				if not item.isBinded():
					hasAmount += item.getAmount()
			if hasAmount < amount:
				if tradeType == csdefine.TRADE_TYPE_COMPOSE_EQUIP:
					player.statusMessage( csstatus.EQUIP_BUILD_NOT_ENOUGH_MATERIAL )
				elif tradeType == csdefine.TRADE_TYPE_COMPOSE_TOOL:
					player.statusMessage( csstatus.COMPOSE_TOOL_FAIL_AS_NOEMOUGHT_ITEM )
				return False
		return True
	
	def pay( self, player, order, tradeType, datas ):
		"""支付"""
		for itemID, amount in datas.items():
			itemList = player.getItemInstsByID(itemID)
			player.removeItemListByAmount(itemList, amount, tradeType, csdefine.ITEM_REMOVE_BY_ONLY_NOT_BIND, order )
		
class PayItemHHSymbol( PayItemBase.PayItemBase ):
	"""
	消耗 回火符
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_HUIHUO )
		if hasAmountF < value:
			if tradeType == csdefine.TRADE_TYPE_RESET_EQUIP:
				player.statusMessage( csstatus.EQUIP_BACK_FU_NOT_ENOUGH )
			elif tradeType == csdefine.TRADE_TYPE_TRANSFER_EQUIP:
				player.statusMessage( csstatus.EQUIP_BIOGRAPHY_NOT_ENOUGH_MATERIAL )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_HUIHUO )
		reason = csdefine.ITEM_REMOVE_BY_EQUIP_INTENSIFY
		if tradeType == csdefine.TRADE_TYPE_TRANSFER_EQUIP:
			reason = csdefine.ITEM_REMOVE_BY_BIOGRAPHY
		player.removeItemListByAmount( itemListF, value, reason, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemZYSymbol( PayItemBase.PayItemBase ):
	"""
	消耗 正阳符
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_ZHENGYANG )
		if hasAmountF < value:
			if tradeType == csdefine.TRADE_TYPE_RESET_EQUIP:
				player.statusMessage( csstatus.EQUIP_BACK_FU_NOT_ENOUGH )
			elif tradeType == csdefine.TRADE_TYPE_TRANSFER_EQUIP:
				player.statusMessage( csstatus.EQUIP_BIOGRAPHY_NOT_ENOUGH_MATERIAL )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_ZHENGYANG )
		reason = csdefine.ITEM_REMOVE_BY_EQUIP_INTENSIFY
		if tradeType == csdefine.TRADE_TYPE_TRANSFER_EQUIP:
			reason = csdefine.ITEM_REMOVE_BY_BIOGRAPHY
		player.removeItemListByAmount( itemListF, value, reason, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemBDSymbol( PayItemBase.PayItemBase ):
	"""
	消耗 北斗符
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_BEIDOU )
		if hasAmountF < value:
			if tradeType == csdefine.TRADE_TYPE_RESET_EQUIP:
				player.statusMessage( csstatus.EQUIP_BACK_FU_NOT_ENOUGH )
			elif tradeType == csdefine.TRADE_TYPE_TRANSFER_EQUIP:
				player.statusMessage( csstatus.EQUIP_BIOGRAPHY_NOT_ENOUGH_MATERIAL )
			elif tradeType == csdefine.TRADE_TYPE_SAVE_INTENSIFY_EQUIP:
				player.statusMessage( csstatus.EQUIP_SAVE_MATERIAL_NOT_ENOUGH )
			elif tradeType == csdefine.TRADE_TYPE_RESET_INTENSIFY_EQUIP:
				player.statusMessage( csstatus.EQUIP_RESTORE_MATERIAL_NOT_ENOUGH )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_BEIDOU )
		reason = csdefine.ITEM_REMOVE_BY_EQUIP_INTENSIFY
		if tradeType == csdefine.TRADE_TYPE_TRANSFER_EQUIP:
			reason = csdefine.ITEM_REMOVE_BY_BIOGRAPHY
		player.removeItemListByAmount( itemListF, value, reason, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemShuffle( PayItemBase.PayItemBase ):
	"""
	消耗洗练石(洗练)
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_RESET_CLASS, ItemTypeEnum.ITEM_WASH )
		if hasAmountF < value:
			player.statusMessage( csstatus.EQUIP_SHUFFLE_STONE_NOT_ENOUGH )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_RESET_CLASS, ItemTypeEnum.ITEM_WASH )
		player.removeItemListByAmount( itemListF, value, csdefine.ITEM_REMOVE_BY_SHUFFLE, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemBloodSymbol( PayItemBase.PayItemBase ):
	"""
	消耗血符（洗练）
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_BLOOD )
		if hasAmountF < value:
			player.statusMessage(csstatus.EQUIP_SHUFFLE_XUEFU_NOT_ENOUGH)
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_BLOOD )
		player.removeItemListByAmount( itemListF, value, csdefine.ITEM_REMOVE_BY_SHUFFLE, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemRecostStone( PayItemBase.PayItemBase ):
	"""
	消耗重铸宝珠(重铸)
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_RESET_CLASS, ItemTypeEnum.ITEM_RECOIN )
		if hasAmountF < value:
			player.statusMessage( csstatus.EQUIP_RECAST_BAOZHU_NOT_ENOUGH )
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_RESET_CLASS, ItemTypeEnum.ITEM_RECOIN )
		player.removeItemListByAmount( itemListF, value, csdefine.ITEM_REMOVE_BY_RECAST, csdefine.ITEM_REMOVE_BY_IS_BIND, order )
		
class PayItemProtectSymbol( PayItemBase.PayItemBase ):
	"""
	消耗重铸保护符（重铸）
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_PROTECT )
		if hasAmountF < value:
			player.statusMessage(csstatus.EQUIP_RECAST_FU_NOT_ENOUGH)
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		hasAmountF, itemListF = player._getMaterialByTypeItemClass( csconst.ITEM_SYMBOL_CLASS, ItemTypeEnum.ITEM_PROTECT )
		player.removeItemListByAmount( itemListF, value, csdefine.ITEM_REMOVE_BY_RECAST, csdefine.ITEM_REMOVE_BY_IS_BIND, order )

class PayItemRoleTrade( PayItemBase.PayItemBase ):
	"""
	玩家之间交易
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		avatar = player.anotherRoleTradeEntity
		srcRoleTradeItemList = list(avatar.dstRoleTradeItem.values())#自己的将要交易的物品
		dstRoleTradeItemList = list(player.dstRoleTradeItem.values())#建议目标的将要交易的物品
		
		#计算自己将会移除物品的格子数，任务物品不能交易，所以不用计算
		srcCommonGridNum = 0 
		srcSparGridNum = 0
		for itemInst, amount in srcRoleTradeItemList:
			if itemInst.isSparItem():
				srcSparGridNum += 1
			elif not itemInst.isQuestItem():
				srcCommonGridNum += 1
		
		#获得自己添加交易目标的物品后剩余的格子数
		commonNum = len(avatar.getAllFreeOrder( ItemTypeEnum.BAG_COMMON ))
		sparNum = len(avatar.getAllFreeOrder( ItemTypeEnum.BAG_SPAR ))
		#如果添加交易目标的交易物品后的剩余格子数 减 自己将要移除的物品的格子数小于0，说明格子说不够
		if commonNum - srcCommonGridNum < 0 or sparNum - srcSparGridNum < 0:
			avatar.changeRoleTradeState( csdefine.TRADE_STATE_NULL, player )
			player.changeRoleTradeState( csdefine.TRADE_STATE_NULL, avatar )
			avatar.statusMessage(csstatus.PLAYERTRADE_KITBAG_NOT_ENOUGH,"")
			player.statusMessage(csstatus.PLAYERTRADE_ANTHOR_KITBAG_NOT_ENOUGH,"")
			return False
				
		#计算交易目标将会移除物品的格子数，任务物品不能交易，所以不用计算
		dstCommonGridNum = 0
		dstSparGridNum = 0
		for itemInst, amount in dstRoleTradeItemList:
			if itemInst.isSparItem():
				dstSparGridNum += 1
			elif not itemInst.isQuestItem():
				dstCommonGridNum += 1
			
		#获得交易目标添加自己的物品后剩余的格子数
		commonNum = len(player.getAllFreeOrder( ItemTypeEnum.BAG_COMMON ))
		sparNum = len(player.getAllFreeOrder( ItemTypeEnum.BAG_SPAR ))

		if commonNum - dstCommonGridNum < 0 or sparNum - dstSparGridNum < 0:
			avatar.changeRoleTradeState( csdefine.TRADE_STATE_NULL, player )
			player.changeRoleTradeState( csdefine.TRADE_STATE_NULL, avatar )
			avatar.statusMessage(csstatus.PLAYERTRADE_ANTHOR_KITBAG_NOT_ENOUGH,"")
			player.statusMessage(csstatus.PLAYERTRADE_KITBAG_NOT_ENOUGH,"")
			return False
				
		#如果自己交易后的金钱数大于最大值，则交易失败
		if not avatar.isAddMoney( avatar.dstRoleTradeMoney - avatar.srcRoleTradeMoney ):
			avatar.changeRoleTradeState( csdefine.TRADE_STATE_NULL, player )
			player.changeRoleTradeState( csdefine.TRADE_STATE_NULL, avatar )
			avatar.statusMessage(csstatus.PLAYERTRADE_MONEY_CANT_GAIN,"")
			player.statusMessage(csstatus.PLAYERTRADE_ANTHOR_MONEY_CANT_GAIN,"")
			return False
		
		#如果交易目标交易后的金钱数大于最大值，则交易失败
		if not player.isAddMoney( player.dstRoleTradeMoney - player.srcRoleTradeMoney ):
			avatar.changeRoleTradeState( csdefine.TRADE_STATE_NULL, player )
			player.changeRoleTradeState( csdefine.TRADE_STATE_NULL, avatar )
			avatar.statusMessage(csstatus.PLAYERTRADE_ANTHOR_MONEY_CANT_GAIN,"")
			player.statusMessage(csstatus.PLAYERTRADE_MONEY_CANT_GAIN,"")
			return False
		return True
	
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		avatar = player.anotherRoleTradeEntity
		avatar.subMoney( avatar.srcRoleTradeMoney, csdefine.MONEY_SUB_REASON_ROLE_TRADE )
		avatar.addMoney( avatar.dstRoleTradeMoney, csdefine.MONEY_ADD_REASON_ROLE_TRADE  )

		player.subMoney( player.srcRoleTradeMoney, csdefine.MONEY_SUB_REASON_ROLE_TRADE )
		player.addMoney( player.dstRoleTradeMoney, csdefine.MONEY_ADD_REASON_ROLE_TRADE )
		
		#添加金钱日志交易
		if avatar.srcRoleTradeMoney > 0:
			g_logger.tradeRoleMoneyLog( player.playerDBID, player.getName(), avatar.playerDBID, avatar.getName(), player.srcRoleTradeMoney, avatar.srcRoleTradeMoney )

		
		for itemUID, amount in avatar.srcRoleTradeItem.values():
			itemInst = avatar.getItemInstByUid( itemUID )
			itemInst.setLock(False)
			avatar.removeItemByAmount( itemInst, amount, csdefine.ITEM_REMOVE_BY_ROLETRADE )
			
		for itemUID, amount in player.srcRoleTradeItem.values():
			itemInst = player.getItemInstByUid( itemUID )
			itemInst.setLock(False)
			player.removeItemByAmount( itemInst, amount, csdefine.ITEM_REMOVE_BY_ROLETRADE )

		for itemInst, amount in avatar.dstRoleTradeItem.values():
			if not itemInst.isEquip() and not itemInst.hasRandomAttrAtInit():			# 如果不是装备，或者在创建时没有随机属性，全部都要重新创建！反正出现相同UID
				uid = 0 if itemInst.getMaxAmount() > 1 else itemInst.getUid()
				itemInst = ItemFactoryInst.createDynamicItem( itemInst.id, amount, {"uid" : uid} )
			else:
				itemInst.setLock( False )
			avatar.addItem( itemInst, csdefine.ITEM_ADD_BY_ROLETRADE )
			#添加物品交易日志
			g_logger.tradeRoleItemByTransferLog( player.playerDBID, player.getName(), avatar.playerDBID, avatar.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, itemInst )

		for itemInst, amount in player.dstRoleTradeItem.values():
			if not itemInst.isEquip() and not itemInst.hasRandomAttrAtInit():			# 如果不是装备，或者在创建时没有随机属性，全部都要重新创建！反正出现相同UID
				uid = 0 if itemInst.getMaxAmount() > 1 else itemInst.getUid()
				itemInst = ItemFactoryInst.createDynamicItem( itemInst.id, amount, {"uid" : uid} )
			else:
				itemInst.setLock( False )
			player.addItem( itemInst, csdefine.ITEM_ADD_BY_ROLETRADE )
			#添加物品交易日志
			g_logger.tradeRoleItemByTransferLog( avatar.playerDBID, avatar.getName(), player.playerDBID, player.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, itemInst )

		avatar.statusMessage( csstatus.PLAYERTRADE_TRADE_SUCCESS,"" )
		player.statusMessage( csstatus.PLAYERTRADE_TRADE_SUCCESS,"" )
		avatar.changeRoleTradeState( csdefine.TRADE_STATE_NULL, player )
		player.changeRoleTradeState( csdefine.TRADE_STATE_NULL, avatar )
		
class PayItemFeedPet( PayItemBase.PayItemBase ):
	"""
	驯养原兽
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return  False
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		return True
		
	def processExt( self, player, order, value ):
		"""
		扩展外部流程
		最后需要调用支付成功、或者失败
		"""
		uid = value["uid"]
		itemID = value["itemID"]
		num = value["num"]
		spaceType = value["spaceType"]
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].feedOriginPet( player, player.databaseID, uid, itemID, num, spaceType )
		return True
		
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		pass
		
class PayItemEvolutionPet( PayItemBase.PayItemBase ):
	"""
	原兽进化为幻兽
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return  False
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		return True
		
	def processExt( self, player, order, value ):
		"""
		扩展外部流程
		最后需要调用支付成功、或者失败
		"""
		uid = value["uid"]
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].evolutionOriginPet( player, player.databaseID, uid )
		return True
		
class PayItemComposeTool( PayItemBase.PayItemBase ):
	"""
	轮回秘境工具打造
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return  False
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		return player.canAddTool( item["itemID"], value["isBinded"] )
		
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		player.doComposeTool( value["itemID"], value["isBinded"] )

class PayItemGenerateOriginPet( PayItemBase.PayItemBase ):
	"""
	原兽入栏
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return False
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		return True
		
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		itemID = value["itemID"]
		player.onGenerateOriginPet( itemID )
		
class PayItemLingNeng( PayItemBase.PayItemBase ):
	"""
	灵能消耗
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
		
	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		if not player.hasEmoughPsionic(value):
			if tradeType == csdefine.TRADE_TYPE_COMPOSE_TOOL:
				player.statusMessage(csstatus.COMPOSE_TOOL_FAIL_AS_NOEMOUGHT_LINGNENG, "")
			elif tradeType == csdefine.TRADE_TYPE_OPEN_BATTLE_FORMATIONS:
				player.statusMessage( csstatus.OPEN_BF_FAIL_AS_NOT_ENOUGH_LN, "")
			else:
				player.statusMessage( csstatus.BUILD_NEED_PSIONIC_NOT_ENOUGH_LN, "")
			return False
		return True
		
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		player.subPsionic( value )
		
class PayItemLHMJShop( PayItemBase.PayItemBase ):
	"""
	轮回秘境商店
	"""
	def __init__( self ):
		PayItemBase.PayItemBase.__init__( self )
		
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return False

	def verifyPay( self, player, tradeType, value ):
		"""验证支付条件"""
		return player.checkItemNum( value["slot"], int(value["amount"]) )
		
	def pay( self, player, order, tradeType, value ):
		"""支付"""
		player.reduceLHMJItem( value["slot"], int(value["amount"]) )
	
	

PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_XIANSHI, PayItemXianShi() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_MONEY, PayItemMoney() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_BIND_MONEY, PayItemBindMoney() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY, PayItemMoneyAndBindMoney() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_POTENTIAL, PayItemPotential() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_CONTRIBUTE, PayItemTongContribute() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_FEATS, PayItemFeats() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_CREATETONG, PayItemCreateTong() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_LEARNTONGSKILL, PayItemLearnTongSkill() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_BUY_STALLGOODS, PayItemStallBuyGoods() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_SELL_STALLGOODS, PayItemStallSellGoods() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_STONE, PayItemStone() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_WASH_STONE, PayItemShuffle() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_BLOOD_SYMBOL, PayItemBloodSymbol() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_RECAST_STONE, PayItemRecostStone() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_RECAST_SYMBOL, PayItemProtectSymbol() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_NORMAL_CRYTAL, PayItemCrystal() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_MCOLOR_CRYTAL, PayItemMColorCrystal() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_SUPPER_CRYTAL, PayItemSuperCrystal() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_GOODS_BY_ID, PayItemGoodsByID() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_GOODS_BY_UID, PayItemGoodsByUID() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_BIND_GOODS_BY_ID, PayItemBindGoodsByID() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_UNBIND_GOODS_BY_ID, PayItemUnBindGoodsByID() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_HH_SYMBOL, PayItemHHSymbol() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_ZY_SYMBOL, PayItemZYSymbol() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_BD_SYMBOL, PayItemBDSymbol() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_ROLE_TRADE, PayItemRoleTrade() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_FEED_PET, PayItemFeedPet() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_EVOLUTION_PET, PayItemEvolutionPet() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_COMPOSE_TOOL, PayItemComposeTool() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_GENERATE_ORIGIN_PET, PayItemGenerateOriginPet() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_LING_NENG, PayItemLingNeng() )
PayItemBase.PayItemBase.regist( csdefine.TRADE_PAY_ITEM_LHMJ_SHOP, PayItemLHMJShop() )