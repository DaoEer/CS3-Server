# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
class RoleShopMallInterface( object ):
	def __init__( self ):
		pass
		
	def set_xianshi(self, old):
		#这里感觉应该是引擎底层有些不对，都还没执行__init__函数，就执行了这里了
		if hasattr(self, "eventObj"):
			self.eventObj.fireEvent("Event_OnxianshiChanged", self.xianshi)
		
	def set_lingshi(self, old):
		#这里感觉应该是引擎底层有些不对，都还没执行__init__函数，就执行了这里了
		if hasattr(self, "eventObj"):
			self.eventObj.fireEvent("Event_OnlingshiChanged", self.lingshi)
			
	def set_xuanshi(self, old):
		#这里感觉应该是引擎底层有些不对，都还没执行__init__函数，就执行了这里了
		if hasattr(self, "eventObj"):
			self.eventObj.fireEvent("Event_OnxuanshiChanged", self.xuanshi)
	
	def GetShopMallItemList( self, str ):
		pass
	
	def InitGoodsDataRecord( self, str ):
		pass
	
	def AddGivingGoodsDataRecord( self, str ):
		pass
	
	def AddReceiveGoodsDataRecord( self, str ):
		pass
	
	def DealReceiveGivingGoodsDataCB( self, str ):
		pass
	
	def ChangeGivingGoodsDataCB( self, str ):
		pass
	
	def ClearGivingGoodsDataRecordCB( self, strList ):
		pass
	
	def ClearReceiveGoodsDataRecordCB( self, strList ):
		pass
		
	def InitCouponItem(self, param):
		pass
		
	def AddCouponItem(self, param):
		pass
		
	def RemoveCouponItem(self, param):
		pass
		
