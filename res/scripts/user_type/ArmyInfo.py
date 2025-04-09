# -*- coding: utf-8 -*-

import KBEDebug

class ArmyInfo( object ):
	"""
	玩家部队数据
	"""
	def __init__( self ):
		"""
		"""
		self.id = 0
		self.controlArmyID = 0					# 部队 被 亲卫领兵（玩家领兵，暂时不设置）
		self.firstGuardScriptID = ""
		self.secondGuardScriptID = ""
		self.soldierScriptID = ""
		self.soldierIDs = []
		
	def canDispatch(self):
		"""部队 能否被派遣"""
		return self.controlArmyID == 0
		
	def setComtrolArmy( self, id ):
		"""pai"""
		self.controlArmyID = id

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		tempDict = {}
		tempDict["id"] = obj.id
		tempDict["controlArmyID"] = obj.controlArmyID
		tempDict["firstGuardScriptID"] = obj.firstGuardScriptID
		tempDict["secondGuardScriptID"] = obj.secondGuardScriptID
		tempDict["soldierScriptID"] = obj.soldierScriptID
		tempDict["soldierIDs"] = []
		for soldierID in obj.soldierIDs:
			tempDict["soldierIDs"].append(soldierID)
		return tempDict

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = ArmyInfo()
		obj.id = dict["id"]
		obj.controlArmyID = dict["controlArmyID"]
		obj.firstGuardScriptID = dict["firstGuardScriptID"]
		obj.secondGuardScriptID = dict["secondGuardScriptID"]
		obj.soldierScriptID = dict["soldierScriptID"]
		for soldierID in dict["soldierIDs"]:
			obj.soldierIDs.append(soldierID)
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, ArmyInfo )

class RoleArmyInfoMgr( dict ):
	"""
	玩家兵营管理器
	"""
	def __init__( self ):
		pass
	
	def initData( self, dict ):
		for m  in dict[ "datas" ]:
			self[ m.id ] = m

	def getDictFromObj( self, obj ):
		tempDict = {}
		tempDict[ "datas" ] = []
		
		for mObj in obj.values():
			tempDict[ "datas" ].append( mObj )
			
		return tempDict
	
	def createObjFromDict( self, dict ):
		obj = RoleArmyInfoMgr()
		obj.initData( dict )
		return obj
		
	def isSameType( self, obj ):
		return isinstance( obj, RoleArmyInfoMgr )


# 自定义类型实现实例
instance = ArmyInfo()
g_RoleArmyInfoMgr = RoleArmyInfoMgr()