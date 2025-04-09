# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopyActivity import SpaceDomainCopyActivity
import KBEDebug

class SpaceDomainCopyYXLM( SpaceDomainCopyActivity ):
	"""
	英雄联盟 副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopyActivity.__init__( self )
		self.spaceKeyToSpaceNumber = {}
		self.teamInfoDict = {}

	def activityStart( self ):
		"""
		"""
		pass

	def activityEnd( self ):
		"""
		活动结束
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.cell.closeSpace()
	
	def initData( self, configData ):
		SpaceDomainCopyActivity.initData( self, configData )

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		teamID = -1
		for teamID, teamInfos in self.teamInfoDict.items():
			if pickArgs["playerDBID"] in teamInfos:
				teamID = teamID
		spaceItem = self.getSpaceItemByKey(teamID)
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		spaceItem.login( roleMB, pickArgs )

	def onSpaceLoseCell( self, spaceNumber ):
		if spaceNumber in self.spaceKeyToSpaceNumber.values():
			index = list(self.spaceKeyToSpaceNumber.values()).index(spaceNumber)
			key = list(self.spaceKeyToSpaceNumber.keys())[index]
			self.spaceKeyToSpaceNumber.pop(key)
			self.removeSpaceTeamRelation(spaceNumber,key)
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
		for teamID in spaceItem.createArgs.get("teamInfos",[]):
			self.spaceKeyToSpaceNumber[ teamID ] = spaceItem.spaceNumber
			self.teamInfoDict[teamID] = spaceItem.createArgs.get(teamID,[])
			self.buildSpaceTeamRelation(spaceItem.spaceNumber,teamID)

	def getSpaceItemByKey( self, spaceKey ):
		"""
		根据spaceKey查找相应的space 
		"""
		if spaceKey in self.spaceKeyToSpaceNumber:
			number = self.spaceKeyToSpaceNumber[ spaceKey ]
			return self.getSpaceItem( number )
		else:
			return None
		