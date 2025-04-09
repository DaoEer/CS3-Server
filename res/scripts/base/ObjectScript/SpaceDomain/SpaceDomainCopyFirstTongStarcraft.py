# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyFirstTongStarcraft( SpaceDomainCopy ):
	"""
	帮会争霸 副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self.spaceKeyToSpaceNumber = {}
		self.tongInfo = {}
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )

	def activeStart( self ):
		"""
		活动开始
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activeStart()

	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		spaceKey = pickArgs.get("spaceKey")
		spaceItem = self.getSpaceItemByKey(spaceKey)
		if not spaceItem:
			KBEDebug.ERROR_MSG(" has not spaceItem ")
			return
		if spaceKey not in self.tongInfo:
			self.tongInfo[spaceKey] = []
		self.tongInfo[spaceKey].append(pickArgs.get("playerDBID"))
		spaceItem.enter( roleMB, position, direction, pickArgs )

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		key = None
		for spaceKey, enterInfo in self.tongInfo.items():
			if pickArgs.get("playerDBID") in enterInfo:
				key = spaceKey
		spaceItem = self.getSpaceItemByKey(key)
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		spaceItem.login( roleMB, pickArgs )

	def onSpaceLoseCell( self, spaceNumber ):
		SpaceDomainCopy.onSpaceLoseCell( self, spaceNumber )
		if spaceNumber in self.spaceKeyToSpaceNumber.values():
			index = list(self.spaceKeyToSpaceNumber.values()).index(spaceNumber)
			key = list(self.spaceKeyToSpaceNumber.keys())[index]
			self.spaceKeyToSpaceNumber.pop(key)
			self.tongInfo.pop(key)

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
		self.spaceKeyToSpaceNumber[ spaceItem.spaceKey ] = spaceItem.spaceNumber

	def getSpaceItemByKey( self, spaceKey ):
		"""
		根据spaceKey查找相应的space 
		"""
		if spaceKey in self.spaceKeyToSpaceNumber:
			number = self.spaceKeyToSpaceNumber[ spaceKey ]
			return self.getSpaceItem( number )
		else:
			return None
		