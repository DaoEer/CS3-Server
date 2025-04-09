# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import csdefine

from ConfigObject.Trade.RoleTradeState.RoleTradeStateBase import RoleTradeStateBase

class RoleTradeStateBegin( RoleTradeStateBase ):
	"""
	玩家开始交易状态
	"""
	def __init__( self, tradeMgr ):
		"""
		"""
		RoleTradeStateBase.__init__( self, tradeMgr )

	def enter( self, srcEntity, dstEntity ):
		"""
		virtual method
		进入此状态后在此函数中做一些初始化，
		srcEntity: 进入此状态的entity
		dstEntity: 交易对象的entity
		"""
		srcEntity.roleTradeState = csdefine.TRADE_STATE_BEGIN

	def leave( self, state, srcEntity, dstEntity ):
		"""
		virtual method
		离开此状态后在此函数中做一些变化
		@summary			:	交易状态改变
		@type	state		:	UINT8
		@param	state		:	改变的状态
		@type	srcEntity	:	entity
		@param	srcEntity	:	主动改变状态的entity
		@type	dstEntity	:	entity
		@param	dstEntity	:	被影响的entity
		"""
		pass

	def changeState( self, state, srcEntity, dstEntity ):
		"""
		virtual method
		@summary			:	交易状态改变
		@type	state		:	UINT8
		@param	state		:	改变的状态
		@type	srcEntity	:	entity
		@param	srcEntity	:	主动改变状态的entity
		@type	dstEntity	:	entity
		@param	dstEntity	:	被影响的entity
		@rtype:	BOOL,能够改变到state状态则返回True，否则返回False
		"""
		if state == csdefine.TRADE_STATE_NULL:				# 离开交易
			return True

		if state == csdefine.TRADE_STATE_LOCK:				# 进入此状态不影响对方
			return True

		return False

	def addItem( self, srcEntity, dstEntity, swapOrder, kitOrder, itemInst, amount ):
		"""
		virtual method
		交易物品的增加
		@type	srcEntity		:	entity
		@param	srcEntity		:	主动改变物品的entity
		@type	dstEntity		:	entity
		@param	dstEntity		:	被影响的entity
		@type	swapOrder		:	改变的交易栏位置
		@param	swapOrder		:	UINT8
		@type	kitOrder		:	背包号
		@param	kitOrder		:	UINT8
		@type	itemInstance	:	物品实例
		@param	itemInstance	:	ITEM
		"""
		isError = False
		if not isError:
			if dstEntity == None:
				# 找不到对方则离开交易
				isError = True

		if not isError:
			if srcEntity.getState() == csdefine.ENTITY_STATE_DEAD or srcEntity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if srcEntity.spaceID != dstEntity.spaceID:
				# 交易双方处于同一幅地图
				isError = True

		if not isError:
			if dstEntity.getState() == csdefine.ENTITY_STATE_DEAD and dstEntity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if srcEntity.position.flatDistTo( dstEntity.position ) > csdefine.TRADE_DISTANCE:
				# 交易双方直线距离大于10米
				isError = True

		if isError:
			srcEntity.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return
		srcEntity.onRoleTradeItemAdd( swapOrder, kitOrder, itemInst.uid, amount )
		dstEntity.onDstRoleTradeItemAdd( srcEntity,swapOrder, itemInst, amount )

	def removeItem( self, srcEntity, dstEntity, swapOrder ):
		"""
		virtual method
		移除一个物品
		@type	srcEntity		:	entity
		@param	srcEntity		:	主动改变物品的entity
		@type	dstEntity		:	entity
		@param	dstEntity		:	被影响的entity
		@type	swapOrder		:	改变的交易栏位置
		@param	swapOrder		:	UINT8
		"""
		isError = False
		if not isError:
			if dstEntity == None:
				# 找不到对方则离开交易
				isError = True

		if not isError:
			if srcEntity.getState() == csdefine.ENTITY_STATE_DEAD or srcEntity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if srcEntity.spaceID != dstEntity.spaceID:
				# 交易双方处于同一幅地图
				isError = True

		if not isError:
			if dstEntity.getState() == csdefine.ENTITY_STATE_DEAD and dstEntity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if srcEntity.position.flatDistTo( dstEntity.position ) > csdefine.TRADE_DISTANCE:
				# 交易双方直线距离大于10米
				isError = True

		if isError:
			srcEntity.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return

		srcEntity.onRoleTradeItemRemove( swapOrder )
		dstEntity.onDstRoleTradeItemRemove( swapOrder, srcEntity )
		
	def swapItem( self, srcEntity, dstEntity, swapOrder, kitOrder, itemInst, amount ):
		"""
		virtual method
		替换物品
		"""
		isError = False
		if not isError:
			if dstEntity == None:
				# 找不到对方则离开交易
				isError = True

		if not isError:
			if srcEntity.getState() == csdefine.ENTITY_STATE_DEAD or srcEntity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if srcEntity.spaceID != dstEntity.spaceID:
				# 交易双方处于同一幅地图
				isError = True

		if not isError:
			if dstEntity.getState() == csdefine.ENTITY_STATE_DEAD and dstEntity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if srcEntity.position.flatDistTo( dstEntity.position ) > csdefine.TRADE_DISTANCE:
				# 交易双方直线距离大于10米
				isError = True

		if isError:
			srcEntity.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return
		
		srcEntity.onRoleTradeItemSwap( swapOrder, kitOrder, itemInst.uid, amount )
		dstEntity.onDstRoleTradeItemSwap( swapOrder, kitOrder, itemInst, srcEntity, amount )

	def changeMoney( self, srcEntity, dstEntity, amount ):
		"""
		virtual method
		改变金钱
		@type	srcEntity		:	entity
		@param	srcEntity		:	主动改变物品的entity
		@type	dstEntity		:	entity
		@param	dstEntity		:	被影响的entity
		@type	amount			:	金钱数量
		@param	amount			:	UINT32
		"""
		isError = False
		if not isError:
			if dstEntity == None:
				# 找不到对方则离开交易
				isError = True

		if not isError:
			if srcEntity.getState() == csdefine.ENTITY_STATE_DEAD or srcEntity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if srcEntity.spaceID != dstEntity.spaceID:
				# 交易双方处于同一幅地图
				isError = True

		if not isError:
			if dstEntity.getState() == csdefine.ENTITY_STATE_DEAD and dstEntity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if srcEntity.position.flatDistTo( dstEntity.position ) > csdefine.TRADE_DISTANCE:
				# 交易双方直线距离大于10米
				isError = True

		if isError:
			srcEntity.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return

		srcEntity.onRoleTradeMoneyChange( amount )
		dstEntity.onDstRoleTradeMoneyChange( amount,srcEntity )

	def onDstStateChanged( self, srcEntity, dstEntity, state ):
		"""
		当交易对象状态改变时收到通知

		srcEntity: 进入此状态的entity
		dstEntity: 交易对象的entity
		state: 交易对象的当前交易状态
		"""
		if state == csdefine.TRADE_STATE_NULL:
			srcEntity.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return

	def onDstItemAdd( self, srcEntity, dstEntity, swapOrder, itemInstance ):
		"""
		当交易对象改变物品时收到通知

		srcEntity: 进入此状态的entity
		dstEntity: 交易对象的entity
		swapOrder: 欲改变的交易栏目标位置
		itemInstance: 物品实例
		"""
		pass

	def onDstItemRemoved( self, srcEntity, dstEntity, swapOrder ):
		"""
		当交易对象移除物品时收到通知

		srcEntity: 进入此状态的entity
		dstEntity: 交易对象的entity
		swapOrder: 欲移除的交易栏目标位置
		"""
		pass
		
	def onDstItemSwap( self, srcEntity, dstEntity, swapOrder, kitOrder ):
		"""
		当交易对象替换物品时收到通知
		"""
		pass

	def onDstChangeMoney( self, srcEntity, dstEntity, amount ):
		"""
		当交易对象改变金钱时收到通知
		srcEntity: 进入此状态的entity
		dstEntity: 交易对象的entity
		amount: 欲改变的金钱数量
		"""
		pass