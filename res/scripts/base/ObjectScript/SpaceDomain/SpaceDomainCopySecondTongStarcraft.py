# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopySecondTongStarcraft( SpaceDomainCopy ):
	"""
	帮会争霸 第二场 副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self.spaceKeyToSpaceNumber = {}
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )

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
		spaceItem.enter( roleMB, position, direction, pickArgs )

	def onSpaceLoseCell( self, spaceNumber ):
		SpaceDomainCopy.onSpaceLoseCell( self, spaceNumber )
		if spaceNumber in self.spaceKeyToSpaceNumber.values():
			index = list(self.spaceKeyToSpaceNumber.values()).index(spaceNumber)
			key = list(self.spaceKeyToSpaceNumber.keys())[index]
			self.spaceKeyToSpaceNumber.pop(key)

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
		findKey = ""
		spaceKeys = self.spaceKeyToSpaceNumber.keys()
		for key in spaceKeys:
			if spaceKey in key.split("|"):
				findKey = key
				break
		number = self.spaceKeyToSpaceNumber[ findKey ]
		return self.getSpaceItem( number )
		