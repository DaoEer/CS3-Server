# -*- coding: utf-8 -*-
import time
import Functions
import KST
import KBEngine
from KBEDebug import *

import csdefine
import MysqlUtility
from CustomTable import CustomTable, CustomTableField

#充值的物品类型
GOOD_TYPE_GAME_TIME	= "onlinetime" #在线时长
GOOD_TYPE_XIANSHI		= "xianshi" #仙石
GOOD_TYPE_MONTHCARD	= "monthcard" #月卡


class ChargeOrders(KBEngine.Entity):
	"""
	充值数据类
	"""
	def __init__( self ):
		KBEngine.Entity.__init__(self)

class ChargeOrdersData(CustomTable):
	"""
	充值数据类
	"""
	_main_key_ = "id"
	_tbl_name_ = "tbl_ChargeOrders"
	
	# key = attr name; value = instance of CustomTableField that include field name and field type
	# example: { "id" : CustomTableField( "id", int ), "name" : CustomTableField( "sm_name", str ), "speed" : CustomTableField( "sm_speed", float ) }
	_tbl_field_ = {
		"account"           : CustomTableField( "sm_account", str ),
		"gy_orderId"      	: CustomTableField( "sm_gy_orderId", str ),
		"chargeType"     	: CustomTableField( "sm_chargeType", int ),
		"goodType"             	: CustomTableField( "sm_goodType", str ),
		"amount"            : CustomTableField( "sm_amount", int ),
		"orders_time"       : CustomTableField( "sm_orders_time", int ),
		"pickup_status"     : CustomTableField( "sm_pickup_status", int ),
		"pickup_time"       : CustomTableField( "sm_pickup_time", int ),
		"pickup_count"      : CustomTableField( "sm_pickup_count", int ),
		"rollback_count"    : CustomTableField( "sm_rollback_count", int ),
		"last_rollback_time": CustomTableField( "sm_last_rollback_time", int ),
		"pickup_orderId"    : CustomTableField( "sm_pickup_orderId", str ), #因为元宝增加的接口中需要传一个订单号按照目前的设计，将光宇的订单号传进来显然是不合适的（这里涉及到多条订单一次性提取）
	}

	def __init__( self ):
		"""
		"""
		CustomTable.__init__( self )
	

class RefreshCharge:
	"""
	从订单表中提取
	"""
	def __init__( self, parentEntity ):
		"""
		"""
		self.parentEntity = parentEntity
		self.isRefreshing = False

	def refresh( self ):
		"""
		请求把兑换成功的提取出来
		"""
		if self.isRefreshing:
			assert False
			return
			
		self.isRefreshing = True
		ChargeOrdersData.queryWithKeys( self._onQueryOrdersForRefreshCB, True, 
			account = self.parentEntity.playerName, 
			pickup_status = 0         # 且未提取的
		)
		
	def _onQueryOrdersForRefreshCB( self, sucess, ordersInsts ):
		"""
		"""
		# 异步操作，确定回来的时候entity还在
		if self.parentEntity is None or self.parentEntity.isDestroyed:
			self.isRefreshing = False
			return
			
		if not sucess:
			self.isRefreshing = False
			return
		
		if not ordersInsts:
			self.isRefreshing = False
			return
		
		xianshi_amount = 0			#仙石
		gameTime_amount = 0		#游戏时间
		monthcard_amount = 0		#月卡
		pickup_orderId = str(KBEngine.genUUID64())	#这里生成一个提取码，如果一次性提取了多条，那金元宝和银元宝的数目变化情况就只能通过这个提取码来进行追踪了。
		ordersIDs = []
		for orders in ordersInsts:
			if orders.pickup_status != 0:
				continue
			
			# 计算总获得
			if orders.goodType == GOOD_TYPE_GAME_TIME:
				gameTime_amount += orders.amount
			elif orders.goodType == GOOD_TYPE_XIANSHI:
				xianshi_amount += orders.amount
			elif orders.goodType == GOOD_TYPE_MONTHCARD:
				monthcard_amount += orders.amount
			ordersIDs.append( orders.gy_orderId )

		# 先把更新状态写入到数据库中，当成功写入后，再更新玩家的数据，
		# 以避免数据库操作出问题时出现bug
		sql_cmd = "update {} set sm_pickup_status = 1, sm_pickup_time = {}, sm_pickup_count = sm_pickup_count + 1, sm_pickup_orderId = {} where sm_gy_orderId in ({})"
		sql_cmd = sql_cmd.format( ChargeOrdersData._tbl_name_, int(time.time()), pickup_orderId, ", ".join(("%s",) * len(ordersIDs)) )
		sql_cmd = MysqlUtility.makeSafeSql( sql_cmd, ordersIDs )
		INFO_MSG( "will update charge orders. xianshi = '%s', gameTime = '%s', monthcard = '%s', sql = '%s'" % ( xianshi_amount, gameTime_amount, monthcard_amount, sql_cmd ) )
		KBEngine.executeRawDatabaseCommand( sql_cmd, Functions.Functor( self._onUpdateChargeOrdersCB, pickup_orderId, xianshi_amount, gameTime_amount, monthcard_amount, ordersIDs, sql_cmd ) )

	def _onUpdateChargeOrdersCB( self, pickup_orderId, xianshi_amount, gameTime_amount, monthcard_amount, ordersIDs, cmd, result, rows, insertid, error ):
		"""
		@param xianshi_amount: 如果数据库表数据更新成功，应该给玩家多少
		@param ordersIDs: 被改变的订单列表，如果数据库操作成功，但玩家人不在了，就需要恢复订单的处理
		@param cmd: 执行的是哪条sql语句
		"""
		# 不管最终结果如何，都可以解锁了
		self.isRefreshing = False
		
		if error is not None:
			ERROR_MSG( "execute raw sql '%s' fault!!!; xianshi_amount = '%s', gameTime_amount = '%s', monthcard_amount = '%s', ordersIDs = '%s', error: '%s'" % ( cmd, xianshi_amount, gameTime_amount, monthcard_amount, ordersIDs, error ) )
			return
		
		# 数据库操作成功，需要确定回来的时候entity还在
		if self.parentEntity is None or self.parentEntity.isDestroyed:
			# 如果这时目标不在了——我擦，蛋疼……
			# 需要把之前的修改恢复回来
			sql_cmd = "update {} set sm_pickup_status = 0, sm_pickup_time = 0, sm_pickup_orderId = '', sm_rollback_count = sm_rollback_count + 1, sm_last_rollback_time = {} where sm_gy_orderId in ({})"
			sql_cmd = sql_cmd.format( ChargeOrdersData._tbl_name_, int(time.time()), ", ".join(("%s",) * len(ordersIDs)) )
			sql_cmd = MysqlUtility.makeSafeSql( sql_cmd, ordersIDs )
			KBEngine.executeRawDatabaseCommand( sql_cmd, Functions.Functor( self._onRoolbackCB, sql_cmd ) )
			return
		
		oldxianshi = self.parentEntity.xianshi	#仙石
		oldgametime = self.parentEntity.payTimeBalance
		if xianshi_amount > 0:
			self.parentEntity.addXianShi(xianshi_amount, csdefine.CHANGE_XIANSHI_CHARGE, pickup_orderId)
		if gameTime_amount > 0:
			self.parentEntity.addGameTimeBalance(gameTime_amount * 60) #充值单位是分钟
		#月卡功能暂时还不支持
		self.parentEntity.writeToDB()
		INFO_MSG("%s(%s): xianshi:'%s'->'%s', gametime:'%s'->'%s'" % (self.parentEntity.playerName, self.parentEntity.id, oldxianshi, self.parentEntity.xianshi, oldgametime, self.parentEntity.payTimeBalance))

	def _onRoolbackCB( self, cmd, result, rows, insertid, error ):
		"""
		回滚操作
		"""
		INFO_MSG( "execut raw sql '%s' over. error = '%s', effect rows = '%s'" % ( cmd, error, rows ) )
