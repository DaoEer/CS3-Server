# -*- coding: utf-8 -*-

import csdefine
import csstatus
import Const
import KBEngine
from ObjectScript.Space.SpaceBase import SpaceBase

class SpaceLunHuiMiJinMultiLine( SpaceBase ):
	"""
	轮回秘境多线地图
	"""
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
		if not playerRole.hasDongFu():
			playerRole.delayRequestOriginPet()

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceBase.onLeave( self, selfEntity, playerRole, packArgs )
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].decPlayerAmount( playerRole.playerDBID, int(selfEntity.spaceKey) )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceBase.onLogin( self, selfEntity, playerRole )
		if not playerRole.hasDongFu():
			playerRole.delayRequestOriginPet()

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		gotoArgs = SpaceBase.getPackDomainData( self, playerEntity, args )
		gotoArgs["spaceKey"] = str(playerEntity.queryTemp( "lineNumber",-1 ))
		
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
		
	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass