
# -*- coding: utf-8 -*-
"""
cell部份的QuestAIIDSImpl实现模块.
"""
import KBEngine
import KBEDebug 

class QuestAIIDSImpl:
	"""
	任务下保存的AI行为
	"""

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		d = {"questID":obj.questID,"aiIDS":[]}
		for aiID in obj.aiIDS:
			d["aiIDS"].append(aiID)

		return d
		
	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = QuestAIIDSImpl()
		obj.questID = dict["questID"]
		obj.aiIDS = dict["aiIDS"]
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, QuestAIIDSImpl )

#自定义类型实现实例
instance = QuestAIIDSImpl()

