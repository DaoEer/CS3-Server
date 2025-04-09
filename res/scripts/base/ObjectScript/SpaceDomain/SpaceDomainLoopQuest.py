# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainLoopQuest( SpaceDomainCopy ):
	"""
	环任务秘境副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )
	
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
		roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )

	def notifyToCloseRingTaskParentSpace( self, playerDBIDStr ):
		"""
		关闭副本空间
		"""
		realSpaceItem = None
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceKey == playerDBIDStr:
				realSpaceItem = spaceItem
		if not realSpaceItem:
			return
		if realSpaceItem.spaceMailBox and realSpaceItem.spaceMailBox.cell:
			realSpaceItem.spaceMailBox.cell.closeSpace()
