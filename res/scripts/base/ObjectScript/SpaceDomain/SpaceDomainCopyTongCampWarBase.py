# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyTongCampWarBase( SpaceDomainCopy ):
	"""
	CST-8722 帮会阵营战 大本营空间组
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self.spaceKeyToSpaceNumber = {}
		self.spaceKeyToPlayerDBIDs = {}

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		playerDBID = pickArgs.get(playerDBID)
		spaceKey = self.findSpaceKey( playerDBID )
		spaceItem = self.getSpaceItemByKey(spaceKey)
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
			self.spaceKeyToPlayerDBIDs.pop(key)

	def findSpaceKey( self, playerDBID ):
		"""
		通过玩家的DBID 查找SpaceKey
		"""
		spaceKey = ""
		for key, playerDBIDs in self.spaceKeyToPlayerDBIDs.items():
			if playerDBID in playerDBIDs:
				spaceKey = key
				break

		return spaceKey

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
		self.spaceKeyToPlayerDBIDs[spaceItem.spaceKey] = spaceItem.createArgs.get("playerDBIDs",[])

	def getSpaceItemByKey( self, spaceKey ):
		"""
		根据spaceKey查找相应的space 
		"""
		if spaceKey in self.spaceKeyToSpaceNumber:
			number = self.spaceKeyToSpaceNumber[ spaceKey ]
			return self.getSpaceItem( number )
		else:
			return None