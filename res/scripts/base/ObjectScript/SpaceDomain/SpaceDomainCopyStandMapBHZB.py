# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyStandMapBHZB( SpaceDomainCopy ):
	"""
	CST-11386 帮会争霸沙盘大地图 副本空间领域
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
		spaceKey = pickArgs.get("spaceKey")
		playerDBID = pickArgs["playerDBID"]
		spaceItem,key = self.getSpaceItemByKey(spaceKey)
		if not spaceItem:
			KBEDebug.ERROR_MSG(" has not spaceItem ")
			return
		pickArgs["spaceKey"] = key
		if key in self.spaceKeyToPlayerDBIDs:
			self.spaceKeyToPlayerDBIDs[key].append(playerDBID)
		spaceItem.enter( roleMB, position, direction, pickArgs )

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		key = None
		for spaceKey, playerDBIDs in self.spaceKeyToPlayerDBIDs.items():
			if pickArgs.get("playerDBID") in playerDBIDs:
				key = spaceKey

		spaceNumber = self.spaceKeyToSpaceNumber.get(key,None)
		spaceItem = self.getSpaceItem( spaceNumber )
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		pickArgs["spaceKey"] = key
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
		self.spaceKeyToPlayerDBIDs[ spaceItem.spaceKey ] = []

	def getSpaceItemByKey( self, spaceKey ):
		"""
		根据spaceKey查找相应的space 
		"""
		for key,number in self.spaceKeyToSpaceNumber.items():
			if spaceKey in key.split("|"):
				return self.getSpaceItem( number ),key
		return None

	def changeMemberGroup( self, tongDBID, groupDict ):
		"""
		改变玩家所在的组
		"""
		spaceItem = self.getSpaceItemByKey( str(tongDBID) )
		if not spaceItem:
			return

		if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
			spaceItem.spaceMailBox.cell.changeMemberGroup( tongDBID, groupDict )

