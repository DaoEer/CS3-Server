# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopyJiYuan import SpaceCopyJiYuan
import csdefine
import KBEngine
import random

class SpaceCopyXKTB( SpaceCopyJiYuan ):
	"""
	副本虚空探宝
	"""
	def __init__( self ) :
		SpaceCopyJiYuan.__init__( self )

	def onStartProbeItem( self, entity, extcavateTime, currentText ):
		"""
		开始探测财宝
		"""
		entity.monsterAISendCommand( entity.id, "PROBE" )
		entity.allClients.DisplyCurrentText( currentText, 1 ) 				# 显示挖掘中
		self.extcavateTimerID = self.addTimerCallBack( random.randint( extcavateTime[0], extcavateTime[1] ),"onStartExcavateItem",( entity, ) )
	
	def onStartExcavateItem( self, entity ):
		"""
		挖掘出财宝
		"""
		entity.monsterAISendCommand( entity.id, "EXCAVATE" )
		
	def onPlayerExchangeToMoney(self, roleMB, playerIntegral, money):
		pass