# -*- coding: utf-8 -*-

import KBEDebug
import csdefine
import ConfigObject.Item.ItemBase as ItemBase
import csstatus
import Functions
import csconst
import datetime
import time
import QuestEventDefine

class ItemUse(ItemBase.ItemBase):
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
		if srcData.get("UseAmount",""):	#使用限量 useAmount[0] 代表时间  useAmount[1] 代表使用限量
			self.useAmount = [int(item) for item in srcData.get("UseAmount").split("|")]
		else:
			self.useAmount = ""
		self.skillID = srcData.get("SkillID", 0)

	def getDictFromObj(self):
		"""
		转化为字典打包传输或保存到数据库
		"""
		return ItemBase.ItemBase.getDictFromObj(self)

	def checkReqTargetList(self, owner):
		"""
		检测能否对当前目标使用
		"""
		return True

	def checkReqLevel(self, owner):
		"""
		检查装备等级
		"""
		return owner.level >= self.getItemDir("ReqLevel", 1)

	def checkReqJingJieLevel(self, owner):
		"""
		检查物品境界等级
		"""
		return owner.jingjieLevel >= self.getItemDir("ReqJingJieLevel", 1)

	def checkUseAmountDay( self, owner, createTime, amount):
		"""
		检查每天使用限量
		"""
		if datetime.date.fromtimestamp(createTime).year == datetime.date.today().year:
			if datetime.date.fromtimestamp(createTime).month == datetime.date.today().month:
				if datetime.date.fromtimestamp(createTime).day == datetime.date.today().day:
					if amount <= 0:
						return False
					else: return True
		newRefreshTime = time.mktime(datetime.date.today().timetuple())
		owner.updateItemUseAmount(self.id,self.useAmount[1],newRefreshTime * csconst.TIME_ENLARGE_MULTIPLE)
		return True

	def checkUseAmountWeek( self, owner, createTime, amount ):
		"""
		检查每周使用限量
		"""
		if datetime.date.fromtimestamp(createTime).year == datetime.date.today().year:
			if datetime.date.fromtimestamp(createTime).month == datetime.date.today().month:
				startDay = datetime.date.fromtimestamp(createTime)
				weekDay = startDay.weekday()
				nextWeek = startDay + datetime.timedelta(days = (7-weekDay))
				if time.mktime(nextWeek.timetuple()) > time.time():
					if amount <= 0:
						return False
					else: return True
		newRefreshTime = time.mktime(datetime.date.today().timetuple())
		owner.updateItemUseAmount(self.id,self.useAmount[1],newRefreshTime * csconst.TIME_ENLARGE_MULTIPLE)
		return True

	def checkUseAmountMonth( self,owner,createTime, amount ):
		"""
		检查每月使用限量
		"""
		if datetime.date.fromtimestamp(createTime).year == datetime.date.today().year:
			if datetime.date.fromtimestamp(createTime).month == datetime.date.today().month:
				if amount <= 0:
					return False
				else: return True
		newRefreshTime = time.mktime(datetime.date.today().timetuple())
		owner.updateItemUseAmount(self.id,self.useAmount[1],newRefreshTime * csconst.TIME_ENLARGE_MULTIPLE)
		return True

	def checkUseTime( self, owner ):
		"""
		检查物品使用限量
		remainAmountData[0] 代表刷新时间
		remainAmountData[1] 代表剩余使用限量
		"""
		remainAmountData = owner.getItemUseAmount(self.id)
		if self.useAmount == "" or remainAmountData == None:
			return True
		if self.useAmount[0] == csdefine.ITEM_USE_AMOUNT_FOREVER:
			if remainAmountData[1] > 0:
				return True
			else: return False
		elif self.useAmount[0] == csdefine.ITEM_USE_AMOUNT_DAY:
			return self.checkUseAmountDay( owner, remainAmountData[0] / csconst.TIME_ENLARGE_MULTIPLE, remainAmountData[1] )
		elif self.useAmount[0] == csdefine.ITEM_USE_AMOUNT_WEEK:
			return self.checkUseAmountWeek( owner, remainAmountData[0] / csconst.TIME_ENLARGE_MULTIPLE, remainAmountData[1] )
		elif self.useAmount[0] == csdefine.ITEM_USE_AMOUNT_MONTH:
			return self.checkUseAmountMonth( owner, remainAmountData[0] / csconst.TIME_ENLARGE_MULTIPLE, remainAmountData[1] )

	def checkUseBySpace( self, owner ):
		"""
		检查地图是否可以使用
		"""
		space = owner.getCurrentSpace()
		if space:
			if len( space.getScript().getAllowUseItemTypes() ) and self.getType() not in space.getScript().getAllowUseItemTypes():
				return False

			if len( space.getScript().getForbidUseItemTypes() ) and self.getType() in space.getScript().getForbidUseItemTypes():
				return False

			if len( space.getScript().getAllowUseItemIDs() ) and self.id not in space.getScript().getAllowUseItemIDs():
				return False

			if len( space.getScript().getForbidUseItemIDs() ) and self.id in space.getScript().getForbidUseItemIDs():
				return False
		return True

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		if not self.checkUseBySpace( owner ):
			return csstatus.ITEM_FORBID_BY_SPACE

		if owner.actionForbidSign( csdefine.ACTION_FORBID_USE_ITEM ):
			return csstatus.USE_ITEM_FORBID_BY_STATE
		if not self.checkReqLevel(owner):
			return csstatus.ITEM_USE_LV_LESS_MSG

		if not self.checkReqJingJieLevel(owner):
			return csstatus.ITEM_USE_JJLV_LESS_MSG

		if not self.checkUseTime( owner ):
			return csstatus.ITEM_USE_AMOUNT_LIMIT

		# 物品需求地图判定
		if not self.checkReqSpaceList( owner ):
			return csstatus.ITEM_CANNOT_USED
			
		if self.amount <= 0:
			return csstatus.ITEM_USE_NUMBER_LIMIT

		# 物品过期
		if self.isLimitTimeItem() and self.isItemOverTime():
			return csstatus.ITEM_OVER_TIME

		from ConfigObject.Item.Drug import Drug
		if ( owner.isTeamFollowing() or owner.isNormalFollowing() ) and not isinstance( self, Drug ):	#跟随状态只能使用药和装备
			return csstatus.USE_ITEM_FORBID_BY_STATE
		
		return csstatus.ITEM_USE_GO_ON_MSG

	def use(self, owner, target):
		"""
		使用
		"""
		owner.onUseItem( self )
		return csstatus.ITEM_USE_GO_ON_MSG

	def onUseResult(self, owner, useResult ):
		"""
		使用物品结果
		"""
		# 充能物品,只消耗次数！不销毁
		if self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_EMPOWER:
			self.setAmount( owner, self.amount - 1 )
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
		
	def addUseNumber( self, amount, owner ):
		"""充能"""
		if self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_EMPOWER:
			self.amount = min( self.amount + amount, self.overlyingMax )
			owner.updateOneDataToClient("amount", self.amount, self)
		else:
			KBEDebug.ERROR_MSG("item(id:%d,overlyingType(%d)) can not add use num!"%( self.id, self.overlyingType))

	#------------------------增加道具地图限制使用---------------------------------------------
	def getReqSpaceName( self ):
		"""
		获取物品需求地图列表
		"""
		spaceData = {}
		space = self.getItemDir("ReqSpace")
		if space:
			tempData = space.split(":")
			if len(tempData) == 2:
				spaceData[int(tempData[0])] = tempData[1]
			elif len(tempData) == 1:
				spaceData[0] = tempData[0]
		return spaceData
	
	def checkReqSpaceList( self, owner ):
		"""
		检查可使用地图
		"""
		reqSpaceDict = self.getReqSpaceName()
		if not reqSpaceDict:
			return True
		if list(reqSpaceDict.keys())[0] == 0:
			reqSpaceList = reqSpaceDict[0].split("|")
			return owner.getCurrentSpaceScriptID() in reqSpaceList
		elif list(reqSpaceDict.keys())[0] == 1:
			reqSpaceList = reqSpaceDict[1].split("|")
			return owner.getCurrentSpaceScriptID() not in reqSpaceList