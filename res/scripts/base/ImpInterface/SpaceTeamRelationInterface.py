# -*- coding: utf-8 -*-

import KBEngine

class TeamItem:
	"""
	一个队伍的数据
	"""
	def __init__( self ):
		self.memberDBIDs = []		# 队伍成员DBID列表
		self.relationSpace = []		# 对这个队伍感兴趣的副本
	
	def initMember( self, members ):
		self.memberDBIDs = members
	
	def clearMember( self ):
		self.memberDBIDs = []
	
	def addMember( self, dbid ):
		"""
		"""
		if dbid not in self.memberDBIDs:
			self.memberDBIDs.append( dbid )
	
	def removeMember( self, dbid ):
		"""
		"""
		if dbid in self.memberDBIDs:
			self.memberDBIDs.remove( dbid )
	
	def hasMember( self, dbid ):
		"""
		"""
		return dbid in self.memberDBIDs
	
	def addRelationSpace( self, spaceNumber ):
		"""
		"""
		self.relationSpace.append( spaceNumber )
	
	def removeRelationSpace( self, spaceNumber ):
		"""
		"""
		self.relationSpace.remove( spaceNumber )
	
	def hasNoRelationSpace( self ):
		return not len( self.relationSpace )

class SpaceTeamRelationInterface:
	"""
	队伍副本接口,SpaceDomain接口
	"""
	def __init__( self ):
		self.teamItems = {} # { teamID: teamItem }
	
	def buildSpaceTeamRelation( self, spaceNumber, teamID ):
		"""
		建立某个副本与某个队伍的关联
		"""
		if teamID not in self.teamItems:
			self.teamItems[ teamID ] = TeamItem()
			KBEngine.globalData["TeamManager"].teamRemoteCall( teamID, "registerRelationSpace", ( self.scriptID, ) )
		self.teamItems[ teamID ].addRelationSpace( spaceNumber )
	
	def registerRelationSpaceCB( self, teamID, teamMemDBIDs ):
		"""
		接收队伍成员dbid列表
		"""
		self.teamItems[ teamID ].initMember( teamMemDBIDs )
	
	def removeSpaceTeamRelation( self, spaceNumber, teamID ):
		"""
		取消某个副本与某个队伍的关联
		"""
		_item = self.teamItems[ teamID ]
		_item.removeRelationSpace( spaceNumber )
		if _item.hasNoRelationSpace():
			self.teamItems.pop( teamID )
			KBEngine.globalData["TeamManager"].teamRemoteCall( teamID, "unRegisterRelationSpace", ( self.scriptID, ) )
	
	def stRelation_onTeamAddMember( self, teamID, dbid ):
		"""
		队伍加人
		"""
		_item = self.teamItems.get( teamID, None )
		if _item:
			_item.addMember( dbid )
	
	def stRelation_onTeamRemoveMember( self, teamID, dbid ):
		"""
		队伍减人
		"""
		_item = self.teamItems.get( teamID, None )
		if not _item: return
		for _spaceNumber in _item.relationSpace:
			spaceItem = self.getSpaceItem( _spaceNumber )
			if not spaceItem:
				return
			spaceItem.spaceMailBox.cell.remoteScriptCall( "onTeamMemberLeave", ( teamID, dbid ) )
		_item.removeMember( dbid )
	
	def stRelation_onTeamDisband( self, teamID ):
		"""
		队伍解散
		"""
		_item = self.teamItems.get( teamID, None )
		if not _item: return
		for _spaceNumber in _item.relationSpace:
			spaceItem = self.getSpaceItem( _spaceNumber )
			if not spaceItem:
				return
			spaceItem.spaceMailBox.cell.remoteScriptCall( "onTeamDisband", ( teamID, _item.memberDBIDs ) )
		_item.clearMember()
	
	def isTeamMemberValid( self, teamID, memberDBID ):
		"""
		检测某玩家是否还在队伍中
		"""
		_item = self.teamItems.get( teamID, None )
		if not _item:
			return False
		return _item.hasMember( memberDBID )