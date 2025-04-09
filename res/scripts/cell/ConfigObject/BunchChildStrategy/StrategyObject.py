# -*- coding: utf-8 -*-
"""
一个策略实例
"""

from ConfigObject.BunchChildStrategy.StrategyCondition import *
from ConfigObject.BunchChildStrategy.StrategyResult import *

class StrategyObject:
	def __init__( self ):
		self._conditions = []
		self._result = None
	
	def init( self, datas ):
		for conDict in datas["conditions"]:
			conObj = eval(conDict["script"])()
			conObj.init( conDict )
			self._conditions.append( conObj )
		
		resultDict = datas["result"]
		resultObj = eval(resultDict["script"])()
		resultObj.init( resultDict )
		self._result = resultObj
	
	def checkConditions( self, bunchObj, spaceEntity, playerEntity ):
		"""
		"""
		for con in self._conditions:
			if not con.check( bunchObj, spaceEntity, playerEntity ):
				return False
		return True
	
	def getSpace( self, bunchObj, spaceEntity, playerEntity ):
		"""
		"""
		return self._result.getResult( bunchObj, spaceEntity, playerEntity )