# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceBase import SpaceBase
import Const
import KBEngine
import csdefine

class SpaceMultiLine( SpaceBase ):
	def __init__( self ):
		SpaceBase.__init__( self )
		self.lineMaxPlayerAmout = 0

	def initData( self, configData ):
		SpaceBase.initData( self, configData )
		self.lineMaxPlayerAmout = configData["SpaceData"].get("maxPlayerAmount",0)

	def onEnter( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceBase.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.setLineNumber( int(selfEntity.spaceKey) )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( selfEntity.scriptID,"incPlayerAmount",(int(selfEntity.spaceKey),playerRole.playerDBID))

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceBase.onLeave( self, selfEntity, playerRole, packArgs )
		playerRole.setLineNumber( 0 )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( selfEntity.scriptID,"decPlayerAmount",(int(selfEntity.spaceKey),playerRole.playerDBID))

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceBase.onLogin( self, selfEntity, playerRole )
		playerRole.setLineNumber( int(selfEntity.spaceKey) )
		KBEngine.globalData["SpaceManager"].remoteCallDomain( selfEntity.scriptID,"incPlayerAmount",(int(selfEntity.spaceKey),playerRole.playerDBID))

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		gotoArgs = SpaceBase.getPackDomainData( self, playerEntity, args )
		gotoArgs["spaceKey"] = str(playerEntity.queryTemp( "lineNumber",-1))
		
		gotoArgs[ "currSpaceScriptID" ] = playerEntity.getCurrentSpaceScriptID()

		if int(playerEntity.getCurrentSpaceData( Const.SPACE_DATA_SPACE_TYPE )) == csdefine.SPACE_TYPE_MULTILINE:
			gotoArgs[ "currSpaceLineNumber" ] = int(playerEntity.getCurrentSpaceData(Const.SPACE_DATA_LINE_NUMBER))
		else:
			gotoArgs[ "currSpaceLineNumber" ] = 0
		return gotoArgs

	def checkFullOnTeleport( self, selfEntity ):
		"""
		传送前检查地图人数是否满足
		"""
		if len(selfEntity._spaceRoles) >= self.lineMaxPlayerAmout:
			return False
		return True
		
		
		