# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class AllBHZBTongIntegralData( object ):
	"""
	帮会积分
	"""
	def __init__( self, tongDBID = 0,tongName = "",tongLevel = 0, camp = 0, startTimes = "",integral = 0, totalIntegral = 0 ):
		"""
		"""
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.tongLevel = tongLevel
		self.integral = integral
		self.camp = camp
		self.totalIntegral = totalIntegral
		self.startTimes = startTimes

	def initData( self, dict ):
		"""
		"""
		self.tongDBID = dict["tongDBID"]
		self.tongName = dict["tongName"]
		self.tongLevel = dict["tongLevel"]
		self.integral = dict["integral"]
		self.camp = dict["camp"]
		self.totalIntegral = dict["totalIntegral"]
		self.startTimes = dict["startTimes"]

	def getTongDBID( self ):
		"""
		"""
		return self.tongDBID

	def getTongName( self ):
		return self.tongName

	def getCamp( self ):
		return self.camp

	def getStartTimes( self ):
		return self.startTimes

	def setBHZBTongTotalIntegral( self, totalIntegral ):
		"""
		"""
		self.totalIntegral = totalIntegral

	def getBHZBTongTotalIntegral( self ):
		return self.totalIntegral

	def getDictFromObj( self, obj ):
		dict = {
			"tongDBID" 	: obj.tongDBID,
			"tongName"	: obj.tongName,
			"tongLevel" : obj.tongLevel,
			"integral":obj.integral,
			"camp":obj.camp,
			"totalIntegral":obj.totalIntegral,
			"startTimes":obj.startTimes,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, AllBHZBTongIntegralData )

class ALLBHZBTongIntegralRankMgr( dict ):
	"""
	一场帮会争霸所有帮会积分排行数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			if m.startTimes not in self:
				self[ m.startTimes ] = {}
			self[m.startTimes][m.tongDBID] = m

	def addALLBHZBTongIntegralRankData( self, tongDBID, tongName, tongLevel,camp, startTimes, integral ):
		"""
		增加帮会积分排行数据
		"""
		if startTimes not in self:
			self[startTimes] = {}

		self[startTimes][tongDBID] = AllBHZBTongIntegralData( tongDBID, tongName, tongLevel,camp, startTimes, integral )

	def getCurrentBHZBTongIntegralData( self, startTimes, tongDBID ):
		"""
		"""
		if startTimes not in self:
			return 0
		if tongDBID not in self[startTimes]:
			return 0
		return self[startTimes][tongDBID].integral

	def setBHZBTongTotalIntegral( self, startTimes, tongDBID, totalIntegral ):
		"""
		"""
		if startTimes in self and tongDBID in self[startTimes]:
			self[startTimes][tongDBID].setBHZBTongTotalIntegral( totalIntegral )

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for startTimes, mObj in obj.items():
			tempDict["datas"].extend( mObj.values())
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = ALLBHZBTongIntegralRankMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, ALLBHZBTongIntegralRankMgr )

g_AllBHZBTongIntegralRankMgr = ALLBHZBTongIntegralRankMgr()
g_AllBHZBTongIntegralData = AllBHZBTongIntegralData()