# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.DomainBase import DomainBase
from ImpInterface.SpaceTeamRelationInterface import SpaceTeamRelationInterface
import KBEDebug

class SpaceDomainCopyMagicMazeChild( DomainBase, SpaceTeamRelationInterface ):
	"""
	副本空间领域
	"""
	def __init__( self ):
		DomainBase.__init__( self )
		SpaceTeamRelationInterface.__init__( self )
	
	def initData( self, configData ):
		DomainBase.initData( self, configData )
	
	def createSpaceItem(self, params):
		"""
		创建一个新的空间
		"""
		spaceItem = DomainBase.createSpaceItem( self, params )
		KBEngine.globalData["SpaceManager"].onSpaceCopyItemCreate( self.scriptID, spaceItem.belongType, spaceItem.spaceKey )
		return spaceItem
	
	def findSpaceItem( self,  roleMB, pickArgs ):
		"""
		virtual method
		查找一个空间
		"""
		spaceKey = pickArgs["spaceKey"]
		belongType = pickArgs["belongType"]
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceKey == spaceKey and spaceItem.belongType == belongType:
				return spaceItem
		return None
	
	def onSpaceCreateCell( self, spaceNumber, spaceBase ):
		"""
		space cell创建完成
		"""
		DomainBase.onSpaceCreateCell( self, spaceNumber, spaceBase )	#基类方法必须放前面
		spaceItem = self.spaceItems[ spaceNumber ]
		KBEngine.globalData["MagicMazeSpaceManager"].onChildSpaceCreate( spaceItem.belongType, spaceItem.spaceKey, spaceBase, spaceItem.createArgs["mainScriptID"] )
		if spaceItem.belongType == csdefine.SPACE_BELONG_TEAM:
			self.buildSpaceTeamRelation( spaceItem.spaceNumber, spaceItem.createArgs["teamID"] )
	
	def onSpaceLoseCell( self, spaceNumber ):
		"""
		"""
		spaceItem = self.spaceItems[ spaceNumber ]
		if spaceItem.belongType == csdefine.SPACE_BELONG_TEAM:
			self.removeSpaceTeamRelation( spaceItem.spaceNumber, spaceItem.createArgs["teamID"] )
		
		KBEngine.globalData["SpaceManager"].onSpaceCopyItemDelete( self.scriptID, spaceItem.belongType, spaceItem.spaceKey )
		DomainBase.onSpaceLoseCell( self, spaceNumber )		#基类方法必须放后面
	
	#------------------------------外部调用接口-----------------------------------------------------
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
			spaceItem = self.createSpaceItem( pickArgs )
		
		spaceItem.enter( roleMB, position, direction, pickArgs )
	
	def onSpaceCreateCallBack( self, spaceItem, spaceBase ):
		"""
		virtual method
		space base创建完成
		"""
		pass

