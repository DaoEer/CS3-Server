# -*- coding: utf-8 -*-

import pickle
import KBEDebug
import KBEngine
import time
import datetime
import Functions
import csdefine
import csconst
import ItemTypeEnum
from ItemFactory import ItemFactoryInst as g_itemFactory
import Item.ItemSortByTypeCfg as ItemSortByTypeCfg


class ItemBase:
	"""
	物品基类
	"""
	def __init__(self, srcData):
		""""""
		self.dynamicData = {}
		self.tempData = {}
		self.amount = 1
		self.ownerID = 0
		self.order = -1
		self.itemEndTime = ""
		self.id = srcData.get('ItemID')
		self.useAmount = ""
		if srcData.get("UseAmount",""):	#使用限量 useAmount[0] 代表时间  useAmount[1] 代表使用限量
			self.useAmount = [int(item) for item in srcData.get("UseAmount").split("|")]
		
		self.overlyingType = csdefine.ITEM_OVERLYING_TYPE_NONE		# 累加类型
		self.overlyingMax = 1										# 最大累加值
		overlyingData = srcData.get("StackAmount", "")			
		if overlyingData:
			itemUseDataList = overlyingData.split("|")
			if len(itemUseDataList) > 0:
				self.overlyingType = int(itemUseDataList[0])
				# 叠加数
				if self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_STACK:
					self.overlyingMax = int( itemUseDataList[1] )
				# 次数
				elif self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_TIME:
					self.overlyingMax = int( itemUseDataList[1] )
					self.amount = max(self.overlyingMax, 1 )
				# 充能
				elif self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_EMPOWER:
					self.overlyingMax = int( itemUseDataList[1] )
					self.amount = int( itemUseDataList[2] )
					
		srcBindType = srcData.get("BindType", ItemTypeEnum.NONE_BIND)
		if srcBindType in [ItemTypeEnum.NONE_BIND, ItemTypeEnum.EQUIP_BIND]:
			self.bindType = ItemTypeEnum.BIND_NONT_STATE			#未绑定
		else:
			self.bindType = ItemTypeEnum.BINDED_STATE				#绑定
		
	def loadDynamicData( self, params ):
		"""加载动态数据"""
		if "uid" in params:
			self.uid = params["uid"]
		else:
			self.uid = KBEngine.genUUID64()
		if "order" in params:
			self.order = params["order"]
		if "amount" in params:
			self.amount = params["amount"]
		if "ownerID" in params:
			self.ownerID = params["ownerID"]
		if "bindType" in params:
			self.bindType = params["bindType"]
		if "itemEndTime" in params:
			self.itemEndTime = params["itemEndTime"]
		if "dynamicData" in params:
			self.dynamicData = params["dynamicData"]
		if "tempData" in params:
			if params["tempData"]:
				self.tempData = params["tempData"]
			else:
				self.tempData = {}
		
	def getDictFromObj(self):
		"""
		转化为字典打包传输或保存到数据库
		"""
		data = {
			"id": self.id,
			"uid": self.uid,
			"amount": self.amount,
			"order" : self.order,
			"ownerID": self.ownerID,
			"bindType": self.bindType,
			"itemEndTime": self.itemEndTime,
			"dynamicData": self.dynamicData,
			"tempData" : self.tempData,
			}
		return data
	
	def getDictForClient( self, entity ):
		"""
		获取物品数据同步到客户端的格式
		"""
		return { 
			"id":self.id, 
			"uid":self.uid,
			"amount": self.amount , 
			"bindType":self.bindType,
			"itemOrder":self.order, 
			"itemEndTime":self.itemEndTime,
			"dynamicData": self.getDynamicDataForClient( entity )
		}
		
	def getItemDict(self):
		"""
		获取物品配置
		"""
		return g_itemFactory.getItemData(self.id)
		
	def getItemDir( self, attrStr, default = "" ):
		"""获取物品的静态属性"""
		itemData = g_itemFactory.getItemData(self.id)
		if itemData:
			try:
				return itemData[attrStr]
			except:
				return default
		return default
		
	def setOrder( self, order ):
		self.order = order

	def canStack(self, amount = 1):
		"""
		可以叠加amount个物品
		"""
		KBEDebug.DEBUG_MSG("amount.type = %s,amount = %s"%( type(amount), amount ))
		if self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_STACK:
			return self.overlyingMax >= self.amount + int(amount)
		return False

	def isQuestItem(self):
		"""
		是否为任务物品, 放在任务背包中的物品
		"""
		return self.getType() == ItemTypeEnum.ITEM_TYPE_QUEST

	def isSparItem(self):
		"""
		是否是晶石，放在晶石背包中的物品
		"""
		return self.getType() == ItemTypeEnum.ITEM_TYPE_SPAR

	def isCommonItem(self):
		"""
		放在普通背包中的物品
		"""
		return not self.getType() in [ItemTypeEnum.ITEM_TYPE_SPAR,ItemTypeEnum.ITEM_TYPE_QUEST,ItemTypeEnum.ITEM_TYPE_COPY]

	def isSpaceCopyItem( self ):
		"""
		是否为副本专用物品,放在副本背包中
		"""
		return self.getType() == ItemTypeEnum.ITEM_TYPE_COPY
		
	def getKitBagType(self):
		"""
		获取放入背包的类型
		"""
		type = self.getType()
		if(type == ItemTypeEnum.ITEM_TYPE_QUEST):	return ItemTypeEnum.BAG_QUEST  			 # 该编号的物品只能放入任务背包
		elif(type == ItemTypeEnum.ITEM_TYPE_SPAR):	return ItemTypeEnum.BAG_SPAR		 # 该编号的物品只能放入晶核背包
		elif(type == ItemTypeEnum.ITEM_TYPE_COPY):	return ItemTypeEnum.BAG_SPACE_COPY   # 该编号的物品只能放入副本背包
		elif(type  == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ1):	return ItemTypeEnum.BAG_SPACE_COPY_YXLM1
		elif(type  == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ2):	return ItemTypeEnum.BAG_SPACE_COPY_YXLM2
		elif(type  == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ3):	return ItemTypeEnum.BAG_SPACE_COPY_YXLM3
		elif(type  == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ4):	return ItemTypeEnum.BAG_SPACE_COPY_YXLM4
		else:	return ItemTypeEnum.BAG_COMMON
		
	def getAmount( self ):
		"""
		获取物品个数（计次和充能，物品个数为1）
		"""
		if self.overlyingType in [ csdefine.ITEM_OVERLYING_TYPE_NONE, csdefine.ITEM_OVERLYING_TYPE_STACK]:
			return self.amount
		else:
			return 1
			
	def getMaxAmount( self ):
		"""获取最大数量"""
		return max( self.overlyingMax, 1 )

	def isCanSell(self):
		"""
		能否出售
		"""
		return self.getItemDir("CanSell", True)

	def isCanDestory(self):
		"""
		能否销毁
		"""
		return self.getItemDir("CanDestroy", True)

	def isSameType(self, type):
		"""
		判断是不是和自己类型一致的道具
		"""
		return self.getType() == type

	def getMaxTakeAmount(self):
		"""
		获取最大可携带数量
		"""
		return self.getItemDir("MaxTakeAmount",-1)

	def hasLimitTaskAmount(self):
		"""
		是否有携带数量
		"""
		return self.getItemDir("MaxTakeAmount",-1) != csdefine.MAX_TAKEITEM_AMOUNT

	def setOwner(self, player):
		"""
		设置拥有者DBID
		"""
		self.ownerID = player.playerDBID

	def cancelBind(self):
		"""
		取消绑定
		"""
		self.bindType = ItemTypeEnum.BIND_NONT_STATE

	def isEquip(self):
		"""
		判断是否是装备
		"""
		return False

	def isTempEquip(self):
		"""
		判断是否是临时装备
		"""
		return False
 	
	def isFacade(self):
		"""
		判断是否是外观道具
		"""
		return False

	def isWhite(self):
		"""
		判断是不是白装
		"""
		return self.getQuality() == ItemTypeEnum.QUALITY_WHITE

	def isBlue(self):
		"""
		判断是不是蓝色
		"""
		return self.getQuality() == ItemTypeEnum.QUALITY_BLUE

	def isGold(self):
		"""
		判断是不是黄装
		"""
		return self.getQuality() == ItemTypeEnum.QUALITY_GOLD

	def isPink(self):
		"""
		判断是不是粉装
		"""
		return self.getQuality() == ItemTypeEnum.QUALITY_PINK

	def isGreen(self):
		"""
		判断是不是绿色品质
		"""
		return self.getQuality() >= ItemTypeEnum.QUALITY_GREEN

	def isGreenDi(self):
		"""
		判断是不是地阶绿品质
		"""
		return self.getQuality() == ItemTypeEnum.QUALITY_GREEN

	def isGreenTian(self):
		"""
		判断是不是天阶绿品质
		"""
		return self.getQuality() == ItemTypeEnum.QUALITY_GREEN_TIAN

	def isGreenSheng(self):
		"""
		判断是不是圣阶绿品质
		"""
		return self.getQuality() == ItemTypeEnum.QUALITY_GREEN_SHENG

	def isBinded(self):
		"""
		判断是否绑定
		"""
		return self.bindType == ItemTypeEnum.BINDED_STATE

	def setBindType(self, owner, bindtype = ItemTypeEnum.BINDED_STATE):
		"""
		设置绑定
		"""
		if self.bindType != bindtype:
			self.bindType = bindtype
			#通知客户端更新
			if owner:
				owner.updateOneDataToClient("bindType", self.bindType, self)

	def setAmount(self, owner, amount):
		"""
		设置数量
		"""
		if amount >= 0 and amount <= self.overlyingMax:
			if amount == self.amount:	return
			self.amount = amount
			if owner:
				owner.updateOneDataToClient("amount", self.amount, self)
		else:
			KBEDebug.ERROR_MSG("Item(%d) can not set amount(%d) over max(%d)!"%(self.id,amount,self.overlyingMax))

	def reduce(self, owner, amount):
		"""主要用于消耗次数，充能"""
		# 充能物品,只消耗次数！不销毁
		if self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_EMPOWER:
			self.setAmount( owner, self.amount - amount )
		# 次数物品，使用完！就销毁
		elif self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_TIME:
			if self.overlyingMax == -1:return		# 使用无限次数
			if self.amount > 1:
				self.setAmount( owner, self.amount - 1 )
			else:
				owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)
		# 无叠加物品，不消耗
		elif self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_NONE:
			return
		else:
			# 使用次数的物品，用完就销毁
			owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)
			return
			
	def getPrice( self ):
		"""获取物品的价格"""
		price = self.getItemDir("Price", 1)
		if self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_STACK:
			return self.amount * price
		return price

	def isType( self, type = ItemTypeEnum.ITEM_TYPE_DEFAULT ):
		""""""
		return self.getItemDir( "Type" ) == type

	def getType( self ):
		"""
		获取物品类型
		"""
		return self.getItemDir( "Type" )

	def getLevel( self ):
		"""
		获取等级
		"""
		return self.getItemDir( "Level", 1 )

	def getLevelLv( self ):
		"""
		获取等级段，10级一个等级段
		"""
		return self.getLevel()/10

	def getQuality( self ):
		"""
		获取品质
		"""
		return self.getItemDir( "Quality", 1 )

	def getUid( self ):
		"""
		获取uid
		"""
		return self.uid
		
	def setLock(self, isLock ):
		"""设置锁定状态"""
		if isLock:
			self.tempData["lock"] = True
		else:
			if "lock" in self.tempData:
				self.tempData.pop( "lock" )
		
	def isLocking( self ):
		"""是否在锁定状态"""
		return self.tempData.get("lock", False)

	def getSortIndex(self):
		"""
		获取物品在背包整理的排序用的序号
		在排序时使用index从大到小
		index的组成9位数
		物品类型	品阶(等级)		品质		堆叠
		xxx			xxx				x			xx
		"""
		typestr = "%03d"%ItemSortByTypeCfg.Datas.get( self.getType(), 0)
		levelstr = "%03d"%self.getLevel()
		qualitystr = "%01d"%self.getQuality()
		stackstr = "%02d"%self.amount
		itemID = "%09d"%self.id

		indexstr = "%s%s%s%s%s"%(typestr, levelstr, qualitystr, stackstr, itemID)
		return int(indexstr)
		
	def getPickUpShortIndex( self ):
		"""
		获取自动拾取的顺序（策划配置）
		"""
		indexstr = "%03d"% ItemSortByTypeCfg.Datas.get( self.getType(), 0)
		qualitystr = "%01d"%self.getQuality()
		
		return int("%s%s"%(indexstr,qualitystr))

	def getClientTipDynamicProperty( self ):
		"""获取客户端显示的动态数据"""
		return {}

	def getItemEndTime(self):
		"""
		获得限时属性
		"""
		return self.itemEndTime

	def setItemEndTime(self, owner, endTime):
		"""
		修改限时属性
		"""
		self.itemEndTime = endTime
		if owner:
			owner.updateOneDataToClient("itemEndTime", self.itemEndTime, self)

	def setLimitTimeData(self):
		"""
		设置限时属性
		"""
		limitTimeData = self.getItemDir("LimitTime")
		endTime = 0
		limitTimeDataList = limitTimeData.split("|")
		if len(limitTimeDataList) < 2:
			KBEDebug.ERROR_MSG("itemID:%s LimitTime config is err!!!!"%self.id)
			return	
		if int(limitTimeDataList[0]) == 1:
			timeList = limitTimeDataList[1].split(":")
			if len(timeList) != 3:
				KBEDebug.ERROR_MSG("itemID:%s LimitTime config is err!!!!"%self.id)
				return
			Time = int(timeList[0]) * 60 * 60 + int(timeList[1]) * 60 + int(timeList[2])
			endTime = Functions.getTime(Time)
		elif int(limitTimeDataList[0]) == 2:
			tempList = []
			dateList = limitTimeDataList[1].split("/")
			if len(dateList) != 4:
				KBEDebug.ERROR_MSG("itemID:%s LimitTime config is err!!!!"%self.id)
				return
			tempList = dateList[:-1]
			timeList = dateList[3].split(":")
			if len(timeList) != 3:
				KBEDebug.ERROR_MSG("itemID:%s LimitTime config is err!!!!"%self.id)
				return
			tempList.extend(timeList)
			intList = [int(i) for i in tempList]
			endTime = time.mktime((datetime.datetime(intList[0],intList[1],intList[2],intList[3],intList[4],intList[5])).timetuple())
			endTime = int( endTime * csconst.TIME_ENLARGE_MULTIPLE )
		elif int(limitTimeDataList[0]) == 3:
			timeList = limitTimeDataList[1].split(":")
			if len(timeList) != 3:
				KBEDebug.ERROR_MSG("itemID:%s LimitTime config is err!!!!"%self.id)
				return
			y = datetime.datetime.now().year
			m = datetime.datetime.now().month
			d = datetime.datetime.now().day
			intList = [int(i) for i in timeList]
			endTime = time.mktime((datetime.datetime(y, m, d, intList[0],intList[1],intList[2])).timetuple())
			endTime = int( endTime * csconst.TIME_ENLARGE_MULTIPLE )
			
		self.itemEndTime = str(endTime)

	def isLimitTimeItem(self):
		"""
		是否是限时物品
		"""
		return self.getItemDir("LimitTime") != ""

	def isLimitTimeDestory(self):
		"""
		限时道具过期是否自动销毁
		"""
		string = self.getItemDir("LimitTime")
		if string:
			strList = string.split("|")
			if len(strList) < 3:
				return True
			return bool(int(strList[2]))
		return False

	def isItemOverTime(self):
		"""
		限时道具是否过期
		"""
		if self.getItemDir("LimitTime") == "":
			return False
		if self.itemEndTime == "":
			return False
		return Functions.getTime(0.1) >= int(self.itemEndTime)

	def getDynamicDataForClient(self, entity ):
		return Functions.toJsonString( {} )
		
	def hasRandomAttrAtInit(self):
		"""
		创建时候有随机属性
		"""
		return False