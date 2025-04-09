# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyTrainGroundPVP( SpaceDomainCopy ):
	"""
	练兵场PVP 空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self.spaceKeyToPlayerDBIDs = {}
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )

	def getSpaceKeyByPlayerDBID( self, playerDBID ):
		"""
		获得spaceKey
		"""
		for spaceKey, enterDBIDs in self.spaceKeyToPlayerDBIDs.items():
			if playerDBID in enterDBIDs:
				return spaceKey
		return None

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		playerDBID = pickArgs.get("playerDBID")
		spaceKey = self.getSpaceKeyByPlayerDBID( playerDBID )
		pickArgs["spaceKey"] = spaceKey
		spaceItem = self.findSpaceItem( roleMB, pickArgs )
		if spaceItem == None:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			if exitScriptID == "":
				KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
				return
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		spaceItem.login( roleMB, pickArgs )

	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		spaceItem = self.findSpaceItem( roleMB, pickArgs )
		if not spaceItem:
			spaceItem = self.createSpaceItem( pickArgs )

		spaceItem.enter( roleMB, position, direction, pickArgs )

		if spaceItem.spaceKey not in self.spaceKeyToPlayerDBIDs:
			self.spaceKeyToPlayerDBIDs[spaceItem.spaceKey] = set()
		enterDBIDs = pickArgs.get("enterDBIDs",[])

		self.spaceKeyToPlayerDBIDs[spaceItem.spaceKey].update(enterDBIDs)