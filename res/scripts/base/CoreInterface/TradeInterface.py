# -*- coding: utf-8 -*-
import json
import csstatus
import csdefine
import TradeModule
import KBEDebug

class TradeInterface( object ):
	def __init__( self ):
		pass
		
	def remotePay( self, order, tradeType, baseDict ):
		"""
		define method
		远程支付
		"""
		for key, value in baseDict.items():
			inst = TradeModule.getInst( key )
			if not inst.verifyPay( self, tradeType, json.loads(value) ):
				self.cell.remoteFailPay()
				return
				
		# 定义一个可供外部扩展流程的方法
		for key, value in baseDict.items():
			inst = TradeModule.getInst( key )
			if inst.processExt( self, order, json.loads(value) ):
				return
				
		for key, value in baseDict.items():
			inst = TradeModule.getInst( key )
			inst.pay( self, order, tradeType, json.loads(value) )
		self.cell.remoteSuccessPay()