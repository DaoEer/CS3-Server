import KBEngine
import KBEDebug
import csdefine
from Singleton import Singleton
from ConfigObject.ShopMall.ShopMallMgr import g_shopMallMgr

class CouponMgr( Singleton ):
	"""
	优惠劵管理类
	"""
	def __init__( self ):
		self._configDatas = {}

	def init( self, srcData ):
		"""
		初始化
		"""
		for key,value in srcData.items():
			self._configDatas[key] = value

	def getConfig( self, couponId ):
		"""
		获得该优惠劵的配置
		"""
		return self._configDatas.get(couponId,None)

	def onVerify( self,couponId,shopMallTypeId,slot,itemID ):
		"""
		验证该优惠劵是否适用于该商品
		"""
		couponData = self.getConfig( couponId )
		if couponData != None:
			if couponData["mallType"] == shopMallTypeId:
				shopMallConfig = g_shopMallMgr.getConfig( shopMallTypeId )
				if shopMallConfig != None:
			 		for key,value in shopMallConfig.items():
			 			if key == slot:
			 				if value["itemID"] == itemID:
			 					if couponData["itemType"] == value["itemType"]:
			 						return True
		return False


g_couponMgr = CouponMgr()
	
