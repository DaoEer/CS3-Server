# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import time

class SpaceCopyJSZZ( SpaceCopy ):
	"""
	CST-7896 金树种子
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.isShowJSZZSettlement = False

	def getIsShowJSZZSettlement( self ):
		return self.isShowJSZZSettlement

	def setIsShowJSZZSettlement( self, isShowJSZZSettlement ):
		self.isShowJSZZSettlement = isShowJSZZSettlement