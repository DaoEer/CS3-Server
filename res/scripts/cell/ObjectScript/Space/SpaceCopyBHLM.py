# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Math

class SpaceCopyBHLM( SpaceCopy ):
	"""
	CST-8725 冰火灵脉副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.wolfScriptID = ""
	
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.wolfScriptID = configData["SpaceData"].get( "wolfScriptID","" )

	def createCallWolfMonster( self, selfEntity, position, direction ):
		"""
		创建降服的狼王
		"""
		captain = None
		for role in selfEntity._spaceRoles:
			if role.isTeamCaptain():
				captain = role
				break
		if not captain:
			return

		params = {}
		params["owner"] = captain.base
		params["enableSpace"] = []
		params["spawnPos"] = Math.Vector3(position)
		params["spawnDir"] = Math.Vector3(direction)
		params["level"] = captain.level
		captain.createMonsterExtCall(self.wolfScriptID, selfEntity, position, direction, params)

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		if playerRole.isTeamCaptain():
			self.addTimerCallBackForScript( 2.0,"changeFollow",() )

	def changeFollow( self, selfEntity ):
		"""
		改变狼王的跟随
		"""
		monsters = self.getEntityMailBoxRecord(self.wolfScriptID)
		captain = None
		for role in selfEntity._spaceRoles:
			if role.isTeamCaptain():
				captain = role
				break
		if not captain:
			return

		monsters[0].owner = captain.base
