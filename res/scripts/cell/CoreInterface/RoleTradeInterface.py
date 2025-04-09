# -*- coding: utf-8 -*-
import KBEngine
import Functions
import KBEDebug
import csdefine
import csstatus
import Define
from ConfigObject.Trade.TradeMgr import g_tradeMgr

class RoleTradeInterface:
	"""
	"""
	def __init__(self):		
		"""
		玩家之间交易类
		"""
		self.roleTradeState = csdefine.TRADE_STATE_NULL
		self.anotherRoleTradeEntity = None
		self.srcRoleTradeMoney = 0
		self.dstRoleTradeMoney = 0
		self.srcRoleTradeItem = {}
		self.dstRoleTradeItem = {}

	def getCurrTradeState( self ):
		"""
		获得当前交易状态
		"""
		return self.roleTradeState

	def setCurrTradeState( self, state ):
		"""
		设置当前交易状态
		"""
		self.roleTradeState = state

	def CELL_requestRoleTrade( self, roleID, anotherID ):
		"""
		<exposed method>
		申请交易	
		"""
		if not self.validateClientCall( roleID ):
			return

		entity = KBEngine.entities.get( anotherID, None )

		if entity == None:
			# 找不到对方则离开交易
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL )
			return
			
		if entity.spaceID != self.spaceID:
			# 交易双方处于同一幅地图
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL )
			return
		if self.position.flatDistTo( entity.position ) > csdefine.TRADE_DISTANCE:
			# 交易双方直线距离大于10米
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL )
			return

		if self.isState(csdefine.ENTITY_STATE_DEAD) or self.getState() >= csdefine.ENTITY_STATE_MAX or\
		entity.isState(csdefine.ENTITY_STATE_DEAD) or entity.getState() >= csdefine.ENTITY_STATE_MAX:
			#交易双方任意一方处于死亡状态
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL )
			return
		# 玩家在处于摆摊，或者交易中
		if self.isState(csdefine.ENTITY_STATE_STALL) or self.roleTradeState != csdefine.TRADE_STATE_NULL:
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL)
			return
		#交易对方处于摆摊，或者交易中
		if entity.isState(csdefine.ENTITY_STATE_STALL) or entity.roleTradeState != csdefine.TRADE_STATE_NULL:
			self.statusMessage( csstatus.PLAYERTRADE_IS_BUSYNESS )
			return
		
		#被对方拉入黑名单中，无法交易
		if entity.cellHadBlacklist(self.playerDBID ):
			self.statusMessage( csstatus.RELATION_MSG_FORBID_TRADE_BLACK_LIST, entity.getName() )
			return

		# 发送邀请
		self.changeRoleTradeState( csdefine.TRADE_STATE_INVITE, entity )
	
	def CELL_onLeaveTargetByRequest( self, srcEntityID ):
		"""
		exposed method
		请求交易时，距离目标10米距离，取消交易
		"""
		if self.anotherRoleTradeEntity:
			self.anotherRoleTradeEntity.statusMessage(csstatus.PLAYERTRADE_IS_FARAWAY, "")
			self.stopTrade()
	
	def onEnterDead(self):
		"""死亡状态"""
		if self.roleTradeState != csdefine.TRADE_STATE_NULL:
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL,"" )
			self.anotherRoleTradeEntity.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL,"" )
			self.stopTrade()
			
	def onLeaveSpaceNotify( self ):
		"""
		离开某地图
		"""
		if self.roleTradeState != csdefine.TRADE_STATE_NULL:
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL,"" )
			self.anotherRoleTradeEntity.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL,"" )
			self.stopTrade()
			
	def onRoleTrade( self, entity ):
		"""
		其他玩家申请交易
		"""
		if self.cellHadBlacklist(entity.playerDBID ):
			return
			
		# 通知客户端
		self.client.CLIENT_onRoleTrade( entity.id, entity.getName() )

	def requestRoleTradeOvertime( self ):
		"""
		请求超时
		"""
		self.anotherRoleTradeEntity.statusMessage( csstatus.PLAYERTRADE_ANTHOR_TRADE_OVER_TIME,self.getName() )
		self.changeRoleTradeState( csdefine.TRADE_STATE_NULL, self.anotherRoleTradeEntity )
		self.statusMessage(csstatus.PLAYERTRADE_TRADE_OVER_TIME,"")
		# 通知客户端
		self.client.CLIENT_tradeOvertime()
	
	def cancelRoleTradeOnLogoff( self ):
		"""
		玩家下线时取消交易
		"""
		if self.getCurrTradeState() == csdefine.TRADE_STATE_NULL:
			return
		self.anotherRoleTradeEntity.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL,"" )
		self.stopTrade()
		
	def stopTrade( self ):
		"""停止交易"""
		if self.getCurrTradeState() == csdefine.TRADE_STATE_WAIT:
			self.anotherRoleTradeEntity.popTimer( self.anotherRoleTradeEntity.roleTradeOvertimeID )
		self.changeRoleTradeState( csdefine.TRADE_STATE_NULL, self.anotherRoleTradeEntity )	
	
	def CELL_agreeRoleTrade( self, roleID ):
		"""
		<exposed method>
		同意交易
		"""
		if not self.validateClientCall( roleID ):
			return
		if self.anotherRoleTradeEntity.spaceID != self.spaceID:
			# 交易双方处于同一幅地图
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL )
			return
		if self.position.flatDistTo( self.anotherRoleTradeEntity.position ) > csdefine.TRADE_DISTANCE:
			# 交易双方直线距离大于10米
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL )
			return

		if self.isState(csdefine.ENTITY_STATE_DEAD) or self.getState() >= csdefine.ENTITY_STATE_MAX or\
		self.anotherRoleTradeEntity.isState(csdefine.ENTITY_STATE_DEAD) or self.anotherRoleTradeEntity.getState() >= csdefine.ENTITY_STATE_MAX:
			#交易双方任意一方处于死亡状态
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL )
			return
		# 玩家在处于摆摊，或者交易中
		if self.isState(csdefine.ENTITY_STATE_STALL):
			self.statusMessage( csstatus.PLAYERTRADE_TRADE_FAIL)
			return
		#交易对方处于摆摊，或者交易中
		if self.anotherRoleTradeEntity.isState(csdefine.ENTITY_STATE_STALL):
			self.statusMessage( csstatus.PLAYERTRADE_IS_BUSYNESS )
			return
		
		self.anotherRoleTradeEntity.popTimer( self.anotherRoleTradeEntity.roleTradeOvertimeID )
		self.changeRoleTradeState( csdefine.TRADE_STATE_BEGIN, self.anotherRoleTradeEntity )
	
	def CELL_onLeaveTarget( self, srcEntityID ):
		"""
		exposed method
		离开目标10米距离，取消交易
		"""
		if self.roleTradeState != csdefine.TRADE_STATE_NULL:
			self.statusMessage( csstatus.PLAYERTRADE_IS_FARAWAY,"" )
			self.anotherRoleTradeEntity.statusMessage( csstatus.PLAYERTRADE_IS_FARAWAY,"" )
			self.stopTrade()

	def CELL_cancelRoleTrade( self, roleID ):
		"""
		<exposed method>
		取消交易
		"""
		if not self.validateClientCall( roleID ):
			return
		if self.getCurrTradeState() == csdefine.TRADE_STATE_WAIT:
			self.statusMessage( csstatus.PLAYERTRADE_CANCEL_REQUEST_TRADE,self.anotherRoleTradeEntity.getName() )
			self.anotherRoleTradeEntity.statusMessage( csstatus.PLAYERTRADE_ANTHOR_CANCEL_REQUERT_TRADE,self.getName() )
		if self.getCurrTradeState() not in [csdefine.TRADE_STATE_WAIT,csdefine.TRADE_STATE_NULL,csdefine.TRADE_STATE_INVITE]:
			self.statusMessage( csstatus.PLAYERTRADE_CANCEL_TRADE,"" )
			self.anotherRoleTradeEntity.statusMessage( csstatus.PLAYERTRADE_ANTHOR_CANCEL_TRADE,"" )
		self.stopTrade()
		
	def CELL_requestRoleTradeMoneyChange( self, roleID, amount ):
		"""
		<exposed method>
		交易改变金币
		"""
		if not self.validateClientCall( roleID ):
			return

		amount = int( amount )
		if self.getMoney() < amount:
			# 金币不够
			return

		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )
		stateClass.changeMoney( self, self.anotherRoleTradeEntity, amount )

	def _getItemTradeOrder( self ):
		""""""
		num = len(self.srcRoleTradeItem)
		if num >= Define.TRADE_GRID_NUM:
			return None
		for i in range(num + 1):
			if i not in self.srcRoleTradeItem:
				return i
		return None

	def CELL_requestRoleTradeItemAdd( self, roleID, swapOrder, kitOrder, amount ):
		"""
		<exposed method>
		交易增加物品
		
		swapOrder为交易面板物品所在格子的序号，从0开始，如果值为-1，则表示是右击背包物品
		"""
		if not self.validateClientCall( roleID ):
			return

		swapOrder = int( swapOrder )
		kitOrder = int( kitOrder )
		amount = int( amount )

		itemInst = self.getItemInstByOrder( kitOrder )
		if itemInst == None:
			# 物品不存在
			return

		if itemInst.isBinded():
			# 绑定物品不能交易
			self.statusMessage( csstatus.PLAYERTRADE_ITEM_ISBIND,"" )
			return
		if itemInst.isQuestItem():
			#任务物品不允许交易
			return
		if itemInst.isFacade():
			#外观类道具不允许交易
			return
		if itemInst.getAmount() < amount:
			KBEDebug.ERROR_MSG("itemInst amount is less(%d) than trade(%d)"%(itemInst.getAmount(), amount))
			return
		if itemInst.isLocking():
			KBEDebug.ERROR_MSG("item is locking!!can not trade!")
			return
			
		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )
		if swapOrder in self.srcRoleTradeItem:			# 替换物品
			stateClass.swapItem( self, self.anotherRoleTradeEntity, swapOrder, kitOrder, itemInst, amount )
			return
		else:
			swapOrder = self._getItemTradeOrder()
			if swapOrder == None:
				stateClass.swapItem( self, self.anotherRoleTradeEntity, len(self.srcRoleTradeItem)-1, kitOrder, itemInst, amount )
				return
			stateClass.addItem( self, self.anotherRoleTradeEntity, swapOrder, kitOrder, itemInst, amount )

	def CELL_requestRoleTradeItemRemove( self, roleID, swapOrder ):
		"""
		<exposed method>
		交易减少物品
		"""
		if not self.validateClientCall( roleID ):
			return
		swapOrder = int( swapOrder )
		if not swapOrder in self.srcRoleTradeItem:
			# 交易格子里面没有这个物品
			KBEDebug.ERROR_MSG( "requestRoleTradeItemRemove %s"%(swapOrder) )
			return
		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )
		stateClass.removeItem( self, self.anotherRoleTradeEntity, swapOrder )

	def CELL_cancelRoleTradeLock( self, roleID ):
		"""
		<exposed method>
		取消交易锁定物品		
		"""
		if not self.validateClientCall( roleID ):
			return

		if self.getCurrTradeState() == csdefine.TRADE_STATE_SURE or self.anotherRoleTradeEntity.getCurrTradeState() == csdefine.TRADE_STATE_SURE:
			#如果玩家当前状态为交易确定状态,不允许取消交易锁定
			return

		if self.getCurrTradeState() != csdefine.TRADE_STATE_LOCK:
			# 玩家不是锁定状态，不需要解锁
			KBEDebug.ERROR_MSG( "role trade state != TRADE_STATE_LOCK" )
			return

		self.changeRoleTradeState( csdefine.TRADE_STATE_BEGIN, self.anotherRoleTradeEntity )

	def CELL_requestRoleTradeLock( self, roleID ):
		"""
		<exposed method>
		交易锁定物品		
		"""
		if not self.validateClientCall( roleID ):
			return
		if self.getCurrTradeState() == csdefine.TRADE_STATE_SURE or self.anotherRoleTradeEntity.getCurrTradeState() == csdefine.TRADE_STATE_SURE:
			#如果玩家当前状态为交易确定状态,不允许交易锁定
			return

		self.changeRoleTradeState( csdefine.TRADE_STATE_LOCK, self.anotherRoleTradeEntity )

	def CELL_requestRoleTradeSure( self, roleID ):
		"""
		<exposed method>
		确定交易		
		"""
		if not self.validateClientCall( roleID ):
			return
		if self.anotherRoleTradeEntity.getCurrTradeState() == csdefine.TRADE_STATE_NULL:
			self.statusMessage(csstatus.PLAYERTRADE_ANTHOR_CANCEL_TRADE,"")
			return
		self.changeRoleTradeState( csdefine.TRADE_STATE_SURE, self.anotherRoleTradeEntity )

	def changeRoleTradeState( self, state, dstEntity ):
		"""
		统一状态机改变接口，任何状态的改变都应该调用此接口统一处理。
		"""
		oldState = self.getCurrTradeState()
		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )

		if not stateClass.changeState( state, self, dstEntity ):
			# 不能转变状态
			return
		
		stateClass = g_tradeMgr.getRoleTradeState( state )
		stateClass.enter( self, dstEntity )
		
		if self.getClient():
			# 通知客户端状态改变，CLIENT_onTradeState要放在changeDstRoleTradeState前面
			self.client.CLIENT_onTradeState( state )
		
		dstEntity.changeDstRoleTradeState( state, self )
		#通知客户端将“锁定/取消锁定”按钮强制置灰
		if state == csdefine.TRADE_STATE_SURE and oldState == csdefine.TRADE_STATE_LOCK:
			dstEntity.client.CLIENT_onDstTradeSure( state )

		if oldState != state and ( oldState == csdefine.TRADE_STATE_LOCK or state == csdefine.TRADE_STATE_LOCK ) and state != csdefine.TRADE_STATE_SURE:
			dstEntity.client.CLIENT_onDstTradeLock( state == csdefine.TRADE_STATE_LOCK )

	def changeDstRoleTradeState( self, state, dstEntity ):
		"""
		<Define method>
		对方改变状态通知己方。判断交易对象是否正确，然后通知状态机，在状态机中决定是否更改。
		"""
		# 有一个例外情况，对方在csdefine.TRADE_SWAP_LOCKAGAIN状态，而己方在csdefine.TRADE_SWAP_DEFAULT状态，那么通知对方离开交易
		# 出现这个情况是因为，对方看到己方已经点了交易按钮情况下，对方点击交易，对方将进入csdefine.TRADE_SWAP_LOCKAGAIN状态并通知己方进入同样的状态
		# 由于网络延时，己方的取消交易消息先于服务器要求己方进入csdefine.TRADE_SWAP_LOCKAGAIN状态的消息到达，此时必须通知对方取消交易而不理会TRADE_SWAP_LOCKAGAIN。
		isError = False
		entity = KBEngine.entities.get( dstEntity.id, None )
		if not isError:
			if entity == None:
				# 找不到对方则离开交易
				isError = True

		if not isError:
			if self.getState() == csdefine.ENTITY_STATE_DEAD or self.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if entity.spaceID != self.spaceID:
				# 交易双方处于同一幅地图
				isError = True

		if not isError:
			if entity.getState() == csdefine.ENTITY_STATE_DEAD or entity.getState() >= csdefine.ENTITY_STATE_MAX:
				#交易双方任意一方处于死亡状态
				isError = True

		if not isError:
			if self.position.flatDistTo( entity.position ) > csdefine.TRADE_DISTANCE:
				# 交易双方直线距离大于10米
				isError = True

		if isError:
			if self.getCurrTradeState() != csdefine.TRADE_STATE_NULL:
				self.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return

		# 正在处理其他交易请求
		if self.anotherRoleTradeEntity != dstEntity and self.getCurrTradeState() != csdefine.TRADE_STATE_NULL:
			if state == csdefine.TRADE_STATE_INVITE:
				# 通知处于繁忙状态
				pass
			dstEntity.changeDstRoleTradeState( csdefine.TRADE_STATE_NULL, self )				# 通知对方离开交易
			return

		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )
		if stateClass == None:
			return

		stateClass.onDstStateChanged( self, dstEntity, state )

	def onRoleTradeMoneyChange( self, amount ):
		"""
		自己改变交易金币
		"""
		self.srcRoleTradeMoney = amount
		# 通知客户端
		self.client.CLIENT_onMoneyChange( amount )

	def onDstRoleTradeMoneyChange( self, amount,dstEntity ):
		"""
		对方改变交易金币
		"""
		self.dstRoleTradeMoney = amount

		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )
		if stateClass == None:
			self.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return

		stateClass.onDstChangeMoney( self, dstEntity, amount )
		# 通知客户端
		self.client.CLIENT_onDstMoneyChange( amount )

	def onRoleTradeItemAdd( self, swapOrder, kitOrder, itemUID, amount ):
		"""
		自己改变交易物品
		"""
		self.srcRoleTradeItem[swapOrder] = (itemUID, amount)
		self.setItemLockState( itemUID, True )
		# 通知客户端
		self.client.CLIENT_onItemAdd( swapOrder, kitOrder, amount )

	def onDstRoleTradeItemAdd( self, dstEntity,swapOrder, itemInst, amount ):
		"""
		对方改变交易物品
		"""
		self.dstRoleTradeItem[swapOrder] = (itemInst, amount)
		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )
		if stateClass == None:
			self.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return

		stateClass.onDstStateChanged( self, dstEntity, self.roleTradeState )
		# 通知客户端
		tempdict = {"id":str(itemInst.id), "uid":str(itemInst.uid),"amount":str(amount) }
		tempdict.update( itemInst.getClientTipDynamicProperty() )
		self.client.CLIENT_onDstItemAdd( swapOrder, Functions.toJsonString( [tempdict] ) )

	def onRoleTradeItemRemove( self, swapOrder ):
		"""
		自己移除交易物品
		"""
		uid, amount = self.srcRoleTradeItem.pop( swapOrder )
		self.setItemLockState( uid, False )
		# 通知客户端
		self.client.CLIENT_onItemRemove( swapOrder )

	def onDstRoleTradeItemRemove( self, swapOrder,dstEntity ):
		"""
		对方移除交易物品
		"""
		del self.dstRoleTradeItem[swapOrder]

		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )
		if stateClass == None:
			self.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return

		stateClass.onDstItemRemoved( self, dstEntity, swapOrder )
		# 通知客户端
		self.client.CLIENT_onDstItemRemove( swapOrder )

	def onRoleTradeItemSwap( self, swapOrder, kitOrder, itemUID, amount ):
		"""自己替换物品"""
		oldUID, oldAmount = self.srcRoleTradeItem.pop( swapOrder )
		self.setItemLockState( oldUID, False )
		
		self.srcRoleTradeItem[swapOrder] = ( itemUID, amount )
		self.setItemLockState( itemUID, True )
		# 通知客户端
		self.client.CLIENT_onItemSwap( swapOrder, kitOrder, amount )
		
	def onDstRoleTradeItemSwap( self, swapOrder, kitOrder, itemInst, dstEntity, amount ):
		"""对方替换物品"""
		self.dstRoleTradeItem[swapOrder] = (itemInst, amount)
		stateClass = g_tradeMgr.getRoleTradeState( self.roleTradeState )
		if stateClass == None:
			self.changeRoleTradeState( csdefine.TRADE_STATE_NULL, dstEntity )
			return

		stateClass.onDstItemSwap( self, dstEntity, swapOrder, kitOrder )
		# 通知客户端
		tempdict = {"id":str(itemInst.id), "uid":str(itemInst.uid),"amount":str(amount), "bindType":str(itemInst.bindType) }
		tempdict.update( itemInst.getClientTipDynamicProperty() )
		self.client.CLIENT_onDstItemSwap( swapOrder, Functions.toJsonString( [tempdict] ) )

	def clearTradeData( self ):
		"""
		清除交易数据
		"""
		for (itemUID,amount) in self.srcRoleTradeItem.values():
			self.setItemLockState( itemUID, False )

		self.roleTradeState = csdefine.TRADE_STATE_NULL
		self.anotherRoleTradeEntity = None
		self.srcRoleTradeItem.clear()
		self.dstRoleTradeItem.clear()
		self.srcRoleTradeMoney = 0
		self.dstRoleTradeMoney = 0

	def CELL_setForbidRoleTradeFC( self, srcEntityID, value ):
		"""
		exposed method
		客户端设置“拒绝交易”
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.forbidRoleTrade = value

	def onOppositeCantTrade(self, srcEntityID):
		"""
		exposed method
		对方不能交易
		"""
		if not self.validatePlayerClientCall( srcEntityID ):
			return
		
		self.statusMessage(csstatus.PLAYERTRADE_IS_BUSYNESS, "")
		entity = KBEngine.entities.get(srcEntityID, None)
		if entity:
			entity.stopTrade()