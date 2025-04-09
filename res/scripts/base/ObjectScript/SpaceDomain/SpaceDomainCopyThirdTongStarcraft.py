# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyThirdTongStarcraft( SpaceDomainCopy ):
	"""
	帮会争霸 第三场 副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self.campToSpaceNumber = {} 	#camp:Number
		self.campToPlayerDBIDs = {}		#camp:[]
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )

	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		camp = pickArgs.get("camp")
		playerDBID = pickArgs.get("playerDBID")
		if camp not in self.campToSpaceNumber:
			spaceItem = self.createSpaceItem( pickArgs )
			self.campToSpaceNumber[camp] = spaceItem.spaceNumber
		else:
			spaceNumber = self.campToSpaceNumber[camp]
			spaceItem = self.getSpaceItem( spaceNumber )
		if not spaceItem:
			KBEDebug.ERROR_MSG(" has not spaceItem ")
			return
		if camp not in self.campToPlayerDBIDs:
			self.campToPlayerDBIDs[camp] = []
		self.campToPlayerDBIDs[camp].append(playerDBID)
		spaceItem.enter( roleMB, position, direction, pickArgs )

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		playerDBID = pickArgs.get("playerDBID")
		roleCamp = None
		for camp, playerDBIDs in self.campToPlayerDBIDs.items():
			if playerDBID in playerDBIDs:
				roleCamp = camp
				break
		spaceNumber = self.campToSpaceNumber.get( roleCamp, 0 )
		spaceItem = self.getSpaceItem( spaceNumber )
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		spaceItem.login( roleMB, pickArgs )

	def onSpaceLoseCell( self, spaceNumber ):
		SpaceDomainCopy.onSpaceLoseCell( self, spaceNumber )
		if spaceNumber in self.campToSpaceNumber.values():
			index = list(self.campToSpaceNumber.values()).index(spaceNumber)
			key = list(self.campToSpaceNumber.keys())[index]
			self.campToSpaceNumber.pop(key)
			self.campToPlayerDBIDs.pop(key)		

	
		