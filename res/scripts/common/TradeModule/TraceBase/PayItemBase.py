# -*- coding: utf-8 -*-
import json
import csdefine

class PayItemBase( object ):
	#交换目标（交易得到或者支付的内容）
	_DATAS = {}
	@classmethod
	def regist( SELF, itemType, itemObject ):
		"""
		注册实例
		"""
		SELF._DATAS[ itemType ] = itemObject 
	
	@classmethod
	def getClass( SELF, itemType ):
		"""
		获取实例
		"""
		return SELF._DATAS[ itemType ]
	
	def bCellAppPay( self ):
		"""是否在cell中支付"""
		return True
	
	def verifyPay( self, tradeType, entity, value ):
		"""
		验证支付条件
		"""
		return True
	
	def processExt( self, entity, order, value ):
		"""
		扩展外部流程
		最后需要调用支付成功、或者失败
		"""
		return False
	
	def pay( self, entity, value ):
		"""
		支付
		"""
		pass
	
