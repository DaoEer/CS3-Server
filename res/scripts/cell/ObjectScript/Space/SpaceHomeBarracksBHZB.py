# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceMultiLine import SpaceMultiLine
import Const
import KBEngine
import csdefine
from ObjectScript.Space.SpaceBase import SpaceBase

class SpaceHomeBarracksBHZB( SpaceMultiLine ):
	"""
	帮会争霸大本营
	"""
	def __init__( self ):
		SpaceMultiLine.__init__( self )
		

	def initData( self, configData ):
		SpaceMultiLine.initData( self, configData )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceBase.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.setLineNumber( int(selfEntity.spaceKey) )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceBase.onLeave( self, selfEntity, playerRole, packArgs )
		playerRole.setLineNumber( 0 )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceBase.onLogin( self, selfEntity, playerRole )
		playerRole.setLineNumber( int(selfEntity.spaceKey) )

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		gotoArgs = SpaceBase.getPackDomainData( self, playerEntity, args )
		gotoArgs["spaceKey"] = playerEntity.tongDBID
		return gotoArgs
