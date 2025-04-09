# -*- coding: utf-8 -*-

import csdefine

class BunchSpaceItem:
	"""
	一个副本串
	"""
	def __init__( self, domainObj, belongType, spaceKey ):
		self.domainObj = domainObj
		self.belongType = belongType	# 副本串归属类型
		self.spaceKey = spaceKey		# 副本串归属key
		self._createList = []
		self._completeList = []
		self._destroyList = []
		self.enterPlayerRecord = []
	
	def onSpaceCreateCell( self, childSpaceScriptID ):
		"""
		子副本创建
		"""
		self._createList.append( childSpaceScriptID )
	
	def onSpaceLoseCell( self, childSpaceScriptID ):
		"""
		子副本销毁
		"""
		self._destroyList.append( childSpaceScriptID )
	
	def canDestroy( self ):
		existList = list( set( self._createList ) ^ set( self._destroyList ) )
		return len( existList ) == 0
	
	def onEnterSpace( self, activityType, roleMB, roleDBID ):
		"""
		玩家进子副本
		"""
		if roleDBID not in self.enterPlayerRecord:
			self.enterPlayerRecord.append( roleDBID )
			isFirstEnter = True
		else:
			isFirstEnter = False
		roleMB.cell.onEnterBunchSpace( self.domainObj.scriptID, isFirstEnter, activityType )
	
	def onSpaceSuccess( self, childSpaceIndex ):
		"""
		子副本通关
		"""
		self._completeList.append( childSpaceIndex )