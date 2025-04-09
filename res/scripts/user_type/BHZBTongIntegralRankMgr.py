# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class BHZBTongIntegralData( object ):
	"""
	帮会争霸帮会积分数据
	"""
	def __init__( self, tongDBID = 0,tongName = "",tongLevel = 0, camp = 0, occupyPointAmount = 0, integral = 0 ):
		"""
		"""
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.tongLevel = tongLevel
		self.occupyPointAmount = occupyPointAmount
		self.integral = integral
		self.camp = camp

	def initData( self, dict ):
		"""
		"""
		self.tongDBID = dict["tongDBID"]
		self.tongName = dict["tongName"]
		self.tongLevel = dict["tongLevel"]
		self.occupyPointAmount = dict["occupyPointAmount"]
		self.integral = dict["integral"]
		self.camp = dict["camp"]

	def addTongOccupyPointAmount( self ):
		"""
		"""
		self.occupyPointAmount += 1

	def reduceTongOccupyPoint( self ):
		"""
		"""
		self.occupyPointAmount -= 1

	def addTongIntegral( self, integral ):
		"""
		"""
		self.integral += integral

	def getTongIntegral( self ):
		return self.integral

	def getTongOccupyPointAmount( self ):
		return self.occupyPointAmount

	def getDictFromObj( self, obj ):
		dict = {
			"tongDBID" 	: obj.tongDBID,
			"tongName"	: obj.tongName,
			"tongLevel" : obj.tongLevel,
			"occupyPointAmount" : obj.occupyPointAmount,
			"integral":obj.integral,
			"camp":obj.camp,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongIntegralData )

class BHZBTongIntegralRankMgr( dict ):
	"""
	帮会争霸积分排行数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def addTongIntegralRankData( self, tongDBID, tongName, tongLevel,camp ):
		"""
		增加帮会积分排行数据
		"""
		if tongDBID in self:
			return
		self[tongDBID] = BHZBTongIntegralData( tongDBID, tongName, tongLevel,camp )

	def removeTongIntegralRankData( self, tongDBID ):
		"""
		移除帮会积分排行数据
		"""
		if tongDBID in self:
			del self[tongDBID]

	def addTongOccupyPointAmount( self, tongDBID ):
		"""
		增加占领的据点数
		"""
		if tongDBID in self:
			self[tongDBID].addTongOccupyPointAmount()

	def reduceTongOccupyPoint( self, tongDBID ):
		"""
		减少占领据点数
		"""
		if tongDBID in self:
			self[tongDBID].reduceTongOccupyPoint()

	def addTongIntegral( self, tongDBID,integral ):
		"""
		增加积分数据
		"""
		if tongDBID in self:
			self[tongDBID].addTongIntegral( integral )

	def getTongIntegral( self, tongDBID ):
		"""
		获得帮会积分
		"""
		if tongDBID not in self:
			return 0
		return self[tongDBID].getTongIntegral()

	def getTongOccupyPointAmount( self, tongDBID ):
		"""
		获得帮会占领的据点数
		"""
		if tongDBID not in self:
			return 0
		return self[tongDBID].getTongOccupyPointAmount()

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			tempDict["datas"].append( mObj )
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBTongIntegralRankMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBTongIntegralRankMgr )

g_BHZBTongIntegralRankMgr = BHZBTongIntegralRankMgr()
g_BHZBTongIntegralData = BHZBTongIntegralData()