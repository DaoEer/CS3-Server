# -*- coding: utf-8 -*-

import KST
import csdefine
import KBEngine
import KBEDebug


class RoleFixedUpdateInterface:
	def __init__( self ):
		pass
		
	def onGetCell( self ):
		self.checkFixedTime()
	
	def checkFixedTime(self):
		"""
		检查是否更新
		"""	
		for fixedTimeType in csdefine.FIXED_UPDATE_TOKEN_LIST:
			key = csdefine.FIXED_UPDATE_KEY + str(fixedTimeType)
			if self.tokenDict.get(key, "") != KBEngine.globalData.get(key, ""):
				self.fixedTimeUpdate(fixedTimeType, KBEngine.globalData.get(key, ""))
			
	def fixedTimeUpdate(self, fixedTimeType, token):
		KBEDebug.DEBUG_MSG("role[%d:%d] fixedTimeUpdate, %d, %s" %(self.databaseID, self.id, fixedTimeType, token))
		self.onFixedTimeUpdate(fixedTimeType, token)
		if hasattr(self, "cell") and self.cell:
			self.cell.fixedTimeUpdate(fixedTimeType, token)
		
	def onFixedTimeUpdate(self, fixedTimeType, token):
		"""
		定点更新
		"""
		key = csdefine.FIXED_UPDATE_KEY + str(fixedTimeType)
		self.tokenDict[key] = token
		
		#0点更新
		if fixedTimeType == csdefine.FIXED_UPDATE_TOKEN_ZERO:
			pass
