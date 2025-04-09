# -*- coding: utf-8 -*-

import csdefine
import KBEDebug

class TradeInterface( object ):
	"""快捷支付"""
	def __init__( self ):
		pass
		
	def requestPay( self, tradeType, targetID, payDict, *args ):
		"""
		支付流程
		@param tradeType 	: 交易方式（csdefine.TRADE_TYPE_NULL）
		@param targetID		: 交易目标entityID
		@param payItems		: 消耗物品（{ csconst.TRADE_ITEM_TYPE_MONEY : 10000,... } ）
		@param args			: 支付成功回调
		"""
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		self.quickPayImp.startPay(self, tradeType, targetID, payDict, *args)
			
	def verifyPay( self, tradeType, payDict ):
		"""需要远程处理，优先判断本地是否足够支付"""
		return self.quickPayImp.verifyPay( self, tradeType, payDict, {}, {} )
			
	def onSuccessPayCB( self, order, tradeType, targetID, payDict, *args ):
		"""
		成功支付回调
		"""
		if tradeType == csdefine.TRADE_TYPE_NPC_SHOP:			# npc商店交易
			self.onSuccessPayShopItem( payDict, *args )
		elif tradeType == csdefine.TRADE_TYPE_LEARN_SKILL:		# 学习技能
			self.onSuccessPaySkill( *args )
		elif tradeType == csdefine.TRADE_TYPE_LEAR_TONG_SKILL:	# 学习帮会技能
			self.onSuccessPayTongSkill( *args )
		elif tradeType == csdefine.TRADE_TYPE_ROLE_STALL:		# 摆摊
			self.onSuccessPayStall( *args )
		elif tradeType == csdefine.TRADE_TYPE_SHUFFLE_EQUIP:	# 洗练
			self.doShuffleEquip( order, *args )
		elif tradeType == csdefine.TRADE_TYPE_RECOST_EQUIP:
			self.doRecastEquip( order, *args )					# 重铸
		elif tradeType == csdefine.TRADE_TYPE_INTENSIFY_EQUIP:
			self.onIntensify( order, *args )					# 强化
		elif tradeType == csdefine.TRADE_TYPE_RESET_EQUIP:
			self.onBackfire( order, *args )						# 回火
		elif tradeType == csdefine.TRADE_TYPE_OPEN_INTENSIFY_SAVE_SLOT:
			self.openIntensifySaveSlotSuccess( order )			# 开启 装备备份栏位
		elif tradeType == csdefine.TRADE_TYPE_SAVE_INTENSIFY_EQUIP:
			self.onIntensifySave( order, *args)					# 保存装备强化
		elif tradeType == csdefine.TRADE_TYPE_RESET_INTENSIFY_EQUIP:
			self.onReStoreIntensify( order, *args )				# 还原装备强化
		elif tradeType == csdefine.TRADE_TYPE_TRANSFER_EQUIP:
			self.onTransferIntensifyEquip(order, *args)			# 装备传星
		elif tradeType == csdefine.TRADE_TYPE_COMPOSE_EQUIP:
			self.doComposeEquit( order, *args )					# 装备打造
		elif tradeType == csdefine.TRADE_TYPE_UNLOCK_PASSIVESKILLBAR:
			self.onUnLockPassiveSkillBar( order, *args )		# 解锁被动技能栏栏位
		elif tradeType == csdefine.TRADE_TYPE_ROLE_RARRACKS:
			self.onSuccessPayBarracksItem( *args )
		elif tradeType == csdefine.TRADE_TYPE_BARRACKS_REVIVE:	# 天兵营复活
			self.onSuccessPayReviveGuard(*args)
		elif tradeType == csdefine.TRADE_TYPE_COMPOSE_TOOL:
			self.doComposeTool( *args )							# 工具打造
		elif tradeType == csdefine.TRADE_TYPE_QUENCHING_EQUIP:
			self.beginQuenchingEquip( *args )					# 装备淬炼
		elif tradeType == csdefine.TRADE_TYPE_PRAY_EQUIP:
			self.doPrayComposeTime(*args)						# 淬炼
		elif tradeType == csdefine.TRADE_TYPE_GENERATE_ORIGIN_PET:
			self.onGenerateOriginPet()							# 原兽蛋入栏
		elif tradeType == csdefine.TRADE_TYPE_GET_JADE:
			self.onAddJadeItem(*args)							# 获得玲珑玉令
		elif tradeType == csdefine.TRADE_TYPE_JADE_UPGRADE:
			self.onUpgradeJadeItem(*args)						# 玲珑玉令升级
		elif tradeType == csdefine.TRADE_TYPE_BUILD_LINGQUAN:
			self.onBuildDongFuCB(*args)							# 建造洞府
		elif tradeType == csdefine.TRADE_TYPE_LINGQUAN_UPGRADE:
			self.onUpgradeBuildCB(*args)							# 升级灵泉
		elif tradeType == csdefine.TRADE_TYPE_ACCEPT_LBC_TASK:
			self.onAcceptLbcTaskSuccessed(*args)					# 接取练兵场任务
		elif tradeType == csdefine.TRADE_TYPE_REFRESH_TG_QUEST:
			self.doRefreshTGQuest(*args)						# 刷新练兵场任务
		elif tradeType == csdefine.TRADE_TYPE_REPAIR_DF_BUILD:
			self.beginRepairDFBuild(*args)						# 修复洞府建筑
		elif tradeType == csdefine.TRADE_TYPE_LEARN_PASSIVE_SKILL:		# 学习被动技能
			self.onSuccessPayPassiveSkill( *args )
		elif tradeType == csdefine.TRADE_TYPE_MYSTERIOUS_SHOP:		#神秘商人
			self.onSuccessPayMysteriousShopItem( *args )
		elif tradeType == csdefine.TRADE_TYPE_OPEN_BATTLE_FORMATIONS:	# 开启阵图
			self.activeBatteleFormations( *args )
		elif tradeType == csdefine.TRADE_TYPE_LEARN_CHUANCHENG_SKILL:		# 学习传承技能
			self.onSuccessPayChuanChengSkill( *args )

		
	def onFailPayCB( self, tradeType, *args ):
		"""
		支付失败回调
		"""
		if tradeType == csdefine.TRADE_TYPE_NPC_SHOP:
			self.onFailPayShopItem( *args )
		elif tradeType == csdefine.TRADE_TYPE_ROLE_STALL:		# 摆摊
			self.onFailPayStall( *args )
			
	def remoteSuccessPay( self ):
		"""
		远程支付成功回调
		define method
		"""
		self.quickPayImp.onRemoteSuccessPay( self )
		
	def remoteFailPay( self ):
		"""
		远程支付失败回调
		define method
		"""
		self.quickPayImp.onRemoteFailPay( self )
	
		
