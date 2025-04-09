# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import math
import KBEngine
import csdefine
import csstatus
import Const
import time
import KBEMath
import Functions


class SpaceCopyTongTianDa( SpaceCopy ):
	"""
	通天塔
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		
	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		SpaceCopy.addEntityMailBoxRecord( self, scriptID, entityMailBox )
		if entityMailBox.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
			self.addTimerCallBack(0.5, "addBuffDelay", (entityMailBox,))
		
	def addBuffDelay( self, entityMailBox ):
		""""""
		spaceSript = self.getScript()
		if spaceSript.buffList and self._spaceRoles:
			playerRole = self._spaceRoles[0]
			index = min( max( playerRole.level - playerRole.layerNumber, 0 ), len(spaceSript.buffList) - 1 )
			buffID = spaceSript.buffList[index]
			entityMailBox.addBuff( entityMailBox, buffID )
		
	def onEnter( self, playerRole, packArgs ):
		""""""
		SpaceCopy.onEnter( self, playerRole, packArgs )
		
		spaceSript = self.getScript()
		if spaceSript.buffList:
			index = min( max( playerRole.level - playerRole.layerNumber, 0 ), len(spaceSript.buffList) - 1 )
			buffID = spaceSript.buffList[index]
			for scriptID, entityMBs in self.entityMailBoxRecord.items():
				for entityMB in entityMBs:
					if entityMB.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
						entityMB.addBuff( entityMB, buffID )