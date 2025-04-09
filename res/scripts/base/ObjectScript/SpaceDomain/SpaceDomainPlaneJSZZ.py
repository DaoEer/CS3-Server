# -*- coding: utf-8 -*-

import KBEngine
import csdefine
import KST
from ObjectScript.SpaceDomain.SpaceDomainPlane import SpaceDomainPlane

import KBEDebug

class SpaceDomainPlaneJSZZ( SpaceDomainPlane ):
	"""
	金树种子位面空间领域
	"""
	def __init__( self ):
		SpaceDomainPlane.__init__( self )
		
	
	def initData( self, configData ):
		SpaceDomainPlane.initData( self, configData )
	
	def createSpaceItem(self, params):
		"""
		创建一个新的空间
		"""
		params["spaceKey"] = str( params["playerDBID"] )
		spaceItem = SpaceDomainPlane.createSpaceItem( self, params )
		return spaceItem
	
	def onSpaceCreateCell( self, spaceNumber, spaceBase ):
		"""
		space cell创建完成
		"""
		SpaceDomainPlane.onSpaceCreateCell( self, spaceNumber, spaceBase )	#基类方法必须放前面
		
	
	def onSpaceLoseCell( self, spaceNumber ):
		"""
		"""
		
		SpaceDomainPlane.onSpaceLoseCell( self, spaceNumber )		#基类方法必须放后面

	def findSpaceItemByPlayerDBID( self, playerDBID,belongType ):
		"""
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceKey == playerDBID and spaceItem.belongType == belongType:
				return spaceItem
		return None
	
	#------------------------------外部调用接口-----------------------------------------------------
	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		spaceItem = self.findSpaceItemByPlayerDBID( str(pickArgs["playerDBID"]), pickArgs["belongType"] )
		KBEDebug.ERROR_MSG("++++++++++++++++",spaceItem)
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		
		spaceItem.login( roleMB, pickArgs )
	
	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		spaceItem = self.findSpaceItemByPlayerDBID( str(pickArgs["playerDBID"]), pickArgs["belongType"] )
		if not spaceItem:
			spaceItem = self.createSpaceItem( pickArgs )
		
		spaceItem.enter( roleMB, position, direction, pickArgs )
	