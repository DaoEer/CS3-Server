# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopyActivity import SpaceDomainCopyActivity
import KBEDebug

class SpaceDomainCopyCampRandomFit( SpaceDomainCopyActivity ):
	"""
	阵营战场随机匹配 副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopyActivity.__init__( self )
		self.playerDBIDDict = {}
	
	def initData( self, configData ):
		SpaceDomainCopyActivity.initData( self, configData )

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		# spaceNumber = -1
		# for key, playerDBIDList in self.playerDBIDDict.items():
		# 	if pickArgs["playerDBID"] in playerDBIDList:
		# 		spaceNumber = key
		# spaceItem = self.getSpaceItem(spaceNumber)
		# if not spaceItem:
		# 	spaceObject = self.getSpaceObject()
		# 	exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
		# 	roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
		# 	return
		# spaceItem.login( roleMB, pickArgs )
		spaceObject = self.getSpaceObject()
		exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
		roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )

	def onSpaceLoseCell( self, spaceNumber ):
		SpaceDomainCopyActivity.onSpaceLoseCell( self, spaceNumber )

	def requestNewSpace( self, params ):
		"""
		define method.
		请求预创建一个指定的space
		"""
		SpaceDomainCopyActivity.createSpaceItem( self, params )

	def onSpaceCreateCallBack( self, spaceItem, spaceBase ):
		"""
		virtual method
		space base创建完成
		"""
		SpaceDomainCopyActivity.onSpaceCreateCallBack( self, spaceItem, spaceBase )
		self.playerDBIDDict[spaceItem.spaceNumber] = spaceItem.createArgs.get("playerDBIDs",[])
	
	def findSpaceItem( self,  roleMB, pickArgs ):
		"""
		virtual method
		查找一个空间
		"""
		spaceKey = pickArgs["spaceKey"]
		belongType = pickArgs["belongType"]
		playerDBID = pickArgs["playerDBID"]
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceKey == spaceKey and spaceItem.belongType == belongType and playerDBID in self.playerDBIDDict.get(spaceItem.spaceNumber,[]):
				return spaceItem
		return None