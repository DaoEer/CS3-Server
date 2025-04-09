# -*- coding: utf-8 -*-

import KBEngine

class TeamSpaceRelationInterface:
	"""
	队伍副本接口,TeamEntity接口
	"""
	def __init__( self ):
		"""
		"""
		self.teamRelationSpace = []
	
	def registerRelationSpace( self, spaceClassName ):
		"""
		<define method>
		记录与队伍相关的副本
		"""
		self.teamRelationSpace.append( spaceClassName )
		dbids = []
		for entityID, tempinfo in self.member:
			dbids.append( tempinfo.dbid )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( spaceClassName, "registerRelationSpaceCB", ( self.id, dbids ) )
	
	def unRegisterRelationSpace( self, spaceClassName ):
		"""
		<define method>
		移除队伍相关的副本
		"""
		self.teamRelationSpace.remove( spaceClassName )
	
	def onAddMember( self, memberDBID ):
		"""
		"""
		for spaceClassName in self.teamRelationSpace:
			KBEngine.globalData["SpaceManager"].remoteCallDomain( spaceClassName, "stRelation_onTeamAddMember", ( self.id, memberDBID ) )
	
	def onRemoveMember( self, memberDBID ):
		"""
		"""
		for spaceClassName in self.teamRelationSpace:
			KBEngine.globalData["SpaceManager"].remoteCallDomain( spaceClassName, "stRelation_onTeamRemoveMember", ( self.id, memberDBID ) )
	
	def onDisband( self ):
		"""
		"""
		for spaceClassName in self.teamRelationSpace:
			KBEngine.globalData["SpaceManager"].remoteCallDomain( spaceClassName, "stRelation_onTeamDisband", ( self.id, ) )