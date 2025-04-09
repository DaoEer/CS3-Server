# -*- coding: utf-8 -*-

import csdefine
from SpaceMultiLine import SpaceMultiLine


class SpaceLunHuiMiJinMultiLine2( SpaceMultiLine ):
	"""
	轮回秘境第二层地图
	"""
	def __init__( self ):
		SpaceMultiLine.__init__( self )
		self.controlCloseTimer = 0
		
	def onCloseSpace(self):
		"""
		"""
		self.controlCloseTimer = 0
		#这里只能走直接关闭space的接口，不然关闭副本的时候，把玩家踢出地图可能会存在问题
		if hasattr(self, "cell") and self.cell:
			self.cell.closeSpace()
		
	def onControlClose(self):
		"""
		define method
		关闭space
		"""
		if not self.controlCloseTimer:
			self.controlCloseTimer = self.addTimerCallBack(csdefine.CONTROL_SPACE_CLOSE_TIME, "onCloseSpace", ())
		#通知到cell，即将关闭了，主要是控制进入机缘副本的玩家重新进入轮回秘境2副本。
		if hasattr(self, "cell") and self.cell:
			self.cell.onNotifyCloseSpace()
		