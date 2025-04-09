# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyFirstTongStarcraft7904( SpaceDomainCopy ):
	"""
	帮会争霸 第一场 副本空间领域 CST-7904
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self.spaceKeyToSpaceNumber = {}
		self.spaceKeyToPlayerDBIDs = {}
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )

	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		key = pickArgs.get("spaceKey")
		playerDBID = pickArgs.get("playerDBID")
		spaceKey,spaceItem = self.getSpaceItemByKey(key)
		if not spaceItem:
			KBEDebug.ERROR_MSG(" has not spaceItem ")
			return
		spaceItem.enter( roleMB, position, direction, pickArgs )
		if spaceKey not in self.spaceKeyToPlayerDBIDs:
			self.spaceKeyToPlayerDBIDs[spaceKey] = []
		self.spaceKeyToPlayerDBIDs[spaceKey].append(playerDBID)

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		playerDBID = pickArgs.get( "playerDBID" )
		findKey = ""
		for spaceKey, playerDBIDs in self.spaceKeyToPlayerDBIDs.items():
			if playerDBID in playerDBIDs:
				findKey = spaceKey
				break
		number = -1
		if findKey in self.spaceKeyToSpaceNumber:
			number = self.spaceKeyToSpaceNumber[ findKey ]
		spaceItem = self.getSpaceItem( number )
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			if exitScriptID == "":
				KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
				return
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		spaceItem.login( roleMB, pickArgs )

	def onSpaceLoseCell( self, spaceNumber ):
		SpaceDomainCopy.onSpaceLoseCell( self, spaceNumber )
		if spaceNumber in self.spaceKeyToSpaceNumber.values():
			index = list(self.spaceKeyToSpaceNumber.values()).index(spaceNumber)
			key = list(self.spaceKeyToSpaceNumber.keys())[index]
			self.spaceKeyToSpaceNumber.pop(key)
			self.spaceKeyToPlayerDBIDs.pop(key)

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
		return spaceKey,self.getSpaceItem( number )
		