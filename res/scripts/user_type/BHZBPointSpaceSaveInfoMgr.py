# -*- coding: utf-8 -*-

import KBEDebug
import Math

class BHZBPointSpaceSaveInfo( object ):
	"""
	帮会争霸据点PVP 保存数据
	"""
	def __init__( self, pointIndex = 0, scriptID = "", position = Math.Vector3(0,0,0), direction = Math.Vector3(0,0,0) ):
		"""
		"""
		self.pointIndex = pointIndex
		self.scriptID = scriptID
		self.position = position
		self.direction = direction

	def initData( self, dict ):
		self.pointIndex = dict[ "pointIndex" ]
		self.scriptID = dict["scriptID"]
		self.position = dict["position"]
		self.direction = dict["direction"]

	def getDictFromObj( self, obj ):
		dict = {
			"pointIndex" 	: obj.pointIndex,
			"scriptID"	: obj.scriptID,
			"position" : obj.position,
			"direction" : obj.direction,
		}
		return dict
	
	def createObjFromDict( self, dict ):
		obj = self.__class__()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBPointSpaceSaveInfo )

class BHZBPointSpaceSaveInfoMgr( dict ):
	"""
	帮会争霸据点PVP 保存数据
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m in dict[ "datas" ]:
			if m.pointIndex not in self:
				self[m.pointIndex] = []
			self[m.pointIndex].append( m )

	def updataBHZBPointSpaceSaveInfo( self, pointIndex, spaceSaveInfos ):
		"""
		"""
		if pointIndex in self:
			del self[pointIndex]
		self[pointIndex] = spaceSaveInfos

	def getBHZBPointSpaceSaveInfo( self, pointIndex ):
		"""
		"""
		if pointIndex in self:
			return self[pointIndex]
		return []

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		for mObj in list(obj.values()):
			tempDict["datas"].extend( mObj )
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBPointSpaceSaveInfoMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBPointSpaceSaveInfoMgr )

g_BHZBPointSpaceSaveInfoMgr = BHZBPointSpaceSaveInfoMgr()
g_BHZBPointSpaceSaveInfo = BHZBPointSpaceSaveInfo()
