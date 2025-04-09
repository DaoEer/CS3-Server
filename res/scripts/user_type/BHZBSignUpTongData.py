# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine

class BHZBSignUpTongData( object ):
	"""
	帮会争霸帮会数据
	"""
	def __init__( self, tongDBID = 0,tongName = "",tongLevel = 0, activity = 0, tongMemNum = 0, camp = 0 ):
		"""
		"""
		self.tongDBID = tongDBID
		self.tongName = tongName
		self.tongLevel = tongLevel
		self.activity = activity
		self.tongMemNum = tongMemNum
		self.camp = camp

	def initData( self, dict ):
		"""
		"""
		self.tongDBID = dict["tongDBID"]
		self.tongName = dict["tongName"]
		self.tongLevel = dict["tongLevel"]
		self.activity = dict["activity"]
		self.tongMemNum = dict["tongMemNum"]
		self.camp = dict["camp"]

	def setTongActivity( self, activity ):
		"""
		"""
		self.activity = activity

	def setTongMemNum( self, number ):
		"""
		"""
		self.tongMemNum = number

	def getDictFromObj( self, obj ):
		dict = {
			"tongDBID" 	: obj.tongDBID,
			"tongName"	: obj.tongName,
			"tongLevel" : obj.tongLevel,
			"activity" : obj.activity,
			"tongMemNum":obj.tongMemNum,
			"camp":obj.camp,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBSignUpTongData )

class BHZBSignUpTongDataMgr( dict ):
	"""
	帮会争霸帮会报名数据管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.tongDBID ] = m

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			tempDict["datas"].append( mObj )
		return tempDict

	def addSignUpTongData( self, tongDBID, tongName, tongLevel, activity, tongMemNum,camp ):
		"""
		"""
		if tongDBID in self:
			del self[tongDBID]

		self[tongDBID] = BHZBSignUpTongData( tongDBID, tongName, tongLevel, activity, tongMemNum,camp )

	def removeSignUpTongData( self, tongDBID ):
		"""
		"""
		if tongDBID in self:
			del self[tongDBID]

	def setTongActivity( self, tongDBID, activityValue ):
		"""
		设置帮会活跃度
		"""
		if tongDBID in self:
			self[tongDBID].setTongActivity( activityValue )

	def setTongMemNum( self, tongDBID, tongMemNum ):
		"""
		设置帮会成员数
		"""
		if tongDBID in self:
			self[tongDBID].setTongMemNum( tongMemNum )
	
	def createObjFromDict( self, dict ):
		obj = BHZBSignUpTongDataMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBSignUpTongDataMgr )

g_BHZBSignUpTongDataMgr = BHZBSignUpTongDataMgr()
g_BHZBSignUpTongData = BHZBSignUpTongData()