import KBEngine
import KBEDebug
import csdefine
from Singleton import Singleton
from ConfigObject.ShopMall.OpenRuleBase import ItemTimeLimit
from ConfigObject.ShopMall.OpenRuleBase import ItemAmountLimit

class ShopMallMgr( Singleton ):
	"""
	商城管理类
	"""
	def __init__( self ):
		self.mapping = {
			str(csdefine.SHOP_TYPE_GIFT):{},
			str(csdefine.SHOP_TYPE_XIANSHI):{},
			str(csdefine.SHOP_TYPE_LINGSHI):{},
			str(csdefine.SHOP_TYPE_XUANSHI):{}
		}
		self.openRuleType = {
				"timeLimit":ItemTimeLimit(),
				"amountLimit":ItemAmountLimit(),
			}

	def init( self, configPath ):
		"""
		配置加载
		"""
		for key,value in configPath.items():
			type = self.mapping.get(value["mallType"])
			if type != None:
				type[key] = value

	def getAll( self ):
		"""
		获得商城所有配置
		"""
		return self.mapping

	def getConfig( self,shopMallTypeId ):
		"""
		获得某个商城配置
		"""
		return self.mapping.get( shopMallTypeId, None )

	def getItemPrice( self, shopMallTypeId, slot, itemID, moneyType):
		"""
		获得某个物品价格
		"""
		shopMallTypeConfig = self.getConfig( shopMallTypeId )
		if shopMallTypeConfig != None:
			item = shopMallTypeConfig.get( slot,None )
			if item != None:
				if item["itemID"] == itemID:
					if moneyType == csdefine.SHOP_MONEY_TYPE_XIANSHI:
						return item["price"].get("xianShi",-1)
					elif moneyType == csdefine.SHOP_MONEY_TYPE_LINGSHI:
						return item["price"].get("lingShi",-1)
					elif moneyType == csdefine.SHOP_MONEY_TYPE_XUANSHI:
						return item["price"].get("xuanShi",-1)
		return -1

	def IsOpen( self, shopMall, data,slot,itemID,amount):
		"""
		验证该商品是否开放
		"""
		for type,value in data.items():
			ruleType = self.openRuleType.get(type,None)
			if ruleType == None:
				KBEDebug.ERROR_MSG("ShopMallMgr ruleType is not in self.openRuleType ")
				return False
			if not ruleType.onVerify(shopMall,slot,itemID,amount):
				return False
		return True

	
g_shopMallMgr = ShopMallMgr()