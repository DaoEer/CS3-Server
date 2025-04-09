# -*- coding: utf-8 -*-

import KBEDebug

class BHZBMSignMemberInfo( object ):
	"""
	帮会争霸报名数据
	"""
	def __init__( self ):
		"""
		"""
		self.signID = 0
		self.groupID = 0
		self.captainDBID = ""
		self.memberDBIDs = []
		self.isActive = False
		self.pointIndex = 0

	def getAllMemberDBIDs( self ):
		"""
		获得所有参赛的DBID
		"""
		totalMem = []
		totalMem.append( self.captainDBID )
		totalMem.extend( self.memberDBIDs )
		return totalMem

	def getGroupID( self ):
		return self.groupID

	def setIsActive( self, isActive, pointIndex ):
		self.isActive = isActive
		self.pointIndex = pointIndex

	def getIsActive( self ):
		return self.isActive

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		tempDict = {}
		tempDict["signID"] = obj.signID
		tempDict["groupID"] = obj.groupID
		tempDict["captainDBID"] = obj.captainDBID
		tempDict["memberDBIDs"] = []
		for memberDBID in obj.memberDBIDs:
			tempDict["memberDBIDs"].append(memberDBID)
		tempDict["isActive"] = obj.isActive
		tempDict["pointIndex"] = obj.pointIndex
		return tempDict

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = BHZBMSignMemberInfo()
		obj.signID = dict["signID"]
		obj.groupID = dict["groupID"]
		obj.captainDBID = dict["captainDBID"]
		for memberDBID in dict["memberDBIDs"]:
			obj.memberDBIDs.append(memberDBID)
		obj.isActive = dict["isActive"]
		obj.pointIndex = dict["pointIndex"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, BHZBMSignMemberInfo )

class BHZBMSignMemberInfoMgr( dict ):
	"""
	帮会争霸报名管理器数据
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.groupID ] = m

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		
		for mObj in obj.values():
			tempDict[ "datas" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = BHZBMSignMemberInfoMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, BHZBMSignMemberInfoMgr )

# 自定义类型实现实例
instance = BHZBMSignMemberInfo()
g_BHZBMSignMemberInfoMgr = BHZBMSignMemberInfoMgr()