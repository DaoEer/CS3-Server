# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyBHZBPoint( SpaceDomainCopy ):
	"""
	帮会争霸据点空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )
		self.spaceKeyToSpaceNumber = {}
		self.spaceKeyToPlayerDBIDs = {}
	
	def initData( self, configData ):
		SpaceDomainCopy.initData( self, configData )

	def findSpaceItemBySpaceKey( self, spaceKey ):
		"""
		virtual method
		查找一个空间
		"""
		spaceNumber = self.spaceKeyToSpaceNumber.get(spaceKey,0)
		return self.getSpaceItem( spaceNumber )

	def getSpaceKeyByPlayerDBID( self, playerDBID ):
		"""
		"""
		for spaceKey, playerDBIDs in self.spaceKeyToPlayerDBIDs.items():
			if playerDBID in playerDBIDs:
				return spaceKey
		return ""

	def onSpaceLoseCell( self, spaceNumber ):
		SpaceDomainCopy.onSpaceLoseCell( self, spaceNumber )
		if spaceNumber in self.spaceKeyToSpaceNumber.values():
			index = list(self.spaceKeyToSpaceNumber.values()).index(spaceNumber)
			key = list(self.spaceKeyToSpaceNumber.keys())[index]
			self.spaceKeyToSpaceNumber.pop(key)
			self.spaceKeyToPlayerDBIDs.pop(key)

	def roleLogin( self, roleMB, pickArgs  ):
		"""
		virtual method
		玩家登陆
		"""
		spaceKey = self.getSpaceKeyByPlayerDBID( pickArgs["playerDBID"] )
		spaceItem = self.findSpaceItemBySpaceKey(spaceKey)
		if not spaceItem:
			spaceObject = self.getSpaceObject()
			exitScriptID, exitPosition, exitDirection = spaceObject.getReviveToExitInfo( roleMB, pickArgs )
			if exitScriptID == "":
				KBEDebug.CRITICAL_MSG( "Space Config Exit SpaceScriptID is Empty!!!!" )
				return
			roleMB.loginToConfigSpace( exitScriptID, exitPosition, exitDirection )
			return
		spaceItem.login( roleMB,pickArgs )
		
	def gotoSpace( self, roleMB, position, direction, pickArgs ):
		"""
		virtual method
		玩家传送
		"""
		playerDBID = pickArgs["playerDBID"]
		spaceKey = pickArgs["spaceKey"]
		spaceItem = self.findSpaceItemBySpaceKey(spaceKey)
		if not spaceItem:
			spaceItem = self.createSpaceItem( pickArgs )

		if spaceItem.spaceKey not in self.spaceKeyToSpaceNumber:
			self.spaceKeyToSpaceNumber[spaceItem.spaceKey] = spaceItem.spaceNumber
		if spaceItem.spaceKey not in self.spaceKeyToPlayerDBIDs:
			self.spaceKeyToPlayerDBIDs[spaceItem.spaceKey] = []

		self.spaceKeyToPlayerDBIDs[spaceItem.spaceKey].append( playerDBID )
		spaceItem.enter( roleMB, position, direction, pickArgs )

	def statusMsgToAllMember( self, camp,msgID,msgArgs ):
		"""
		广播消息
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
				spaceItem.spaceMailBox.cell.statusMsgToMember( msgID, msgArgs )

	def statusMsgToTongMember( self, camp,tongDBID,msgID,msgArgs ):
		"""
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.createArgs.get("declareTongDBID",0) == tongDBID or int(spaceItem.spaceKey.split("|")[1]) == tongDBID:
				if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
					spaceItem.spaceMailBox.cell.statusMsgToTongMember( msgID, msgArgs,tongDBID )

	def updateBHZBWarDetailIntegralData( self, camp,tongDBID,integral,rank ):
		"""
		更新帮会争霸详情积分和排名数据
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.createArgs.get("declareTongDBID",0) == tongDBID or int(spaceItem.spaceKey.split("|")[1]) == tongDBID:
				if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
					spaceItem.spaceMailBox.cell.updateBHZBWarDetailIntegralData( tongDBID, integral, rank )

	def updateBHZBWarDetailOccupyNumber( self, camp, tongDBID, occupyPointAmount ):
		"""
		更新帮会争霸详情占领的据点数据
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.createArgs.get("declareTongDBID",0) == tongDBID or int(spaceItem.spaceKey.split("|")[1]) == tongDBID:
				if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
					spaceItem.spaceMailBox.cell.updateBHZBWarDetailOccupyNumber( tongDBID, occupyPointAmount )

	def updateBHZBWarDetailTeamData( self, camp,tongDBID, teamNumber, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情队伍数据
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.createArgs.get("declareTongDBID",0) == tongDBID or int(spaceItem.spaceKey.split("|")[1]) == tongDBID:
				if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
					spaceItem.spaceMailBox.cell.updateBHZBWarDetailTeamData( tongDBID, teamNumber, pointNumber, pointState, pointName )

	def removeBHZBWarDetailTeamData( self, camp,tongDBID, teamNumber ):
		"""
		移除帮会争霸详情队伍数据
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.createArgs.get("declareTongDBID",0) == tongDBID or int(spaceItem.spaceKey.split("|")[1]) == tongDBID:
				if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
					spaceItem.spaceMailBox.cell.removeBHZBWarDetailTeamData( tongDBID, teamNumber )

	def updateBHZBWarDetailOccupyPointData( self, camp, tongDBID, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情据点占领数据
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.createArgs.get("declareTongDBID",0) == tongDBID or int(spaceItem.spaceKey.split("|")[1]) == tongDBID:
				if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
					spaceItem.spaceMailBox.cell.updateBHZBWarDetailOccupyPointData(  tongDBID, pointNumber, pointState, pointName )

	def removeBHZBWarrDetailOccupyPoint( self, camp, tongDBID, pointNumber ):
		"""
		移除帮会争霸详情占领据点
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.createArgs.get("declareTongDBID",0) == tongDBID or int(spaceItem.spaceKey.split("|")[1]) == tongDBID:
				if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
					spaceItem.spaceMailBox.cell.removeBHZBWarrDetailOccupyPoint( tongDBID, pointNumber )

	def addBHZBWarMsgData( self, camp,tongDBID, statusID, statusArgs ):
		"""
		增加帮会争霸详情提示消息数据
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.createArgs.get("declareTongDBID",0) == tongDBID or int(spaceItem.spaceKey.split("|")[1]) == tongDBID:
				if spaceItem.spaceMailBox and spaceItem.spaceMailBox.cell:
					spaceItem.spaceMailBox.cell.addBHZBWarMsgData( tongDBID, statusID, statusArgs )
