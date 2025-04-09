# -*- coding: utf-8 -*-
#
import KBEngine
import KST
from KBEDebug import *
from csdefine import *
from CoreObject.MgrPersistentObject import MgrPersistentObject

class TeamManager(MgrPersistentObject):
	def __init__( self ):
		MgrPersistentObject.__init__( self )
		self.member = {}
		self.onCompleteInit()

	def register( self, teamMailBox ):
		"""
		<defined method>
		注册一支队伍
		
		@param teamMailBox: 队伍BaseEntityMailbox
		"""
		self.member[teamMailBox.id] = teamMailBox
	
	def deregister( self, teamID ):
		"""
		<defined method>
		删除一支队伍
		
		@param teamID: OBJECT_ID; 队伍ID
		"""
		if teamID in self.member:
			self.member.pop( teamID )

	def rejoinTeam( self, teamID, playerDBID, playerBase ):
		"""
		<defined method>
		玩家上线，请求尝试重新加入队伍
		
		@param     teamID: OBJECT_ID; 队伍ID
		@param playerDBID: 玩家DBID
		@param playerBase: 玩家BaseEntityMailbox
		"""
		if teamID not in self.member:
			playerBase.onRejoinTeamFailed()
			return
			
		self.member[teamID].teammateLogin( playerDBID, playerBase )		
	
	def teamRemoteCall( self, teamID, rFuncName, args ) :
		"""
		<define method>
		远程调用队伍的指定方法
		@type		teamID : OBJECT_ID
		@param		teamID : 队伍的ID
		@type		rFuncName : STRING
		@param		rFuncName : 队伍的远程方法名称
		@type		args : PY_ARGS
		@param		args : 远程方法参数组成的元组
		"""
		if teamID not in self.member :
			return
		try:
			getattr( self.member[teamID], rFuncName )( *args )
		except AttributeError as errstr:
			ERROR_MSG( "Team(ID:%i) not found. Remote method is %s" % ( teamID, rFuncName ) )
