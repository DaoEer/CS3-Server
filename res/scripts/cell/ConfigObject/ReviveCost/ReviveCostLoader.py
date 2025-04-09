# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
from Singleton import Singleton
import imp
import RoleReviveCostConfig

class ReviveCostLoader( Singleton ):
	"""
	复活消耗加载类
	"""
	def __init__( self ):
		self.reviveCostItemDict = {}  #复活消耗物品字典
		self.reviveCostMoneyDict = {} #复活消耗金钱字典
		self.reviveCostYXLMDict = {} #英雄联盟复活消耗字典
		self.reviveCostGCZDict = {}	# 攻城战复活消耗字典

	def init( self ):
		"""
		读取配置
		"""
		self.reviveCostItemDict = RoleReviveCostConfig.datas.get(csdefine.REVIVE_ON_ORIGIN_BY_COST_ITEM,{})
		self.reviveCostMoneyDict = RoleReviveCostConfig.datas.get( csdefine.REVIVE_ON_ORIGIN_BY_COST_MONEY,{} )
		self.reviveCostYXLMDict = RoleReviveCostConfig.datas.get( csdefine.REVIVE_ON_YXLM,{} )
		self.reviveCostGCZDict = RoleReviveCostConfig.datas.get( csdefine.REVIVE_ON_GCZ,{} )

	def reloadConfig( self ):
		"""
		"""
		self.reviveCostItemDict = {}
		self.reviveCostMoneyDict = {}
		self.reviveCostYXLMDict = {}
		self.reviveCostGCZDict = {}
		imp.reload(RoleReviveCostConfig)
		self.init()

	def getCostItemData( self, number ):
		"""
		规则：如果number大于最大上限  返回最大上限的数据
		"""
		if not self.reviveCostItemDict:
			return None
		numberList = list(self.reviveCostItemDict.keys())
		if number < max(numberList):
			return self.reviveCostItemDict.get(number,None)
		return self.reviveCostItemDict.get( max(numberList),None )

	def getCostMoneyData( self, number ):
		"""
		规则：如果number大于最大上限  返回最大上限的数据
		"""
		if not self.reviveCostMoneyDict:
			return None
		numberList = list( self.reviveCostMoneyDict.keys() )
		if number < max(numberList):
			return self.reviveCostMoneyDict.get(number,None)
		return self.reviveCostMoneyDict.get( max(numberList),None )

	def getCostYXLMData( self, number ):
		"""
		规则：如果number大于最大上限  返回最大上限的数据
		"""
		if not self.reviveCostYXLMDict:
			return None
		numberList = list( self.reviveCostYXLMDict.keys() )
		if number < max(numberList):
			return self.reviveCostYXLMDict.get(number,None)
		return self.reviveCostYXLMDict.get( max(numberList),None )

	def getCostGCZData( self, number ):
		"""
		如果number 大于最大上限，返回空值
		"""
		if not self.reviveCostGCZDict:
			return None
		numberList = list( self.reviveCostGCZDict.keys() )
		if number <= max(numberList):
			return self.reviveCostGCZDict.get( number, None )
		return None
	
g_reviveCostLoader = ReviveCostLoader()