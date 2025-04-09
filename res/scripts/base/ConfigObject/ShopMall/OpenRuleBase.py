import KBEngine
from KBEDebug import *
from csdefine import *
import time
import datetime

class OpenRuleBase:
	def __init__( self ):
		pass
	
	def verity(self, shopMall,slot,itemID,amount):
		return True

class ItemAmountLimit(OpenRuleBase):
	def __init__( self ):
		pass
	
	def onVerify(self, shopMall,slot,itemID,amount):
		"""
		验证物品数量限制
		"""
		return shopMall.reduceShopMallItem( slot,itemID,amount )

class ItemTimeLimit(OpenRuleBase):
	def __init__( self ):
		pass

	def onVerify( self, shopMall,slot,itemID,amount ):
		"""
		验证物品开放时间
		"""
		nowTime = time.time()
		item = shopMall.getItemConfig(slot)
		if item != None:
			if item["itemID"] == itemID:
				itemTimeLimit = item["openRule"].get("timeLimit",None)
				if itemTimeLimit != None:
					if len(itemTimeLimit) > 0:	#判断配置是否有错
						i = 0
						while( i < len(itemTimeLimit) ):
							startTimeLimit = time.mktime((datetime.datetime(itemTimeLimit[i][0],itemTimeLimit[i][1],itemTimeLimit[i][2],itemTimeLimit[i][3],itemTimeLimit[i][4],itemTimeLimit[i][5])).timetuple())
							endTimeLimit = 	time.mktime((datetime.datetime(itemTimeLimit[i][6],itemTimeLimit[i][7],itemTimeLimit[i][8],itemTimeLimit[i][9],itemTimeLimit[i][10],itemTimeLimit[i][11])).timetuple())				
							i += 1
							if nowTime >= startTimeLimit:
								if nowTime < endTimeLimit:
									return True

		return False