# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopySparHunTing( SpaceDomainCopy ):
	"""
	晶石狩猎场 副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self._activityStart = False
		self.spaceKeyToSpaceNumber = {}
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )

	def activeStart( self ):
		"""
		活动开始
		"""
		self._activityStart = True
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activeStart()

	def activeEnd( self ):
		"""
		活动结束
		"""
		self._activityStart = False
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activeEnd()

	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		KBEngine.globalData["SparHunTingManager"].teleportPlayer( position, direction, roleMB, pickArgs )

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		spaceKey = pickArgs.get("spaceKey")
		spaceItem = self.getSpaceItemByKey(spaceKey)
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		spaceItem.login( roleMB, pickArgs )

	def teleportPlayerCallBack( self, roleMB, position, direction, params ):
		"""
		玩家传送
		"""
		spaceKey = params.get("spaceKey")
		spaceItem = self.getSpaceItemByKey( spaceKey )
		if spaceItem:
			spaceItem.enter( roleMB, position, direction, params )
		else:
			KBEDebug.ERROR_MSG("not found spaceItem(%s), role %d teleport fail" %(spaceKey, roleMB.id))
			
	def onSpaceLoseCell( self, spaceNumber ):
		SpaceDomainCopy.onSpaceLoseCell( self, spaceNumber )
		if spaceNumber in self.spaceKeyToSpaceNumber.values():
			index = list(self.spaceKeyToSpaceNumber.values()).index(spaceNumber)
			key = list(self.spaceKeyToSpaceNumber.keys())[index]
			self.spaceKeyToSpaceNumber.pop(key)

	# -------------------------------------------------
	# 空间预创建机制
	# -------------------------------------------------
	def requestNewSpace( self, params ):
		"""
		define method.
		请求预创建一个指定的space
		"""
		SpaceDomainCopy.createSpaceItem( self, params )

	def onSpaceCreateCallBack( self, spaceItem, spaceBase ):
		"""
		virtual method
		space base创建完成
		"""
		SpaceDomainCopy.onSpaceCreateCallBack( self, spaceItem, spaceBase )
		self.spaceKeyToSpaceNumber[spaceItem.spaceKey] = spaceItem.spaceNumber

	def getSpaceItemByKey( self, spaceKey ):
		"""
		根据spaceKey查找相应的space 
		"""
		if spaceKey in self.spaceKeyToSpaceNumber:
			number = self.spaceKeyToSpaceNumber[ spaceKey ]
			return self.getSpaceItem( number )
		else:
			return None