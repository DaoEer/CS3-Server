# -*- coding: utf-8 -*-

import KBEngine
import csdefine
import KBEDebug
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy

class SpaceDomainCopyGCZ( SpaceDomainCopy ):
	"""
	攻城战副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )
	
	def requestNewSpace( self, params ):
		"""
		define method.
		请求预创建一个指定的space
		"""
		SpaceDomainCopy.createSpaceItem( self, params )

	def findSpaceItem( self,  roleMB, pickArgs ):
		"""
		virtual method
		查找一个空间
		"""
		spaceKey = pickArgs["spaceKey"]
		belongType = pickArgs["belongType"]
		playerDBID = pickArgs["playerDBID"]
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceKey == spaceKey and spaceItem.belongType == belongType and playerDBID in spaceItem.createArgs["enterPlayerDBID"]:
				return spaceItem
		return None

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		spaceObject = self.getSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
		if exitScriptID == "":
			KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
			return
		spaceItem = self.findSpaceItem( roleMB, pickArgs )
		if not spaceItem:
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		
		if pickArgs["belongType"] == csdefine.SPACE_BELONG_TEAM:
			if not self.isTeamMemberValid( pickArgs["teamID"], pickArgs["playerDBID"] ):
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
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			if exitScriptID == "":
				KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
				return
			roleMB.cell.gotoSpace( exitScriptID, exitPosition, exitDirection )
			return
		
		spaceItem.enter( roleMB, position, direction, pickArgs )	
	
	
	