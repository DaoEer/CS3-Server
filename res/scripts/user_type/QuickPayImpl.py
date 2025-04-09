# -*- coding: utf-8 -*-

"""
快捷支付（用于交易支付）
"""

import csdefine
import KBEDebug
import time, json
import TradeModule

class QuickPayImpl( dict ):
	"""
	"""
	def __init__( self ):
		self.orderID = ""							# 订单号
		self.tradeType = csdefine.TRADE_TYPE_NULL	# 交易类型
		self.targetID = 0							# 交易目标
		self.pyItems = {}							# 支付物品
		self.args = ()								# 参数
	
	def startPay( self, selfEntity, tradeType, targetID, payDict, *args ):
		"""开始支付"""
		if self.orderID:
			KBEDebug.NOTICE_MSG("Player(id:%d) is paying(order:%s)!!"%(selfEntity.id, self.orderID))
			return
		
		# 订单号
		self.orderID = str(int(time.time() * 1000)) + "_%d_%d_%d"%(selfEntity.id, tradeType, targetID)
		result, baseDict, cellDict = self.verifyPay( selfEntity, tradeType, payDict )
		if not result:
			self.orderID = ""
			selfEntity.onFailPayCB( tradeType, *args )
			return
		
		if baseDict:
			self.pyItems = cellDict
			self.tradeType = tradeType
			self.targetID = targetID
			self.args = args
			selfEntity.base.remotePay( self.orderID, tradeType, baseDict )
			return
			
		self.pay(selfEntity, tradeType, payDict)
		selfEntity.onSuccessPayCB( self.orderID, tradeType, targetID, payDict, *args )
		self.orderID = ""
			
	def verifyPay( self, selfEntity, tradeType, payDict ):
		""""""
		baseDict = {}
		cellDict = {}
		for key, value in payDict.items():
			inst = TradeModule.getInst( key )
			if inst:
				if inst.bCellAppPay():
					# 如果支付失败
					if not inst.verifyPay( selfEntity, tradeType, value ):
						return False, baseDict, cellDict
					else:
						cellDict.update( {key : value} )	
				else:
					baseDict.update({key : json.dumps(value)})#这里这样用，是因为不知道到底是str还是int，转到base不好还原
		return True, baseDict, cellDict
		
	def pay( self, selfEntity, tradeType, payDict ):
		""""""
		for key, value in payDict.items():
			inst = TradeModule.getInst( key )
			inst.pay( selfEntity, self.orderID, tradeType, value )
		
	def onRemoteSuccessPay( self, selfEntity ):
		""""""
		if self.pyItems:
			self.pay( selfEntity, self.tradeType, self.pyItems )
		selfEntity.onSuccessPayCB( self.orderID, self.tradeType, self.targetID, self.pyItems, *self.args )
		self.orderID = ""
		self.tradeType = csdefine.TRADE_TYPE_NULL
		self.targetID = 0
		self.pyItems = {}
		self.args = ()
		
	def onRemoteFailPay( self, selfEntity ):
		""""""
		selfEntity.onFailPayCB( self.tradeType, *self.args )
		self.orderID = ""
		self.tradeType = csdefine.TRADE_TYPE_NULL
		self.targetID = 0
		self.pyItems = {}
		self.args = ()
		
	
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		temp = {}
		temp["orderID"] = self.orderID
		temp["tradeType"] = self.tradeType
		temp["targetID"] = self.targetID
		temp["args"] = self.args
		temp["pyItems"] = self.pyItems
		return temp
		
	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = QuickPayImpl()
		obj.orderID = dict["orderID"]
		obj.tradeType = dict["tradeType"]
		obj.targetID = dict["targetID"]
		obj.args = dict["args"]
		obj.pyItems = dict["pyItems"]
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, QuickPayImpl )

instance = QuickPayImpl()