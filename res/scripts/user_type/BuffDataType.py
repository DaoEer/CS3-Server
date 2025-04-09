
# -*- coding: utf-8 -*-
"""
cell部份的QuestAIIDSImpl实现模块.
"""
import KBEngine
import KBEDebug
import Functions
import time


class BuffDataType:
	"""
	实现 buffs 数据创建、还原
	"""
	def __init__( self ):
		self.index = 0
		self.buffID = 0
		self.holdTime = 0
		self.endTime = 0
		self.timerID = 0
		self.casterID = 0
		self.casterIsSelf = 0
		self.layer = 1
		self.param = {}
		self.className = ""
	
	def setTempData( self, key, value ):
		self.param[ key ] = value
	
	def getTempData( self, key, default = None ):
		if key in self.param:
			return self.param[key]
		return default
	
	def getRemainingTime( self ):
		if self.endTime == 0:
			return -1    #表示永久
		
		remainingTime = self.endTime - Functions.getTime()
		return remainingTime if remainingTime > 0 else 0
		
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		buffData = []
		d = { 	"index" 	: obj.index,
				"buffID" 	: obj.buffID,
				"holdTime"	: obj.holdTime,
				"endTime" 	: obj.endTime,
				"timerID" 	: obj.timerID,
				"casterID" 	: obj.casterID,
				"casterIsSelf" 	: obj.casterIsSelf,
				"layer"		: obj.layer,
				"param"		: obj.param,
				"className"	: obj.className,
			}
		return d
		
	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = BuffDataType()
		obj.index = dict["index"]
		obj.buffID = dict["buffID"]
		obj.holdTime = dict["holdTime"]
		obj.endTime = dict["endTime"]
		obj.timerID = dict["timerID"]
		obj.casterID = dict["casterID"]
		obj.casterIsSelf = dict["casterIsSelf"]
		obj.layer = dict["layer"]
		obj.param = dict["param"]
		obj.className = dict["className"]
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, BuffDataType )


class BuffClientDataType:
	"""
	实现 buffs 数据创建、还原
	"""

	def __init__(self):
		self.index = 0
		self.buffID = 0
		self.holdTime = 0
		self.endTime = 0
		self.timerID = 0
		self.casterID = 0
		self.casterIsSelf = 0
		self.layer = 1
		self.className = ""

	def converting(self, buffData ):
		self.index = buffData.index
		self.buffID = buffData.buffID
		self.holdTime = buffData.holdTime
		self.endTime = buffData.endTime
		self.timerID = buffData.timerID
		self.casterID = buffData.casterID
		self.casterIsSelf = buffData.casterIsSelf
		self.layer = buffData.layer
		self.className = buffData.className

	def getDictFromObj(self, obj):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		buffData = []
		d = { "index" 	: obj.index,
				 "buffID" 	: obj.buffID,
				 "holdTime"	: obj.holdTime,
				 "endTime" 	: obj.endTime,
				 "timerID" 	: obj.timerID,
				 "casterID" 	: obj.casterID,
				 "casterIsSelf" 	: obj.casterIsSelf,
				 "layer"		: obj.layer,
				"className"	: obj.className,
				 }
		return d

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = BuffClientDataType()
		obj.index = dict["index"]
		obj.buffID = dict["buffID"]
		obj.holdTime = dict["holdTime"]
		obj.endTime = dict["endTime"]
		obj.timerID = dict["timerID"]
		obj.casterID = dict["casterID"]
		obj.casterIsSelf = dict["casterIsSelf"]
		obj.layer = dict["layer"]
		obj.className = dict["className"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, BuffClientDataType )

class BuffDatasType( dict ) :
	"""
	实现 buffs 数据创建、还原
	"""
	def __init__(self):
		dict.__init__(self)
		self.buffIDToBuff = {}
		self.forClientDict = {}
		
	def __setitem__(self, buffIndex, buff):
		dict.__setitem__(self, buffIndex, buff)
		if buff.buffID not in self.buffIDToBuff:
			self.buffIDToBuff[buff.buffID] = []
		self.buffIDToBuff[buff.buffID].append(buff)
		
		cbuffData = BuffClientDataType()
		cbuffData.converting( buff )
		self.forClientDict[ buffIndex ] = cbuffData

	def pop(self, buffIndex, default = None ):
		if buffIndex not in self:
			return default
		if self[buffIndex].buffID in self.buffIDToBuff:
			buffList = self.buffIDToBuff[self[buffIndex].buffID]
			if self[buffIndex] in buffList:
				buffList.remove(self[buffIndex])
			if not buffList:
				self.buffIDToBuff.pop(self[buffIndex].buffID)
				
		if buffIndex in self.forClientDict:
			del self.forClientDict[ buffIndex ]
			
		return dict.pop(self, buffIndex, default)

	def getBuffByBuffID(self, buffID):
		return self.buffIDToBuff.get(buffID, [])
		
	def delBuffByBuffID(self, buffID):
		self.buffIDToBuff.pop(buffID, [])

	def upClientData(self, ownerEntity ):
		ownerEntity.setAttrBuffsForClient( list( self.forClientDict.values() ) )

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		buffData = []
		for buff in obj.values() :
			buffData.append( buff )

		return {"buffData": buffData}
		
	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = BuffDatasType()
		buffData = dict["buffData"]
		for buff in buffData :
			obj[ buff.index ] = buff

		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, BuffDatasType )


instance  = BuffDataType()
buffDictInstance = BuffDatasType()
clientInstance = BuffClientDataType()



