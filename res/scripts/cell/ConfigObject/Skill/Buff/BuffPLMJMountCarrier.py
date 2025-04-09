# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
#common
import csdefine
import csconst
from ConfigObject.Skill.Buff.BuffMountCarrier import BuffMountCarrier
#cell
import Functions


class BuffPLMJMountCarrier( BuffMountCarrier ):
	""""
	CST-13639
	"""
	def __init__( self ):
		BuffMountCarrier.__init__( self )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.client.CLIENT_ActivePLMJCarrierUI()
		BuffHold.doEnd( self, receiver, buffData,reason )
