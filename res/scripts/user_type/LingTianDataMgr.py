# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine
import Math

class LingTianData( ):
	"""
	灵田数据
	"""
	def __init__( self, scriptID = "", seedNum = 0, growthStage = 0, growTime = 0 ):
		self.scriptID = scriptID
		self.seedNum = seedNum
		self.growthStage = growthStage
		self.growTime = growTime
	
	def initData( self, dict ):
		self.scriptID = dict[ "scriptID" ]
		self.seedNum = dict[ "seedNum" ]
		self.growthStage = dict[ "growthStage" ]
		self.growTime = dict["growTime"]

	def getDictFromObj( self, obj ):
		dict = {
			"scriptID"		: obj.scriptID,
			"seedNum"		: obj.seedNum,
			"growthStage"	: obj.growthStage,
			"growTime"		: obj.growTime,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, LingTianData )

class LingTianDataMgr( dict ):
	"""
	灵田数据管理器
	"""
	def __init__( self ):
		pass
	
	def addLingTianData( self, belongDBID, scriptID, seedNum, growthStage, growTime ):
		"""
		增加灵田数据
		"""
		if belongDBID not in self:
			self[belongDBID] = {}
		self[belongDBID].update( { scriptID : LingTianData( scriptID, seedNum, growthStage, growTime )} )
		
	def removeLingTianData( self, belongDBID, scriptID ):
		"""收获，移除灵田数据"""
		if belongDBID in self and scriptID in self[belongDBID]:
			self[belongDBID].pop( scriptID )
			if len( self[belongDBID] ) == 0:
				self.pop( belongDBID )

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for bdid, playerDatas in obj.items():
			playerDict = {}
			playerDict["belongDBID"] = bdid
			playerDict["LTDatas"] = []
		
			for obj in playerDatas.values():
				playerDict[ "LTDatas" ].append( obj )
			tempDict["datas"].append(playerDict)
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = LingTianDataMgr()
		for m  in dict[ "datas" ]:
			obj[ m["belongDBID"] ] = {}
			for data in m["LTDatas"]:
				obj[ m["belongDBID"] ].update( {data.scriptID : data} )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, LingTianDataMgr )

g_LingTianDataMgr = LingTianDataMgr()
g_LingTianData = LingTianData()
