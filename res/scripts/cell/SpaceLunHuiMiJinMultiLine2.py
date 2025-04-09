# -*- coding: utf-8 -*-

from SpaceMultiLine import SpaceMultiLine
import Const
import KBEDebug
import KBEngine

class SpaceLunHuiMiJinMultiLine2( SpaceMultiLine ):
	def __init__( self ):
		SpaceMultiLine.__init__( self )
		
	def onNotifyCloseSpace(self):
		"""
		define method
		base通知cell副本快要关闭了
		"""
		self.clearCellAppDataBeforeClose()
		
		
	
