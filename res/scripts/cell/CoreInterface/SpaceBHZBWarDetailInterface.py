# -*- coding: utf-8 -*-

import csdefine
import KBEngine
import KBEDebug

class SpaceBHZBWarDetailInterface:
	"""
	帮会争霸战场详情Interface
	"""
	def __init__( self ):
		pass

	def onTeleportCompleted( self, playerRole ):
		if playerRole.tongDBID not in self.warDetailMgr:
			return
		if playerRole.getClient():
			playerRole.client.InitBHZBWarDetailData( self.warDetailMgr[playerRole.tongDBID] )

	def addBHZBWarDetailData( self, tongDBID ):
		"""
		增加帮会争霸战场详情数据
		"""
		self.warDetailMgr.addBHZBWarDetailData( tongDBID )
		
	def updateBHZBWarDetailIntegralData( self, tongDBID, integral, rank ):
		"""
		更新帮会争霸详情积分和排名数据
		"""
		self.warDetailMgr.updateBHZBWarDetailIntegralData( tongDBID, integral, rank )
		for role in self._spaceRoles:
			if role.tongDBID == tongDBID and role.getClient():
				role.client.UpdateBHZBWarDetailIntegralData( integral, rank )

	def updateBHZBWarDetailOccupyNumber( self, tongDBID, occupyPointAmount ):
		"""
		更新帮会争霸详情占领的据点数据
		"""
		self.warDetailMgr.updateBHZBWarDetailOccupyNumber( tongDBID, occupyPointAmount )
		for role in self._spaceRoles:
			if role.tongDBID == tongDBID and role.getClient():
				role.client.UpdateBHZBWarDetailOccupyNumber( occupyPointAmount )

	def updateBHZBWarDetailTeamData( self, tongDBID, teamNumber, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情队伍数据
		"""
		lastPointNumber,lastPointState = self.warDetailMgr.getBHZBWarDetailTeamData( tongDBID, teamNumber )
		self.warDetailMgr.updateBHZBWarDetailTeamData( tongDBID, teamNumber, pointNumber, pointState, pointName )
		for role in self._spaceRoles:
			if role.tongDBID == tongDBID and role.getClient():
				role.client.UpdateBHZBWarDetailTeamData( teamNumber, pointNumber, pointState, pointName )

	def removeBHZBWarDetailTeamData( self, tongDBID, teamNumber ):
		"""
		移除帮会争霸详情队伍数据
		"""
		self.warDetailMgr.removeBHZBWarDetailTeamData( tongDBID, teamNumber )
		for role in self._spaceRoles:
			if role.tongDBID == tongDBID and role.getClient():
				role.client.RemoveBHZBWarDetailTeamData( teamNumber )

	def updateBHZBWarDetailOccupyPointData( self, tongDBID, pointNumber, pointState, pointName ):
		"""
		更新帮会争霸详情据点占领数据
		"""
		lastPointNumber,lastPointState = self.warDetailMgr.getBHZBWarDetailOccupyPointData( tongDBID, pointNumber )
		self.warDetailMgr.updateBHZBWarDetailOccupyPointData( tongDBID, pointNumber, pointState, pointName )
		for role in self._spaceRoles:
			if role.tongDBID == tongDBID and role.getClient():
				role.client.UpdateBHZBWarDetailOccupyPointData( pointNumber, pointState, pointName )

	def removeBHZBWarrDetailOccupyPoint( self, tongDBID, pointNumber ):
		"""
		移除帮会争霸详情占领据点
		"""
		self.warDetailMgr.removeBHZBWarrDetailOccupyPoint( tongDBID, pointNumber )
		for role in self._spaceRoles:
			if role.tongDBID == tongDBID and role.getClient():
				role.client.RemoveBHZBWarrDetailOccupyPoint( pointNumber )

	def addBHZBWarMsgData( self, tongDBID, statusID, statusArgs ):
		"""
		增加帮会争霸详情提示消息数据
		"""
		self.warDetailMgr.addBHZBWarMsgData( tongDBID,statusID, statusArgs )
		for role in self._spaceRoles:
			if role.tongDBID == tongDBID and role.getClient():
				role.client.AddBHZBWarMsgData( statusID, statusArgs )
