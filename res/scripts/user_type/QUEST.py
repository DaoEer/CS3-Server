# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *


if KBEngine.component == "cellapp":
	from ConfigObject.Quest.QuestBase.Quest import Quest
	from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader

	def getDictFromObj( obj ):
		""""""
		if obj is None:
			return { "id" : 0, "tasks": [] }
		return obj.packStreamData()

	def createObjFromDict( dictData ):
		""""""
		quest = g_QuestLoader.newQuest(dictData["id"])
		if quest is not None:
			quest.initFromStream(dictData)
		else:
			ERROR_MSG("QuestConverter::createObjFromDict: Quest with id %i "\
				"dosen't exist!" % dictData["id"])
		return quest

	def isSameType( obj ):
		""""""
		if obj is None: return True
		return isinstance( obj, Quest )

else:
	def getDictFromObj( obj ):
		""""""
		return obj

	def createObjFromDict( dictData ):
		""""""
		return dictData

	def isSameType( obj ):
		""""""
		return True


class QuestConverter:
	"""
	"""
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		DEBUG_MSG("QuestConverter::getDictFromObj:%s" % obj)
		return getDictFromObj(obj)

	def createObjFromDict( self, dictData ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dictData: The dictData parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		DEBUG_MSG( "QuestConverter::createObjFromDict:%s" % dictData.items() )
		return createObjFromDict(dictData)

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isSameType(obj)


inst = QuestConverter()