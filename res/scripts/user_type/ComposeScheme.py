# -*- coding: utf-8 -*-

import KBEDebug
import csdefine
import random
import ItemFactory
import time
import csstatus
from ItemSystemExp import g_ToolCompose

class ComposeScheme( dict ):
	def __init__(self, playerDBID, name, composeType, itemID, isBind, endTime, successRate):
		self.playerMB = None
		self.name = name
		self.playerDBID = playerDBID				# 打造玩家的DBID
		self.composeType = composeType				# 打造类型（工具、绿装、乾坤鼎）
		self.itemID = itemID						# 打造物品ID
		self.isBind = isBind						# 打造物品是否绑定
		self.endTime = endTime						# 打造结束时间
		self.successRate = successRate				# 打造成功率(取值范围0~1)
	
	def doCompose( self ):
		"""开始打造"""
		itemInst = None
		rate = random.random()
		if self.successRate >= rate:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(self.itemID, 1, {"bindType":self.isBind})
			return True, itemInst
		# 绿装打造失败会获得半成品
		elif self.composeType == csdefine.COMPOSE_TOOL_GREEN_EQUIP:
			partEquipID = g_ToolCompose.getGreenComposeEquipPart(self.itemID)
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(partEquipID, 1, {"bindType":self.isBind})
				
		return False, itemInst
		
	def reduceComposeTime(self, _time):
		"""祈福减少时间"""
		if self.composeType == csdefine.COMPOSE_TOOL_GREEN_EQUIP:
			self.endTime = max(time.time()+2, self.endTime - _time)
		else:
			KBEDebug.ERROR_MSG("Must be err!!only green equip can pray reduce time")
	
	@classmethod
	def getDictFromObj(self, obj):
		""""""
		data = {}
		data["playerDBID"] = obj.playerDBID
		data["name"] = obj.name
		data["composeType"] = obj.composeType
		data["itemID"] = obj.itemID
		data["isBind"] = obj.isBind
		data["endTime"] = obj.endTime
		data["successRate"] = obj.successRate
		return data
	
	@classmethod
	def createObjFromDict(self, dict):
		return ComposeScheme(dict["playerDBID"], dict["name"], dict["composeType"], dict["itemID"], dict["isBind"], dict["endTime"],dict["successRate"])
	
	@classmethod
	def isSameType(self, obj):
		return isinstance(obj, ComposeScheme)
		
class ComposeCraftsman( dict ):
	"""{playerDBID:{composeType:scheme}}"""
	def __init__(self):
		pass
		
	def onPlayerOnLine( self, playerDBID, playerBase ):
		"""玩家上线"""
		if playerDBID in self:
			for type, scheme in self[playerDBID].items():
				scheme.playerMB = playerBase
		
	def onPlayerOffLine( self, playerDBID ):
		"""玩家销毁"""
		if playerDBID in self:
			for type, scheme in self[playerDBID].items():
				scheme.playerMB = None
		
	def getScheme(self, playerDBID, composeType):
		"""获取打造方案"""
		if playerDBID in self:
			return self[playerDBID].get(composeType)
		return None
		
	def addScheme(self, scheme):
		"""添加打造方案"""
		if not scheme.playerDBID in self:
			self[scheme.playerDBID] = {}
		self[scheme.playerDBID][scheme.composeType] = scheme
		
	def removeScheme(self, scheme):
		"""移除打造方案"""
		if scheme.playerDBID in self:
			if scheme.composeType in self[scheme.playerDBID]:
				self[scheme.playerDBID].pop(scheme.composeType)
			if not self[scheme.playerDBID]:
				self.pop(scheme.playerDBID)
		
	def getMinTimeScheme( self ):
		"""获取最短时间的打造方案"""
		minScheme = None
		for schemeDict in self.values():
			for scheme in schemeDict.values():
				if minScheme is None:
					minScheme = scheme
				if minScheme.endTime > scheme.endTime:
					minScheme = scheme
		return minScheme
		
	@classmethod
	def getDictFromObj(self, obj):
		""""""
		data = {}
		temp = []
		for playerDBID, subObj in obj.items():
			for composeType, scheme in subObj.items():
				temp.append( scheme )
		data["datas"] = temp
		return data
	
	@classmethod
	def createObjFromDict(self, dict):
		man = ComposeCraftsman()
		for data in dict["datas"]:
			if not data.playerDBID in man:
				man[data.playerDBID] = {}
			man[data.playerDBID].update( {data.composeType : data} )
		return man
		
	@classmethod
	def isSameType(self, obj):
		return isinstance(obj, ComposeCraftsman)


instance = ComposeScheme(0,"",0,0,0,0,0)
manInst = ComposeCraftsman()
