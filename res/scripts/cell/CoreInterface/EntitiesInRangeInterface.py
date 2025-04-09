# -*- coding: utf-8 -*-
import KBEngine

import csdefine
import SearchScript
import csconst

class EntitiesInRangeInterface( object ):
	def __init__( self ):
		object.__init__( self )

	def getSearchScriptObj( self ):
		"""
		"""
		curSpaceScriptID = self.getCurrentSpaceScriptID()
		if curSpaceScriptID in SearchScript.g_SearchDict:
			return SearchScript.g_SearchDict[curSpaceScriptID]
		else:
			return SearchScript.g_SearchDict["SearchDefult"]

	def entitiesInRangeExt(self, range, entityType=None, position=None ):
		#默认方的
		searchScriptObj = self.getSearchScriptObj()
		return searchScriptObj.entitiesInRangeExt( self, range, entityType, position )

	def entitiesInRangeExtCircle(self, range, entityType=None, position=None ):
		# 圆的
		searchScriptObj = self.getSearchScriptObj()
		return searchScriptObj.entitiesInRangeExtCircle( self, range, entityType, position  )

	def entitiesInRangeExtForAI(self, radius, height = csconst.AI_ENTITIES_IN_RANGE_HEIGHT, entityType=None, scriptID=[], exceptStates=[csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD], position=None ):
		searchScriptObj = self.getSearchScriptObj()
		return searchScriptObj.entitiesInRangeExtForAI( self, radius, height, entityType, scriptID, exceptStates, position )

	def entitiesInRangeExtForBehind(self, length, height, entityType=None, scriptID=[], exceptStates=[csdefine.ENTITY_STATE_PEAD, csdefine.ENTITY_STATE_DEAD] ):
		searchScriptObj = self.getSearchScriptObj()
		return searchScriptObj.entitiesInRangeExtForBehind( self, length, height, entityType, scriptID, exceptStates )

