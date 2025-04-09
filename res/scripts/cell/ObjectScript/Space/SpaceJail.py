# -*- coding: utf-8 -*-

import csdefine
import csstatus
from ObjectScript.Space.SpaceMultiLine import SpaceMultiLine


class SpaceJail( SpaceMultiLine ):
	"""
	监狱
	"""
	def __init__( self ):
		SpaceMultiLine.__init__( self )
	
	def checkLeaveEnable( self, player, params ):
		"""
		virtual method
		检测离开条件
		"""
		if not params.get( "isTalkLeave", False ):	#不是对话离开
			return csstatus.CANNOT_TRANSPORT_IN_JAIL
		return csstatus.SPACE_ENTER_OR_LEAVE_OK
	
	def onEnter( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceMultiLine.onEnter( self, selfEntity, playerRole, packArgs )
		if playerRole.isState( csdefine.ENTITY_STATE_DEAD ):
			playerRole.reviveOnOrigin()	#原地复活，避免复活不了出不了监狱